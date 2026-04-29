# Consultation Answers — Enfilade Properties

**Inquiry:** What abstract properties must the indexing data structure satisfy? What guarantees about range queries, composable widths, and structural balance does the system require — independent of any particular tree implementation?
**Date:** 2026-02-24 08:31
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a reader requests a contiguous range of a document — say, characters 5 through 50 — what must the system guarantee about the completeness and ordering of what is returned?

### Nelson's Answer

## Completeness and Ordering of Retrieved Content

When a reader requests a contiguous range — say, V-positions 5 through 50 — the system must guarantee three things:

### 1. Dense, Gap-Free Delivery

The V-stream is defined as a contiguous sequence with no holes. Nelson's model guarantees that V-addresses form a dense numbering starting at 1:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

If the document has 100 bytes, positions 1 through 100 all exist and are all retrievable. A request for positions 5 through 50 must return all 46 bytes. There is no possibility of "gaps" in the V-stream — the virtual byte stream is defined to be contiguous.

### 2. V-Stream Ordering Preserved

The bytes must come back in the order defined by the document's current arrangement. The V-stream defines a specific sequence, and that sequence is what the reader sees:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The ordering is the document's current V-space arrangement — which may differ from I-space storage order, from the chronological order of creation, and from the ordering in previous versions.

### 3. Origin Transparency

The returned byte stream must be seamless regardless of where the bytes physically originate. Some bytes in positions 5–50 might be native to this document; others might be transcluded from documents owned by entirely different users on different servers. The reader gets one unified stream:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

The front end does not see I-space addresses at all:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### The Part-Pounce Guarantee

Nelson emphasizes that the system must deliver the requested fragment *instantly*, materializing it on demand from whatever scattered storage fragments actually hold the content:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." [LM 2/16]

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you are, as it were, in midair." [LM 2/16]

The document need never exist as a single contiguous stored unit. The back end assembles the response from I-space fragments — potentially scattered across multiple documents and servers — and presents it as a seamless V-stream.

### The FEBE Operation

The operation that delivers content is RETRIEVEV, which Nelson describes as the *only* content-delivery command:

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." [LM 4/61]

> "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

The spec-set is a set of vspans — ranges in V-space. A request for characters 5–50 is a single vspan. The back end resolves each V-position to its I-address (via the positional mapping), fetches the bytes from their home locations (possibly across the network), and returns them in V-stream order as a unified response.

### Summary

For a request of V-positions 5 through 50, the system guarantees:

| Property | Guarantee |
|----------|-----------|
| **Completeness** | All 46 bytes are returned; the V-stream has no gaps |
| **Ordering** | Bytes arrive in V-stream sequence (the document's current arrangement) |
| **Transparency** | Native and transcluded bytes are indistinguishable in the response |
| **Materialization** | Content is assembled on demand from fragments; no pre-assembled document required |
| **Origin independence** | Content may come from multiple documents and servers; the reader sees one stream |

---

## Question 2 [nelson]

> If a document is built from several contributed pieces, must the total length of the document always equal the sum of the lengths of its constituent pieces, and must this hold at every level of aggregation?

### Nelson's Answer

## Yes — V-Stream Length Is Additive Over Its Constituent Spans

A document's virtual byte stream is a contiguous, gapless sequence from position 1 through *m*. Each position maps to exactly one I-space address. The document is composed of contiguous spans — some native, some transcluded — that partition this sequence without gaps or overlaps.

This makes additivity definitional:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The V-stream is flat — it doesn't care whether a byte is native or transcluded; each byte occupies exactly one V-position. INSERT confirms this accounting explicitly:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

No bytes are hidden, doubled, or compressed in V-space. The document's length is always the sum of its span lengths.

## This Holds at Every Level of Aggregation

When document D transcludes from B, and B itself transcludes from A, the accounting works at each level independently. Nelson's glass-pane metaphor describes the layering:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

But despite this conceptual layering, each document's V-stream is independently flat. D's V-stream has *m* positions; each maps to an I-address. Some of those I-addresses may be native to A, some to B, some to D — but the length of D's V-stream equals the sum of its component span lengths, regardless of provenance depth.

Similarly, B's V-stream is its own flat contiguous sequence with its own additive decomposition. The levels are independent.

The COPY operation (transclusion) makes this precise:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY shares I-addresses with the source. D doesn't get "B's bytes" — it gets the I-space bytes B was showing. The result is a new V-stream in D that includes spans pointing to those same I-addresses. Length accounting remains additive.

## The One Subtlety: Length Counts Positions, Not Unique Content

The same I-space content can be transcluded into a document multiple times. If a 100-byte passage from A is transcluded twice into D, D's V-stream has 200 positions — both transclusion spans map to the same I-addresses, but occupy distinct V-positions.

So:
- **V-stream length = sum of constituent span lengths** — always, by definition
- **V-stream length = number of unique I-space bytes referenced** — only when no content is transcluded more than once

Nelson's royalty model depends on this counting:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The split is proportional to V-stream composition — how many bytes each contributor accounts for in the virtual stream. If A's passage appears twice, A's share is proportionally larger.

## Summary

The V-stream is a contiguous sequence partitioned into non-overlapping spans. Length is additive over those spans at every level. This is not an extra constraint imposed on the system — it follows from the definition of V-space as a dense, gapless, flat byte stream where each position belongs to exactly one constituent span.

---

## Question 3 [nelson]

> Must the system guarantee that retrieving any range of a document takes time proportional to the size of that range, regardless of how large the document has grown or how many edits it has undergone?

### Nelson's Answer

## No — Nelson guarantees *fast* retrieval but not that specific complexity bound

Nelson makes strong aspirational claims about retrieval performance, but never formalizes a guarantee that retrieval time is proportional to the requested range size independent of document size or edit history. What he provides is weaker: a *system-wide* scaling requirement (the "soft corridor") and an *architectural* claim ("part-pounce"), supported by a *mechanism* claim (enfilades). Let me trace each.

---

### 1. The Soft Corridor: System-Wide Scaling

Nelson's most precise performance statement is about the *docuverse as a whole*, not individual document retrieval:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

This establishes that total system size should degrade response time only logarithmically. But this is about the network growing (more servers, more documents, more links), not about a single document accumulating edits. A document with a million edits is a different concern from a network with a million documents.

### 2. Part-Pounce: Instant Partial Retrieval

Nelson's user-facing guarantee is qualitative, not quantitative:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." [LM 2/16]

> "We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

Note the language: "we believe," "virtually instantaneous," "gives you that part instantly." These are design aspirations, not formal bounds. Nelson is saying the system *should* deliver partial retrieval without materializing the whole document — but he does not say the cost scales with the output size alone.

### 3. Enfilades: The Mechanism Claim

Nelson credits enfilades with making scalable retrieval possible:

> "the system we now call the first enfilade — the Model T: a data structure that manages huge agglomerates of text and their arrangement in and out of core. With its attendant routines, the Model T enfilade handles the revision of serial data very quickly and very cleanly." [LM 1/33]

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely." [LM 1/36]

"Could conceivably scale up infinitely" is weaker than "guarantees O(k + log n) retrieval." Nelson is saying the data structure *permits* scaling, not that it *guarantees* a specific bound.

### 4. What Nelson Does NOT Say

Nelson never states:

- A formal complexity bound (O(k), O(k log n), etc.)
- That retrieval cost is independent of edit history
- That retrieval cost is proportional to output size
- That the number of edits a document has undergone does not affect retrieval time

He also never addresses the specific concern your question raises: whether a document that has been edited a million times still delivers a 100-byte range as fast as a document edited once.

### 5. The Implicit Architecture

The I-space/V-space separation *implies* something close to your question. Since:

- V-space is a mapping over I-space content
- The POOM enfilade implements this mapping as a tree
- Tree lookups are logarithmic in tree size

...the intended architecture gives O(log n + k) retrieval where n is the POOM tree size and k is the output. But the POOM tree grows with edits (each edit restructures the tree), so retrieval is *not* independent of edit history — it's logarithmic in it.

Nelson does not state this explicitly. He states the aspiration ("virtually instantaneous") and the mechanism ("enfilades"), but the formal bound lives in the implementation, not in Literary Machines.

### Summary

| Claim | Stated by Nelson? | Formal? |
|-------|-------------------|---------|
| System scales logarithmically with total size | Yes [LM 4/2] | Semi-formal ("soft corridor") |
| Partial retrieval without full materialization | Yes [LM 2/16] | Qualitative only |
| Enfilades enable scalable retrieval | Yes [LM 1/33-1/36] | Mechanism claim, not bound |
| Retrieval time proportional to output size | No | — |
| Retrieval time independent of edit count | No | — |
| O(k + log n) bound on range retrieval | No | — |

**Nelson guarantees that you can retrieve any part of any version without materializing the whole document, and that the system stays responsive as it grows. He does not guarantee that retrieval time is proportional to the range size independent of document size or edit history.** That is a property of the enfilade implementation, not a user-facing guarantee from Literary Machines.

---

## Question 4 [nelson]

> The system must answer two kinds of questions about the same content — "what is at this position?" and "where did this content originate?" Must both queries be answerable from a single unified structure, or could they be served independently?

### Nelson's Answer

# Two Queries, Two Independent Structures

Nelson's architecture answers this clearly: the two queries are served by **independent structures that compose**, not by a single unified structure. This separation is deliberate and fundamental to the design.

## The Two Queries

**Query 1: "What is at this position?"**
This is a V→I→content traversal. Given a V-space address (position in the document's current arrangement), find the I-space address it maps to, then fetch the content at that I-address.

The FEBE operation is RETRIEVEV:
> "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

**Query 2: "Where did this content originate?"**
This is answered by the I-address itself. The I-address structurally encodes provenance — no separate lookup is required.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The I-address format `Node.0.User.0.Document.0.Element` directly encodes which server, which account, and which document created that byte [LM 4/26].

## Nelson Designed Them as Separate Structures

Nelson explicitly describes multiple enfilade types serving different roles:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

The implementation defines three core structures:

| Structure | Role | Address space |
|-----------|------|---------------|
| **POOM** (positional) | V→I mapping | Per-document, mutable |
| **GRAN** (granfilade) | I→content storage | Global, append-only |
| **SPAN** | Span range storage | Auxiliary |

The POOM answers "what is at position N?" by mapping V-addresses to I-addresses. The GRAN answers "what are the actual bytes?" by storing content at I-addresses. These are independent — the POOM changes with every edit, while the GRAN only grows.

## Provenance Requires No Additional Structure

This is the elegant part. To answer "where did the content at V-position 47 originate?", you:

1. Consult the POOM: V-position 47 maps to I-address `1.0.3.0.12.0.1.85`
2. Read the I-address: document `1.0.3.0.12` created this byte

No reverse index, no metadata store, no provenance table. The address IS the provenance:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address is permanent and immutable. Attribution cannot be severed because fetching the content requires knowing the address, and knowing the address means knowing the origin.

## The Reverse Query Needs a Third Structure

There is a third query Nelson specifies that goes beyond both: "What documents contain this content?" — the FINDDOCSCONTAINING operation:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This requires a reverse index from I-addresses to the set of documents whose V-space arrangements reference them. This is neither the POOM (which maps V→I for one document) nor the GRAN (which maps I→content). It is a separate cross-document index — what the EWD series calls DOCISPAN.

## Why Independence Matters

The separation serves Nelson's core architectural principle — **separation of content from arrangement**:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space is ephemeral and per-version. I-space is permanent and global. Fusing them into a single structure would violate this separation:

- **Editing** changes only the V→I mapping (POOM). The content store (GRAN) is untouched.
- **Version creation** creates a new POOM over the same GRAN content.
- **Transclusion** creates a V→I mapping that points to another document's I-addresses — no content is copied.

If both queries required a single unified structure, every edit would need to update provenance information, and transclusion would require duplicating provenance records. By keeping them independent, edits are cheap (update only the POOM) and transclusion is free (the I-address already encodes origin).

## Summary

| Query | Structure | Mutability |
|-------|-----------|------------|
| What is at position N? | POOM (V→I mapping) | Changes with every edit |
| What are the bytes? | GRAN (I→content) | Append-only, never changes |
| Where did this originate? | The I-address itself | Permanent, structural |
| What documents contain this? | Reverse index (DOCISPAN) | Grows with transclusion |

Nelson's answer is unambiguous: these are independent, composable structures. The V→I mapping, the content store, and provenance are three separate concerns that compose through the I-address — the permanent address that simultaneously locates content and identifies its origin.

---

## Question 5 [nelson]

> When new content is inserted into the middle of a document, must the positions of all subsequent content shift by exactly the inserted amount, with no gaps and no overlaps?

### Nelson's Answer

# Yes — INSERT Shifts All Subsequent Positions by Exactly the Inserted Length

Nelson specifies this explicitly in the FEBE protocol definition of INSERT:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

This is not a suggestion or implementation detail — it is the definition of the operation. The shift is **exact** (by the length), **universal** (all following characters), and **immediate** (the addresses *are* increased, not "should be" or "may be").

## No Gaps, No Overlaps

The V-space model guarantees dense, contiguous addressing. Nelson describes V-addresses as positions in a "virtual byte stream":

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

A byte stream is contiguous by definition. If you have 100 bytes, you have V-addresses 1 through 100. After inserting 5 bytes at position 50:

- Positions 1–49 remain unchanged
- Positions 50–54 hold the new content
- Former positions 50–100 become 55–105

No gap at 50 (the new content fills it). No overlap (the shift is exactly 5). The result is still a contiguous stream, now of length 105.

## Why V-Addresses Are Ephemeral

Nelson emphasizes that V-addresses change constantly — this is by design, not a defect:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-addresses shift; I-addresses do not. Links point to I-addresses (permanent content identity), so they survive the V-space rearrangement that INSERT causes:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

## DELETE Is the Mirror Case

DELETE closes the gap rather than opening one. Nelson's V-space model requires that addresses always form a contiguous sequence. Removing a span at positions 50–54 from a 105-byte document shifts positions 55–105 down to become 50–100. The result is again a dense, gapless stream of length 100.

## Summary

The answer is **yes**, and it follows from three properties Nelson specifies:

1. **V-space is a contiguous byte stream** — no gaps permitted [LM 4/11]
2. **INSERT shifts following addresses by exactly the inserted length** — explicitly stated [LM 4/66]
3. **V-addresses are ephemeral by design** — they change with every edit; permanence lives in I-space [LM 4/11, 4/30]

---

## Question 6 [nelson]

> When the same original content appears in multiple documents through transclusion, must the structure allow discovering all the places that content appears without scanning every document?

### Nelson's Answer

# Yes — Structurally Required, Not Just Permitted

Nelson explicitly includes **FINDDOCSCONTAINING** as one of the core FEBE protocol commands, and its semantics demand efficient structural discovery, not brute-force scanning.

## The Command Itself

Nelson specifies:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The phrase "regardless of where the native copies are located" is key — the system must find transclusions across the entire docuverse, not just within one server or one user's documents.

## Why Scanning Is Ruled Out

Nelson's **soft corridor** performance requirement forbids linear-scan approaches:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

If FINDDOCSCONTAINING required scanning every document, its cost would grow linearly with the docuverse. This directly violates the soft corridor.

## The Structural Basis: I-Space Identity

The discovery is made possible by the I-space/V-space separation. Transclusion shares I-addresses — it does not copy content:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Because transclusion preserves I-addresses, content identity is structural. The system can maintain an index from I-addresses to the documents that reference them, enabling efficient reverse lookup without scanning.

## The Enfilade Design Supports This

Nelson credits Barus's "eye in the pyramid" insight as enabling exactly this kind of efficient cross-referencing:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The enfilade data structures are specifically designed so that the relationship between content identity and document arrangement is indexed, not computed by traversal.

## Why This Matters: Three Dependent Guarantees

Several of Nelson's fundamental guarantees depend on efficient content discovery:

1. **Royalties** — The system must know every document delivering a given author's bytes to compute per-byte royalties: "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

2. **Correspondence** — Version comparison works because shared I-addresses identify corresponding parts. SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. This is a specialization of the same structural capability.

3. **Bidirectional discovery** — Nelson requires that readers can find what connects to any content: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46] The phrase "without appreciable delay" rules out scanning.

## Summary

The answer is unambiguous: yes, the architecture **must** support discovering all appearances of content without scanning every document. This is not an implementation optimization — it is a protocol-level command (FINDDOCSCONTAINING), a performance requirement (soft corridor), and a dependency of multiple fundamental guarantees (royalties, correspondence, bidirectional discovery). The I-space/V-space separation and enfilade indexing provide the structural foundation that makes this possible.

---

## Question 7 [nelson]

> When a new version of a document is created, must the structure for the new version share the unchanged portions with the original, or is copying the entire document acceptable?

### Nelson's Answer

## New versions MUST share I-space content with the original. Copying is architecturally unacceptable.

Nelson's design requires this for three independent reasons:

### 1. Correspondence depends on shared I-addresses

The entire version comparison mechanism relies on shared I-space origin. Nelson's SHOWRELATIONOF2VERSIONS operation "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Correspondence is defined as the relationship between V-space positions that map to the *same* I-address. If content were copied (receiving fresh I-addresses), there would be no correspondence to discover — the system couldn't tell which parts match.

Nelson states the dependency explicitly:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

This capability is structurally impossible without shared I-addresses.

### 2. The I-space/V-space separation was designed for exactly this

The entire architecture separates permanent content identity (I-space) from ephemeral document arrangement (V-space). A version is a new V-space arrangement over the same I-space content — that is the *definition* of versioning in this system:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Nelson explicitly rejects the copy model:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

Nelson even names the mechanism: "versioning by inclusion" — creating new versions through transclusion rather than copying.

### 3. Refractive link following requires it

Nelson promises that links made to one version reach through to other versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This works because both versions reference the same I-space bytes. A link to I-address X resolves in any version whose V-space maps some position to X. If versions had independent copies with different I-addresses, refractive following would be impossible.

### The CREATENEWVERSION command

The command description at [LM 4/66] says:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry."

"With the contents" means the new document's V-space maps to the same I-space content — not that content is duplicated. The phrase "its ancestry" confirms the structural relationship is preserved, not severed by copying.

### Summary

Copying would break correspondence (no shared I-addresses to compare), waste storage (violating append-only economics), defeat refractive link following (links couldn't traverse versions), and contradict the fundamental I-space/V-space separation that defines the architecture. A new version is a new V-space arrangement pointing to existing I-space content. That is not an optimization — it is the design.

---

## Question 8 [nelson]

> If a link points to a range within a document, and content is later inserted before that range, must the structure ensure the link's target can still be located at its shifted position?

### Nelson's Answer

# No — Because the Question's Premise Doesn't Apply

The question assumes links target *positions* within a document, which would indeed require tracking shifts. Xanadu's architecture eliminates this problem entirely: **links point to bytes (I-space), not to positions (V-space).**

## The Core Mechanism

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Links attach to content identified by permanent I-space addresses. When content is inserted before a link's target range, only V-space positions shift. The I-space addresses — which the link actually references — are unchanged.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## Why Positions Don't Matter

V-space addresses are ephemeral views over permanent I-space content:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

An insertion changes the V-space mapping (byte at former V-position 5 is now at V-position 12), but the I-space address of that byte never changes. The link still holds the same I-space span. No "shift tracking" is needed because the link never referenced V-space positions in the first place.

## The Survivability Guarantee

Nelson states this explicitly as a design property:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

The only condition for link survival is that *some* bytes remain at each endset. Insertion doesn't remove bytes — it adds new ones. So insertion can never break a link. The structure doesn't "ensure the link's target can still be located at its shifted position" because there is no shifted position to track. The target is the same I-space bytes it always was.

## Summary

| What changes on INSERT | What the link holds | Effect on link |
|---|---|---|
| V-space positions shift | I-space addresses (permanent) | None |
| Document's visual layout changes | Spans of bytes by identity | Unaffected |
| Following content gets new V-addresses | Same content, same I-addresses | Fully intact |

The answer to the question is: the premise dissolves. Xanadu's two-address-space architecture (I-space for identity, V-space for arrangement) means links are structurally immune to insertions, deletions, and rearrangements — by design, not by shift-tracking.

---

## Question 9 [nelson]

> Must the structure preserve its performance guarantees after any sequence of insertions, deletions, and rearrangements, or are there editing patterns that could degrade retrieval?

### Nelson's Answer

This is a precise question that touches the boundary between Nelson's design claims and what he actually proves. Let me examine what Literary Machines says about editing-resilient performance.

## Nelson's Claim: Canonical Order as Invariant

The strongest statement comes from the enfilade description:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. **All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system.**" [LM 1/34]

The phrase "internal mandate" is significant. Nelson presents canonical order not as a best-case property but as a structural invariant — something the system guarantees after *every* operation, regardless of the editing pattern that produced it.

He reinforces this with:

> "the Model T: a data structure that manages huge agglomerates of text and their arrangement in and out of core. With its attendant routines, the Model T enfilade **handles the revision of serial data very quickly and very cleanly.**" [LM 1/33]

## The Soft Corridor: Performance vs. Size, Not vs. History

Nelson's performance guarantee is framed as a function of **system size**, not editing history:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. **(It can't be linear. The system cannot slow down by half as its size doubles.)**" [LM 4/2]

The "soft corridor" diagram shows response time growing logarithmically with size (servers, links, content). Nelson does not present a separate analysis of performance as a function of editing depth or pattern complexity.

## Why the I-Space/V-Space Split Matters Here

The dual address space provides a structural defense against editing-induced degradation:

**I-Space (GRAN enfilade) is immune to editing patterns.** It is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content storage only grows. INSERT appends new bytes; DELETE and REARRANGE don't touch I-space at all. No editing pattern can degrade GRAN retrieval because GRAN never reorganizes.

**V-Space (POOM enfilade) absorbs all editing complexity.** The POOM maps virtual positions to I-space addresses. INSERT shifts following addresses, DELETE closes gaps, REARRANGE transposes regions, COPY adds mappings to existing I-content. Every editing operation modifies the POOM.

The question of editing-pattern degradation therefore reduces to: **can the POOM enfilade become pathologically structured through adversarial editing?**

## What Nelson Does and Does Not Say

Nelson claims the answer is no, through the "canonical order" invariant. But he does not:

1. **Prove** that canonical order implies bounded retrieval time
2. **Analyze** worst-case editing sequences (e.g., alternating insert-at-front and delete-at-back)
3. **Specify** rebalancing or compaction operations
4. **Distinguish** between amortized and worst-case bounds

What he does say is that the enfilade design

> "could conceivably scale up infinitely" [LM 1/36]

and that Barus's "eye in the pyramid" contribution

> "made possible an efficiently ever-linkable enfilade, a whole universe of poly-enfilade structures." [LM 1/34]

The word "efficiently" is doing significant work here without formal backing.

## The Part-Pounce Guarantee

Nelson frames retrieval performance as a user-level guarantee:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet **the system gives you that part instantly, materializing it for you from the many fragments of its actual storage.**" [LM 2/16]

This "part-pounce" is presented as unconditional — it works regardless of how fragmented the document's editing history has made its internal representation. Nelson treats this as a design requirement, not a conditional property.

## The Honest Assessment

Nelson's position is:

1. **The structure preserves canonical order after every operation** — this is an invariant, not a hope
2. **Performance scales logarithmically with size** — the soft corridor
3. **Part-pounce works regardless of history** — unconditional retrieval guarantee

But these are **design claims**, not proofs. Nelson acknowledges the enfilade system's complexity:

> "This is a curious, bizarre, powerful, consistent, non-obvious and hard-to-visualize system. It also has a certain quirkiness and charm. Call it a hack, yes; but it is definitely a superhack." [LM 4/40]

He does not address whether specific editing patterns (e.g., thousands of single-character insertions at random positions, creating extreme POOM fragmentation) could degrade retrieval beyond the soft corridor while still maintaining canonical order. Canonical order is a correctness property; it does not automatically entail a performance bound.

## Summary

Nelson intends the structure to maintain performance guarantees after any editing sequence. The "canonical order" invariant is his mechanism for this — an "internal mandate" that the system remains well-formed after every operation. The append-only I-space is structurally immune to editing degradation; only the POOM (V→I mapping) is exposed to editing patterns.

However, Nelson provides no formal analysis of worst-case editing patterns, no proof that canonical order implies bounded retrieval, and no discussion of rebalancing. The soft corridor analysis addresses growth in *content volume*, not growth in *editing complexity*. Whether adversarial editing patterns can degrade POOM performance while preserving canonical order is a question Nelson's specification leaves open.

NEED_RAW: 1/33-1/38 (raw pages 059-064) — the detailed enfilade description may contain more specific performance claims about editing resilience that the curated summary omits.

---

## Question 10 [nelson]

> If the system crashes partway through updating the structure for an insertion, must the structure be recoverable to a consistent state — either with the insertion fully applied or fully absent?

### Nelson's Answer

# Nelson Does Not Specify Crash Atomicity

**Short answer:** Nelson does not address this question. The requirement that a structure be recoverable to a consistent state after crash is an implementation obligation he leaves entirely unspecified.

## What Nelson DOES Specify

**Append-only storage model** — which inherently provides some crash resilience for content:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

If you only append and never overwrite, a crash during append loses at most the incomplete tail — existing content is structurally safe. But Nelson makes this design choice for *version history* reasons, not for crash recovery reasons.

**Permanence of stored content:**

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This guarantees addresses are never invalidated, but it addresses intentional operations, not crash-induced corruption.

**Canonical order after operations:**

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

This is about the enfilade data structure maintaining its invariants after *completed* operations. It says nothing about incomplete operations interrupted by crash.

## What Nelson Explicitly Disclaims

The most striking evidence is Nelson's software reliability disclaimer:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

This puts crash risk squarely on the user. Nelson does not promise that the system will recover gracefully from failures.

## What Nelson Addresses Instead

Nelson's resilience strategy operates at the **network level**, not the local crash level:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

His answer to failure is **distributed redundancy** — backup copies across servers, content replication, request forwarding — not local crash recovery:

> "Material is moved between servers for a number of purposes: ... 4. for redundancy and backup purposes." [LM 4/71]

## The Gap

Nelson specifies **what** the system must preserve (permanence, addresses, history, links) but not **how** it must behave during partial failure of a single operation. The question "must an interrupted insertion leave the structure either fully applied or fully absent?" falls into this gap.

The closest thing to an answer is the append-only model, which makes content storage inherently crash-safe. But the *structural* updates — the enfilade tree modifications, the V-space mappings, the link indexes — involve non-append operations on tree structures. Whether those must be atomic is an implementation question Nelson does not address.

His design philosophy suggests he was aware of the problem (the "canonical order" mandate for enfilades, the append-only content model, the distributed backup strategy) but treated local crash recovery as an engineering concern below the level of his specification.

---

## Question 11 [gregory]

> When a range query specifies a V-address interval [a, b), does the enfilade guarantee that every bottom crum whose logical span overlaps [a, b) is visited exactly once, or can partial-overlap crums be visited multiple times during traversal?

### Gregory's Answer

## KB Synthesis

## Range Query Traversal: Exactly Once

The KB strongly implies **exactly once** for any bottom crum whose logical span overlaps [a, b), including partial-overlap crums. The argument rests on three structural properties.

### 1. Tree structure guarantees a unique path to each node

The enfilade is a tree, not a DAG. Every bottom crum has exactly one parent, one sibling chain, and one root-to-leaf path. No traversal algorithm operating on a tree can visit the same node via two distinct paths. This applies to both GRAN (1D) and POOM/SPAN (2D) enfilades. [SS-ENFILADE-TREE]

### 2. The sibling walk is strictly linear

For GRAN: `findcbcseqcrum` walks siblings left-to-right via `getrightbro`. [SS-DUAL-ENFILADE, Finding 0041]

For POOM/SPAN: `findcbcinarea2d()` at `retrie.c:229-268` "traverses all siblings at each B-tree level and recursively descends into all qualifying subtrees." [SS-POOM-MULTIMAP, Finding 0039]

In both cases the sibling walk is a linear left-to-right scan — no node appears in the sibling list more than once, so the walk visits each sibling exactly once.

### 3. `incontextlistnd()` accumulates; it does not filter duplicates

The accumulation function "inserts each found context into a sorted linked list, **never replacing existing entries**." [SS-POOM-MULTIMAP, Finding 0039; SS-CONTEXT-LIST, Finding 0078]

This phrasing is about insertion-sort semantics (maintain V-order as you go), not deduplication. Since the traversal visits each node once, no duplicates arise to begin with. If the same bottom crum were somehow presented twice, it would appear twice in the result — the accumulator does not deduplicate. The guarantee of exactly-once visits comes from tree structure and linear sibling walk, not from the accumulator.

### Partial overlap is not a special case

A crum covering [c, d) with c < b and d > a (partial overlap with query [a, b)) is a single node in the tree, reachable via one path, visited once. The traversal decides to descend into it because the widdative summary shows its range intersects the query — but "qualifying" means visited, not visited-multiple-times. The full crum content (including the portion outside [a, b)) is returned to the caller; post-filtering to the exact query interval, if needed, is the caller's responsibility. [SS-INTERVAL-CMP; SS-WHEREONCRUM]

### What could produce apparent duplicates

The KB identifies two sources of multiple results that are **not** multiple visits to the same crum:

- **POOM multimap**: a single I-address can map to multiple V-positions, each stored in a distinct bottom crum. [SS-POOM-MULTIMAP] These are different crums, each visited once.
- **EC-MULTISPAN-LINK-DUPLICATION / EC-PIVOT-LINK-FRAGMENTATION**: link endsets can contain repeated V-spans. This reflects fragmentation of the endset data into multiple sporgls, not multiple visits to the same tree node.

### Summary

| Property | Source |
|----------|--------|
| Unique root-to-leaf path | Tree structure; [SS-ENFILADE-TREE] |
| Linear sibling walk | `findcbcseqcrum`, `findcbcinarea2d`; [SS-DUAL-ENFILADE, SS-POOM-MULTIMAP] |
| Accumulator never re-visits | `incontextlistnd`; [SS-CONTEXT-LIST, INV-RETRIEVAL-TREE-INDEPENDENCE] |

Every bottom crum whose span overlaps [a, b) — whether fully or partially — is visited **exactly once**. The result ordering is V-sorted by [INV-RETRIEVAL-V-SORTED] and independent of tree shape by [INV-RETRIEVAL-TREE-INDEPENDENCE], but the visit count is simply one.

## Code Exploration

Now I have everything I need. Here is the complete analysis.

---

## Enfilade Range Traversal: Exactly-Once Visit Guarantee

**Short answer:** Yes — the enfilade guarantees that every bottom crum whose logical span overlaps `[a, b)` is visited **exactly once**. The tree structure prevents multiple visits; the wisp invariants prevent omissions. One edge case in the `retrieveinspan` wrapper can produce a duplicate entry, but only for queries that extend beyond the document boundary.

---

## Interval Position Constants

`common.h:86-90` establishes the five positions of an address relative to a crum's interval `[left, left+cwid)`:

```c
#define TOMYLEFT       -2   // address < left
#define ONMYLEFTBORDER -1   // address == left
#define THRUME          0   // left < address < right
#define ONMYRIGHTBORDER 1   // address == right
#define TOMYRIGHT       2   // address > right
```

These five values are totally ordered, so `< ONMYRIGHTBORDER` means ≤ THRUME (i.e., address ≤ crum.right), and `> THRUME` means address ≥ crum.right — which expresses half-open interval overlap cleanly as integer comparisons.

---

## Path 1: GRAN Enfilade — `findcbcinspanseq`

The entry point for sequential (1D) range retrieval is `retrieveinspan` → `findcbcinspanseq` [`retrie.c:307-329`]:

```c
int findcbcinspanseq(typecorecrum *crumptr, typewid *offsetptr,
                     tumbler *spanstart, tumbler *spanend, typecontext **headptr)
{
    typewid localoffset;
    movewisp (offsetptr, &localoffset);                          // copy parent's accumulated offset
    for (; crumptr; crumptr = getrightbro (crumptr)) {
        if (!crumintersectsspanseq (crumptr, (tumbler*)&localoffset, spanstart, spanend)) {
            dspadd (&localoffset, &crumptr->cwid, &localoffset, (INT)crumptr->cenftype);
            continue;                                            // advance offset, skip this subtree
        }
        if (crumptr->height == 0) {
            context = makecontextfromcbc ((typecbc*)crumptr, offsetptr);
            oncontextlistseq (headptr, context);                // emit this bottom crum
        } else {
            findcbcinspanseq(findleftson((typecuc*)crumptr), &localoffset, spanstart, spanend, headptr);
        }
        dspadd (&localoffset, &crumptr->cwid, &localoffset, (INT)crumptr->cenftype);
    }
}
```

### Intersection test: `crumintersectsspanseq` [`retrie.c:423-430`]

```c
bool crumintersectsspanseq(typecorecrum *crumptr, tumbler *offsetptr,
                           tumbler *spanstart, tumbler *spanend)
{
    if (iszerotumbler (&crumptr->cwid.dsas[WIDTH]))
        return(FALSE);
    return ((whereoncrum (crumptr, (typewid*)offsetptr, spanstart, WIDTH) < ONMYRIGHTBORDER)
         && (whereoncrum (crumptr, (typewid*)offsetptr, spanend, WIDTH) >/*=*/ ONMYLEFTBORDER));
}
```

The conditions decode to:

- `spanstart < crum.right` (query starts before crum ends) AND  
- `spanend > crum.left` (query ends after crum starts)

This is the exact half-open interval overlap test for `[spanstart, spanend) ∩ [crum.left, crum.right) ≠ ∅`. The comment `>/*=*/` records that the second threshold was tightened from `>=` to `>`: an address exactly at `crum.left` returns `ONMYLEFTBORDER = -1`, and `> -1` (i.e., `>= THRUME = 0`) excludes it. So a query `[a, b)` will NOT pick up a crum that starts at `b`.

### No-duplicate guarantee

`findcbcinspanseq` walks siblings strictly left to right via `getrightbro`. Once a sibling is processed (emitted or recursed into), the loop advances to the next — there is no mechanism to revisit a sibling. Recursion descends only into the **children** of the current upper crum, which are disjoint from the children of any other upper crum by the tree invariant (`leftbroorfather` / `rightbro` / `leftson` in `enf.h:31-49` form an unambiguous tree with no shared nodes).

Furthermore, `enf.h:27` defines `MAXBCINLOAF = 1`. `genf.c:244` enforces this:

```c
return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF
                                              : (is2dcrum(...) ? MAX2DBCINLOAF : MAXBCINLOAF)));
```

A GRAN height-1 upper crum has **at most one** bottom-crum child. So the inner `findcbcinspanseq` call at the leaf level always encounters at most one bottom crum — no sibling ambiguity arises at the bottom level, and the offset passed to `makecontextfromcbc` (`offsetptr`, not `localoffset`) is always correct since `localoffset == offsetptr` for a single-child node.

### Completeness guarantee: `setwidseq` invariant [`wisp.c:150-168`]

```c
bool setwidseq(typecuc *father)
{
    clear (&sum, sizeof (sum));
    for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr))
        widopseq (&sum, &ptr->cwid, &sum);    // sum += child.cwid
    ...
    movewisp (&sum, &father->cwid);           // father.cwid = Σ children.cwid
    return (TRUE);
}
```

Parent width = sum of children's widths. Children at every level **partition** the parent's range without gaps or overlaps. Therefore:

> If a bottom crum's range `[c_left, c_right)` overlaps `[a, b)`, then its parent's range also overlaps `[a, b)` (since parent covers `[..., c_right)`). By induction, every ancestor's range overlaps `[a, b)`. The traversal will not prune any ancestor, and will reach the qualifying bottom crum.

---

## Path 2: SPAN/POOM Enfilade — `findcbcinarea2d`

For 2D range queries (V-address `×` I-address or link endpoints), the path is `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [`retrie.c:229-268`]:

```c
int findcbcinarea2d(typecorecrum *crumptr, typedsp *offsetptr,
                    tumbler *span1start, tumbler *span1end, INT index1,
                    tumbler *span2start, tumbler *span2end, INT index2,
                    typecontext **headptr, typebottomcruminfo *infoptr)
{
    typedsp localoffset;
    for (; crumptr; crumptr = getrightbro (crumptr)) {
        if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                                                  span2start, span2end, index2, infoptr))
            continue;                            // offsetptr NOT accumulated between siblings
        if (crumptr->height != 0) {
            dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
            findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
        } else {
            context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
            incontextlistnd (headptr, context, index1);
        }
    }
}
```

Key structural difference from `findcbcinspanseq`: there is **no offset accumulation across siblings**. For SPAN/POOM each crum carries its own `cdsp` (displacement from parent), so `whereoncrum` inside `crumqualifies2d` computes `left = offsetptr[index] + crum.cdsp[index]` independently for each sibling. The parent's `offsetptr` is used unchanged for every sibling test; only when recursing into children is `offsetptr + crumptr->cdsp` computed as the new base.

`makecontextfromcbc` [`context.c:151-174`] handles this correctly: for non-GRAN crums it adds `cdsp` to the stored offset:

```c
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```

So `context->totaloffset = offsetptr + crum.cdsp` — the correct absolute start of each bottom crum in V/I space, regardless of its position among siblings.

### Qualification test: `crumqualifies2d` [`retrie.c:270-305`]

For span1 (the primary V-address dimension):

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <=/*=*/ ONMYLEFTBORDER)          // span1end ≤ crum.left → no overlap
    return (FALSE);
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME)                       // span1start ≥ crum.right → no overlap
    return (FALSE);
```

`<= ONMYLEFTBORDER` means `endcmp ∈ {TOMYLEFT, ONMYLEFTBORDER}`, i.e., `span1end ≤ crum.left`. The comment `<=/*=*/` records that this was changed from `==` to `<=`. The original `== ONMYLEFTBORDER` alone was insufficient: if `span1end < crum.left` (result = `TOMYLEFT = -2`), the condition `== -1` would not fire and the first dimension test would pass incorrectly. The fix makes the half-open overlap test sound.

**Important boundary asymmetry in span2:** The span2 end-check uses `< ONMYLEFTBORDER` (not `<=`):

```c
if (endcmp < ONMYLEFTBORDER)/* <= was < 12/20/84 */
    return (FALSE);
```

The comment records that `<=` was intentionally changed to `<` on 12/20/84. This means when `span2end == crum.left` (`endcmp == ONMYLEFTBORDER = -1`), the test does **not** exclude the crum. The startcmp check may also fail to exclude it if `span2start < crum.left`. So a crum at `[crum.left, ...)` whose span2 range starts exactly at the query's span2 endpoint `b` may be included. Whether this is a bug or deliberate closed-interval semantics for span2 is not resolved in the code comments.

### Completeness guarantee: `setwispnd` bounding-box invariant [`wisp.c:171-228`]

```c
bool setwispnd(typecuc *father)
{
    // find new upper-left corner: min of children's displacements
    movewisp (&ptr->cdsp, &mindsp);
    for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
        lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, ...);

    // find new lower-right corner: max of (child.cdsp + child.cwid) after renormalization
    for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...);         // renormalize child cdsp
        lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid, ...);
        lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid, ...);
    }
    movewisp (&newdsp, &father->cdsp);   // father covers bounding box of all children
    movewisp (&newwid, &father->cwid);
}
```

Parent's range = **element-wise bounding box** (min start, max end) over all children's ranges. This means:

> If a bottom crum's range overlaps `[a, b)` in dimension `index1`, its parent's bounding box also encompasses it and therefore also overlaps `[a, b)`. By induction, every ancestor overlaps `[a, b)`. No ancestor is pruned by `crumqualifies2d`, and the traversal reaches every qualifying bottom crum.

Unlike the GRAN case, the bounding box does **not** guarantee that every upper crum whose box overlaps `[a, b)` has at least one qualifying child (gaps between siblings in 2D space can produce false positives at upper levels). These false positives cause wasted traversal but never cause a qualifying bottom crum to be missed or emitted twice.

### No-duplicate guarantee

Same argument as for GRAN: `getrightbro` advances strictly left to right; no node in the tree is reachable via two different paths; `findcbcinarea2d` does not revisit siblings.

---

## Edge Case: Potential Duplicate in `retrieveinspan`

`retrieveinspan` [`retrie.c:112-136`] contains:

```c
findcbcinspanseq ((typecorecrum*)fullcrumptr, &offset, spanstart, spanend, &context);
if (tumblercmp (spanend, &fullcrumptr->cwid.dsas[WIDTH]) == GREATER) {
    c = findlastcbcseq ((typecorecrum*)fullcrumptr);
    oncontextlistseq (&context, c);
}
```

If `spanend > document.width` (the query extends past the document boundary), `findlastcbcseq` is called and the **last bottom crum** is appended to the context list. But `findcbcinspanseq` already includes this crum: its range `[L, document.width)` overlaps `[spanstart, spanend)` because `spanend > document.width > L`. The `oncontextlistseq` function [`context.c:113-123`] does no deduplication — it simply appends to a linked list. So the last bottom crum appears **twice** in the returned context when `spanend > document.width`.

This duplication is confined to `retrieveinspan` (GRAN only) and only when the query span extends past the document end. The core traversal functions themselves never produce duplicates.

---

## Summary

| Property | GRAN (`findcbcinspanseq`) | SPAN/POOM (`findcbcinarea2d`) |
|---|---|---|
| Every overlapping bottom crum reached? | **Yes** — by `setwidseq` sum invariant (children partition parent range) | **Yes** — by `setwispnd` bounding-box invariant (every ancestor's box encompasses qualifying children) |
| Any bottom crum visited more than once? | **No** — strict left-to-right tree walk, no shared nodes | **No** — same |
| Boundary semantics (`[a, b)` exclusive end) | Correct: `> ONMYLEFTBORDER` at crum check; `<= ONMYLEFTBORDER` in `crumqualifies2d` span1 | Correct for span1; span2 uses `< ONMYLEFTBORDER` (intentionally treats span2 end as inclusive, changed 12/20/84) |
| Known duplicate case | `retrieveinspan` wrapper: last crum emitted twice when `spanend > document.width` [`retrie.c:123-126`] | None |

The enfilade traversal is a clean bounding-volume hierarchy search. The core invariants — sum-of-widths for GRAN, bounding-box for SPAN/POOM — guarantee that no qualifying bottom crum is unreachable, and the tree structure (one parent per node, `leftbroorfather` / `rightbro` links in `enf.h`) guarantees no crum is reachable by more than one path. Every bottom crum whose logical span overlaps `[a, b)` is visited **exactly once**.

---

## Question 12 [gregory]

> The displacement at each tree level accumulates additively — child grasp equals parent displacement plus child's own displacement. Is additive composition the only algebraic requirement, or must displacements also satisfy cancellation (i.e., if d₁ + d₂ = d₁ + d₃ then d₂ = d₃) for correctness?

### Gregory's Answer

## KB Synthesis

Both additive composition and cancellation are required — they serve distinct purposes, and the implementation silently depends on both.

## Additive Composition (Necessary)

Additive composition is what makes the path-accumulation invariant work [INV-ENFILADE-RELATIVE-ADDRESSING]:

```
absolute_grasp(node) = absolute_grasp(parent) + node.cdsp
```

At retrieval [SS-ENFILADE-TREE Finding 0066], `prologuend` computes `grasp = offset + ptr->cdsp`, where `offset` is the running sum passed down from the root. Without additive composition, this sum would not correctly reconstruct absolute positions.

## Cancellation (Also Necessary)

Cancellation is required for two independent reasons:

**1. `setwispnd` round-trip correctness** [SS-ENFILADE-TREE Finding 0066]:

`setwispnd` finds `mindsp = min(child.cdsp)`, then executes:
- `father.cdsp ← father.cdsp + mindsp`
- `child.cdsp_i ← child.cdsp_i − mindsp` for each child

For this to preserve absolute positions, we need:

```
(father.cdsp + mindsp) + (child.cdsp_i − mindsp) = father.cdsp + child.cdsp_i
```

This reduces to `(child.cdsp_i − mindsp) + mindsp = child.cdsp_i` — i.e., the inverse property `a + (−a) = 0`, which implies (and is implied by) left cancellation.

**2. Uniqueness of tree traversal** [SS-WHEREONCRUM, INV-ENFILADE-RELATIVE-ADDRESSING]:

Tree traversal computes `absolute_grasp = parent_grasp + stored_displacement` and uses this to classify entries via `whereoncrum`. If cancellation failed — meaning two distinct stored displacements `d₂ ≠ d₃` could satisfy `d₁ + d₂ = d₁ + d₃` — then two children with different stored displacements could appear at the same absolute position, making the POOM traversal for INSERT or retrieval non-deterministic.

## The Complication: `strongsub`'s Non-Cancellative Regime

The tumbler arithmetic is **not universally cancellative**. `strongsub` returns `a` unchanged when `b.exp < a.exp` [SS-TUMBLER Finding 0055]:

```
strongsub(a, b) = a   when b.exp < a.exp
```

This means `a − b = a`, so `(a − b) + b = a + b ≠ a` in cross-exponent cases. This is the mechanism that implements subspace isolation for DELETE [FC-SUBSPACE, INT-DELETE-SUBSPACE-ASYMMETRY] — it is intentionally non-cancellative across subspace boundaries.

This does not break `setwispnd` or tree traversal because those operations work within a single subtree where all displacements share the same exponent (same-subspace V-addresses or same-scale I-addresses). The non-cancellative regime is confined to cross-exponent arithmetic that does not arise in intra-level adjustment operations.

## Conclusion

Additive composition is the *structural* requirement: it defines how path sums accumulate. Cancellation is the *algebraic integrity* requirement: it ensures that the adjust-and-rebalance cycle in `setwispnd` is lossless, and that absolute positions uniquely identify relative displacements at each level. The system implicitly relies on both, but the `strongsub` guard intentionally violates cancellation for cross-subspace arithmetic — exploiting the non-cancellative edge case as a design feature rather than treating it as a defect.

## Code Exploration

Now I have everything I need. Let me synthesize the complete answer from the source.

---

## Answer: Cancellation Is Required — and the Code Both Relies on It and Partially Violates It

---

### What the code does with displacements

**`typedsp` is an array of tumblers** — for GRAN, one component (`WIDTH`); for SPAN/POOM, two (`ORGLRANGE`/`SPANRANGE` or `I`/`V`) [wisp.h:10-44]:

```c
struct structwid { tumbler dsas[MAXLOXIZE]; };
typedef struct structwid typewid;
typedef typewid typedsp;
```

**`dspadd` is component-wise `tumbleradd`** [wisp.c:15-18, 269-273]:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
int lockadd(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
    while (loxize--)
        tumbleradd (lock1++, lock2++, lock3++);
}
```

**Grasp = parent offset + child `cdsp`** [retrie.c:334-338]:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    ...
}
```

And `findcbcnd` [retrie.c:219] passes `&grasp` as the `offsetptr` for each child — exactly the additive accumulation described.

**Note: for GRAN, `cdsp` is never stored** (wisp.h line 31-32 comment). The offset is reconstructed by summing sibling widths in `findcbcseq` [retrie.c:195-198]. The displacement question is specific to SPAN/POOM.

---

### The normalization in `setwispnd` requires cancellation

`setwispnd` [wisp.c:171-228] maintains the invariant that the minimum `cdsp` among siblings is zero. When it isn't, it:

1. Promotes the minimum into the parent: `new_parent_cdsp = old_parent_cdsp + mindsp` [wisp.c:200]
2. Subtracts it from every child: `child->cdsp = child->cdsp - mindsp` [wisp.c:211]

```c
// wisp.c:193-211
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr)) {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, ...);
}
if(!lockiszerop){
    dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);
    ...
    dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);
}
```

For every leaf's **absolute position** to be preserved, we need:

```
old_parent_offset + old_parent_cdsp + child_cdsp
  == old_parent_offset + (old_parent_cdsp + mindsp) + (child_cdsp - mindsp)
```

This collapses to requiring `mindsp + (child_cdsp - mindsp) = child_cdsp`, i.e., **left-cancellation**: if you add then subtract the same displacement, you recover the original. Pure additive composition (a monoid) is not sufficient — you also need `d - d` to be the identity and subtraction to be the inverse of addition.

---

### Reparenting in `recombine.c` requires cancellation

`fixdspsofbroschildren` [recombine.c:259-268] performs the same pattern when a node's children are re-homed:

```c
for (nephew = getleftson (bro); nephew; ...) {
    dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);
    dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
}
```

Step 1 computes absolute address `bro->cdsp + nephew->cdsp`. Step 2 subtracts the new parent's `cdsp`. For the leaf to end up at the right absolute position, we need `(a + b) - a = b` — i.e., subtraction undoes addition. This is cancellation.

The same pattern appears in `takenephewnd` [recombine.c:243-248].

---

### Whether tumbler arithmetic actually satisfies cancellation

**In general: No.**

`absadd` [tumble.c:444-485] has an `else` branch for when `bptr->exp > aptr->exp` (b starts at a *shallower* level in the hierarchy than a):

```c
} else {
    answer.exp = bptr->exp;
    temp = bptr->exp - aptr->exp;
    while (i <= temp) {
        ansmant[j++] = bmant[i++];  // copy b's digits only
    }
}
while ( j <= NPLACES -1 ) {    
    ansmant[j++] = bmant[i++];     // ...then more b's digits
}
```

**`a` is never used at all.** The result is just `b`. So when `b` is at a shallower hierarchical level than `a`, `a + b = b` regardless of `a`. This directly breaks cancellation: for any three tumblers where `b` is shallower than `a1` and `a2`, we get `a1 + b = b = a2 + b`, but `a1 ≠ a2`.

**`strongsub`** [tumble.c:534-565] has the symmetric pathology for subtraction:

```c
if (bptr->exp < aptr->exp) {   // b is deeper (finer-grained) than a
    movetumbler(aptr,cptr);
    return(0);                  // return a unchanged: a - b = a
}
```

So if `b` is at a finer hierarchical level than `a`, `a - b = a`, regardless of `b`.

---

### Why the code survives despite non-cancellative arithmetic

The code implicitly operates within a **restricted domain**: all displacements stored in `cdsp` are addresses within the same "story" of the tumbler hierarchy — they are offsets of the form set in `insertcbcnd` [insertnd.c:263]:

```c
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```

Both `origin` and `grasp` are computed from the same root by accumulating displacements at the same level. Their difference is a same-level relative offset, meaning `origin.exp ≈ grasp.exp`. Under the **same-level condition** (`a.exp == b.exp`), `absadd` reduces to its first branch (straightforward digit addition) and `strongsub` computes a proper difference. Within this domain, tumbler arithmetic is effectively standard integer arithmetic, which is fully cancellative.

This invariant is not enforced algebraically by the tumbler type — it is preserved implicitly by how the system creates and normalizes displacements.

---

### Answer to the posed question

**Cancellation is a necessary requirement** for the enfilade to be correct. Additive composition alone (a monoid) is insufficient:

1. **`setwispnd`** [wisp.c:193-228] requires `mindsp + (d - mindsp) = d` to hold for every child displacement `d` — the normalization step preserves absolute positions only if subtraction inverts addition.

2. **`fixdspsofbroschildren` and `takenephewnd`** [recombine.c:264-265, 243-248] require `(a + b) - a = b` for the re-homed children to land at the correct absolute addresses.

3. Tumbler arithmetic is **not generally cancellative**: `absadd` returns `b` outright when `b` is shallower than `a` [tumble.c:467-482], and `strongsub` returns `a` unchanged when `b` is at a finer level [tumble.c:544-547]. Both operations fail the cancellation law for arbitrary inputs.

4. The code is correct **because it never forms such degenerate sums in practice**. The operational domain restricts displacements to same-level tumblers, within which `absadd` and `strongsub` behave as ordinary integers and cancellation holds. But this is a **semantic invariant, not an algebraic one** — the tumbler type does not enforce it, and there is no assertion anywhere that `displacement.exp` values must agree across siblings.

In summary: additive composition is the visible mechanism; cancellation is the hidden requirement; the code satisfies it by construction (same-level displacements) rather than by type safety.

---

## Question 13 [gregory]

> In the 2D enfilade (POOM, spanfilade), the root displacement tracks the minimum child address via `setwispnd`. Is the invariant that root displacement equals the componentwise minimum of all descendant displacements, or is it the minimum of direct children only?

### Gregory's Answer

## KB Synthesis

The invariant is that `root.cdsp` equals the **minimum absolute address across all descendants** in the subtree — not just direct children. However, this global property is maintained by `setwispnd` operating on **direct children only** at each level, with bottom-up propagation doing the rest.

## The Mechanism

From [INV-ENFILADE-RELATIVE-ADDRESSING] and [SS-ENFILADE-TREE] Finding 0066, `setwispnd` at any node performs three steps:

1. Compute `mindsp = min(direct_children.cdsp)` — direct children only
2. Absorb: `node.cdsp += mindsp`
3. Make children relative: `child.cdsp -= mindsp` for each child

After this operation, the **local post-condition** is:

```
min(node.direct_children.cdsp) == 0
```

The child with the minimum displacement is now at relative offset 0. This means `node.cdsp` equals the absolute address of that minimum child's subtree start.

## Why the Global Invariant Holds

`setwispupwards` applies `setwispnd` bottom-up from the modification point to the root. By the time `setwispnd` is called at an internal node N, its children have **already been processed**. Each child's `cdsp` already encodes the minimum of that child's own subtree (relative to the child's position). So when N finds `min(direct_children.cdsp)`, it finds the minimum of the subtree minimums — which is the global minimum of N's entire subtree.

Tracing through a 3-level example:

```
Before setwispupwards (absolute addresses in brackets):
  Root: cdsp = 0
  ├── Node A: cdsp = 5  → subtree minimum is 5
  │   ├── Crum1: cdsp = 0  [abs 5]
  │   └── Crum2: cdsp = 2  [abs 7]
  └── Node B: cdsp = 3  → subtree minimum is 3
      ├── Crum3: cdsp = 0  [abs 3]
      └── Crum4: cdsp = 1  [abs 4]

After setwispnd(A): min(0,2)=0 → no change
After setwispnd(B): min(0,1)=0 → no change
After setwispnd(Root): min(5,3)=3 → root.cdsp=3, A.cdsp=2, B.cdsp=0
```

Result: `root.cdsp = 3` = the global minimum (Crum3 at absolute address 3).

## The Two-Level Invariant

- **Per-node**: after `setwispnd(N)`, `min(N.direct_children.cdsp) == 0`
- **Whole-tree consequence**: `root.cdsp` = minimum absolute address among all descendants

[SS-ENFILADE-TREE] Finding 0066 states this explicitly: "For 2D enfilades, `root.cdsp` and `root.cwid` together form a bounding box: `root.cdsp` is the upper-left corner (minimum address)." The retrieval path at `retrie.c:337` computes `grasp = offset + ptr->cdsp` where `offset` accumulates ancestor contributions — which works precisely because each node's `cdsp` is the minimum of its subtree relative to ancestors, not just the minimum of direct children in isolation.

## Summary

`setwispnd` uses **direct children only** as its operand, but the invariant it establishes is **all-descendant minimum**. The two are equivalent due to bottom-up application: children's `cdsp` values already encode their respective subtree minimums, so finding the minimum of direct children is equivalent to finding the global minimum of the subtree.

## Code Exploration

I now have all the evidence I need. Here is the full answer:

---

## The `setwispnd` Displacement Invariant

### Short Answer

**The code in `setwispnd` takes the minimum of direct children only.** However, because `setwispupwards` always applies this bottom-up, the invariant that actually holds throughout the tree is the componentwise minimum of **all descendants** — not just direct children. The two formulations are equivalent only when children's displacements are themselves already normalized.

---

### Code Walk-Through

#### `setwispnd` — the core operation (`wisp.c:171–228`)

```c
bool setwispnd(typecuc *father)
{
  typecorecrum *ptr;
  typedsp newdsp, mindsp;
  ...
  /* find new upper-left corner */
  movewisp (&ptr->cdsp, &mindsp);
  for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr)) {
      lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp,
               (unsigned)dspsize(ptr->cenftype));     // ← min over DIRECT CHILDREN only
  }
```

Lines 193–196 iterate exactly one level deep — `findleftson → getrightbro` — collecting the componentwise minimum of `ptr->cdsp` across **direct children only**. There is no recursive descent into grandchildren.

The function then applies two consequences of having found that minimum:

1. **Father absorbs it** (`wisp.c:200, 224`):
   ```c
   dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);
   // ...
   movewisp (&newdsp, &father->cdsp);
   ```
   `father->cdsp ← father->cdsp + mindsp`

2. **Children are re-normalized** (`wisp.c:211`):
   ```c
   dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);
   ```
   Every child's displacement is reduced by `mindsp`, so the minimum child's displacement becomes the zero tumbler.

**Local post-condition after `setwispnd`:** `min_i(child_i.cdsp) = 0`. At least one child has displacement zero; all others have non-negative relative displacement.

---

#### How this achieves the global all-descendants invariant

`setwispnd` is never called in isolation. The caller is always `setwispupwards` (`wisp.c:83–111`):

```c
int setwispupwards(typecuc *ptr, INT testflag)
{
  ...
  for (changed = TRUE; changed && ptr; ptr = father) {
      father = findfather ((typecorecrum*)ptr);
      changed = setwisp ((typecorecrum*)ptr);   // → setwispnd for POOM/SPAN
  }
}
```

This walks strictly **upward** from a starting node. Because insertions always call `setwispupwards` starting from the subtree that changed (e.g. `insertnd.c:56–64`), the tree is processed **bottom-up**: lower levels are normalized before higher levels see them.

**Inductive argument:**

Say the tree has three levels: root (fullcrum), level-1 internal nodes, leaves.

After `setwispnd` runs on each level-1 node:
- `level1_i.cdsp = level1_i_original + min(leaf addresses under it)` (in root frame)
- Every leaf under `level1_i` has its `cdsp` reduced by that leaf-minimum.

When `setwispnd` runs on root:
- It scans direct children: `level1_1.cdsp`, `level1_2.cdsp`, …
- Each `level1_i.cdsp` is already the minimum absolute address of all leaves in its subtree.
- So `min_i(level1_i.cdsp)` = the **global minimum** over all leaves.
- Root absorbs it: `root.cdsp ← root.cdsp + global_min`.

**The accumulated displacement from root to any leaf** (via `prologuend`, `retrie.c:334–339`):
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);  // grasp = offset + cdsp
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```
`grasp = accumulated_offset + node.cdsp`. The minimum possible `grasp` at any level is achieved by the child whose `cdsp = 0` (the one that was normalized to zero). Following the zero-cdsp path from root to leaf gives the minimum leaf address = `root.cdsp`.

---

### The Precise Statement of the Invariant

There are two equivalent but distinct ways to state what the code enforces:

| Formulation | Scope | Where enforced |
|---|---|---|
| **Local**: `min_i(child_i.cdsp) = 0` | At every internal node | `wisp.c:193–215` directly |
| **Global**: `node.cdsp` (in parent frame) = min accumulated address of all leaves in subtree | Across the whole tree | Emergent from bottom-up application of the local invariant |

The code mechanically implements the **local** (direct-children) formulation. The **global** (all-descendants) formulation is the invariant that holds in practice, but only because `setwispupwards` always processes levels from bottom to top.

If you were to call `setwispnd` on a node whose children had stale (un-normalized) `cdsp` values, you would get only the minimum of the direct children's stale values — not the true minimum of all descendants. The kluge comment in `insertnd.c:32`:

```c
/**/fixincoresubtreewids(fullcrumptr);/*1999 // a temp kluge zzz till we find
  where setwisp isnt called// this is a brute force kluge, if this fixes anything
  it means that the wids aren't being set properly somplace else probably near here */
```

and the commented-out call to `fixincoresubtreewids` (which recursively descends and calls `setwisp` on every node, `recombine.c:321–334`) confirm that the developers understood this dependency: if bottom-up order is broken, the all-descendants invariant can fail, which is why the "brute force" full-tree re-normalization exists as a debugging fallback.

---

### Summary

- **`setwispnd` looks at direct children only** (`wisp.c:193–196`).
- **The invariant it enforces** (after bottom-up application via `setwispupwards`) **is** that every node's `cdsp` equals the componentwise minimum of all descendant absolute addresses in its subtree.
- The two formulations are equivalent precisely because each child's `cdsp` already encodes the minimum of its own subtree before the parent's `setwispnd` runs.
- The local post-condition is `min_i(child_i.cdsp) = 0_tumbler` at every internal node.

---

## Question 14 [gregory]

> Does the system require that a range query on an interval entirely outside the enfilade's populated region return empty in O(1), or is it acceptable for the traversal to walk down to a leaf before determining emptiness?

### Gregory's Answer

## KB Synthesis

This question is not fully answerable from the KB. Here is what the KB does and does not say.

## What the KB documents

**Per-node bounding boxes exist.** Each 2D enfilade node (POOM, SPAN) carries `cdsp` (minimum address across all descendants) and `cwid` (total extent). The root's `cdsp` therefore equals the minimum address in the entire populated region, and `cdsp + cwid` is the maximum. [SS-ENFILADE-TREE, Finding 0066]

**A five-way classifier exists.** `whereoncrum()` classifies an address relative to a node's `[grasp, reach)` interval, returning `TOMYLEFT` (-2) or `TOMYRIGHT` (+2) when the address is entirely outside. `intervalcmp()` provides the same five-way result for general intervals. [SS-WHEREONCRUM], [SS-INTERVAL-CMP]

**The traversal filters by "qualifying subtrees."** `findcbcinarea2d()` is described as recursively descending into "all qualifying subtrees" and iterating siblings. [SS-CONTEXT-LIST, Finding 0078]

**For 1D (GRAN) enfilades**, root displacement is always zero; the root's extent covers `[0, total_bytes)`. [SS-ENFILADE-TREE, Finding 0066]

## What the KB does not say

No Finding explicitly describes what happens in `findcbcinarea2d` when the query range is entirely disjoint from the root's bounding box. The KB gives the data structure (bounding boxes at every node, five-way classifier) and the traversal description ("qualifying subtrees"), but no Finding traces the traversal path for a fully out-of-range query or gives a complexity bound for that case.

The structure *implies* O(1) root-level rejection for a query falling entirely outside `[root.cdsp, root.cdsp + root.cwid)`, because `whereoncrum` on the root would return `TOMYLEFT` or `TOMYRIGHT` before any child is examined. But whether `findcbcinarea2d` actually checks the root this way before descending — rather than walking siblings at height H, then H-1, etc. — is not confirmed by any Finding in the KB.

The only structurally confirmed O(1) early exit is in `makegappm` during INSERT: when the insertion point is at or beyond a crum's reach, the function returns immediately (`retrie.c:345-372`, `insertnd.c:137-143`). That is a different code path from read queries. [SS-WHEREONCRUM], [PRE-INSERT]

**Bottom line:** The KB documents sufficient structure for a root-level O(1) rejection to be *possible*, but does not confirm whether the retrieval traversal (`retrieverestricted`, `findcbcinarea2d`) takes that early exit or walks down to a leaf first.

## Code Exploration

Now I have the full picture. Let me write the complete answer.

---

## Answer: Range Query Complexity for Out-of-Range Intervals

**Short answer:** It depends on enfilade type and query path. SPAN/POOM enfilades return in O(1). GRAN enfilades do *not* — they walk to a leaf.

---

### Constants

From `common.h:86–90`:

```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER 1
#define TOMYRIGHT       2
```

These are ordered, so `< ONMYLEFTBORDER` means *strictly to the left*, and `> THRUME` means *at or past the right border*.

---

### SPAN / POOM Enfilades — O(1) at Root

#### Point retrieval: `findcbcnd` [`retrie.c:208–227`]

The very first thing it does is check the current node's range:

```c
// retrie.c:215
if ((cmp = whereoncrum (father, offsetptr, address, index)) < ONMYLEFTBORDER || cmp > THRUME )
        return (NULL);
```

Called at the root with `father = fullcrumptr`. If the address is to the right of the root's range (`> THRUME`, i.e. ONMYRIGHTBORDER or TOMYRIGHT), it returns NULL immediately without descending. O(1).

#### Range retrieval: `findcbcinarea2d` [`retrie.c:229–268`]

The outer loop starts at the root (the apex):

```c
// retrie.c:252–255
for (; crumptr; crumptr = getrightbro (crumptr)) {
        if (!crumqualifies2d (crumptr, offsetptr, ...)){
                continue;
        }
        // only descends if crumqualifies2d returned TRUE
```

`crumqualifies2d` [`retrie.c:270–305`] checks both span dimensions. For dimension 1:

```c
// retrie.c:282–289
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER){
        return(FALSE);   // query ends before crum starts
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME /*&& endcmp > THRUME*/)){
        return (FALSE);  // query starts after crum ends
}
```

For an interval entirely to the right of the root's range, `startcmp` is TOMYRIGHT (2), which is `> THRUME` (0) → `crumqualifies2d` returns FALSE → the loop body hits `continue`. The root has no siblings (`getrightbro` returns NULL), so the loop exits immediately. **O(1) — no descent.**

For an interval entirely to the left, `endcmp` is TOMYLEFT (-2) ≤ ONMYLEFTBORDER (-1) → same early exit. **Also O(1).**

---

### GRAN Enfilades — O(log n) for Queries Past the End

The FEBE `retrieve` operation calls:

```
doretrievev → ispanset2vstuffset → ispan2vstuffset [granf2.c:286–318]
                                       → retrieveinspan [retrie.c:112–136]
```

`retrieveinspan` for GRAN [`retrie.c:112–136`]:

```c
case GRAN:
        findcbcinspanseq ((typecorecrum*)fullcrumptr, &offset, spanstart, spanend, &context);
        if (tumblercmp (spanend, &fullcrumptr->cwid.dsas[WIDTH]) == GREATER) {
                c = findlastcbcseq ((typecorecrum*)fullcrumptr);     // [retrie.c:124]
                oncontextlistseq (&context, c);
        }
        return (context);
```

**Step 1 — primary search:** `findcbcinspanseq` uses `crumintersectsspanseq` [`retrie.c:423–430`] to check each node. For a query span entirely to the right of the enfilade's content:

```c
// retrie.c:428–429
return ((whereoncrum (crumptr, (typewid*)offsetptr, spanstart, WIDTH) < ONMYRIGHTBORDER)
         && (whereoncrum (crumptr, (typewid*)offsetptr, spanend, WIDTH) > ONMYLEFTBORDER));
```

If `spanstart > root.cwid.WIDTH`, `whereoncrum` returns TOMYRIGHT (2); `2 < ONMYRIGHTBORDER (1)` is false → the root doesn't intersect → loop exits. No contexts are found. So far O(1).

**Step 2 — secondary path:** But then the condition at `retrie.c:123`:

```c
if (tumblercmp (spanend, &fullcrumptr->cwid.dsas[WIDTH]) == GREATER) {
```

For a query span entirely to the right, `spanend > fullcrumptr->cwid.dsas[WIDTH]` is **TRUE**. This triggers `findlastcbcseq` [`retrie.c:138–158`]:

```c
typecontext *findlastcbcseq(typecorecrum *fullcrumptr) {
  typecorecrum *ptr, *findleftson();
  ...
        tumblerclear (&offset);
        for (ptr = fullcrumptr; ptr; ptr = findleftson((typecuc*)ptr)) {
                for (; getrightbro (ptr); ptr = ptr->rightbro)
                        tumbleradd (&offset, &ptr->cwid.dsas[WIDTH], &offset);
                if (ptr->height == 0) {
                        c = makecontextfromcbc ((typecbc*)ptr, (typewid*)&offset);
                        return(c);
                }
        }
```

This descends from the root all the way to the rightmost leaf, one level at a time. It traverses `height` levels, following `findleftson` at each level and then seeking the rightmost sibling. **This is O(log n)** — it walks down to a leaf before the system can conclude that the query region is empty.

The context it returns (the rightmost leaf) is then processed by `context2vtext` [`context.c:277–309`], which clips the leaf's address range against the query span. For a query entirely past the enfilade, the intersection is empty and `length` computes to zero (returning FALSE at `context.c:261`). The user gets an empty result — but only *after* a full O(log n) tree walk.

---

### Exception: `fetchorglgr` has an explicit O(1) guard

`fetchorglgr` in `granf2.c:31–32` — the GRAN document-lookup path — adds its own bounds check before calling `retrievecrums`:

```c
// granf2.c:31–32
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
        return (NULL);
```

This special-cases the point lookup: if `address > total_width`, it returns NULL in O(1). But this guard is **not** present in the general `retrievecrums` / `findcbcseqcrum` path [`retrie.c:167–189`], which always descends to a leaf regardless of whether the address is in range.

---

### Summary

| Enfilade type | Query path | Out-of-range behavior |
|---|---|---|
| SPAN/POOM | `findcbcnd` (point) | **O(1)** — guard at `retrie.c:215` prunes at root |
| SPAN/POOM | `findcbcinarea2d` (range) | **O(1)** — `crumqualifies2d` at root returns false, `retrie.c:253` |
| GRAN | `findcbcinspanseq` (range) | **O(1)** for primary search, but **O(log n)** for secondary `findlastcbcseq` call when `spanend > cwid` (`retrie.c:123–126`) |
| GRAN | `fetchorglgr` (point) | **O(1)** — explicit guard `granf2.c:31–32`, but only for `LESS` (strictly less) |
| GRAN | `retrievecrums`/`findcbcseqcrum` | **O(log n)** — always descends, no guard |

The system **does not uniformly guarantee O(1) for out-of-range queries**. The SPAN/POOM 2D enfilades achieve it at the root through `crumqualifies2d`. The GRAN enfilade's `retrieveinspan` does *not*: it falls into a secondary `findlastcbcseq` path that walks all the way to the rightmost leaf whenever `spanend` exceeds the enfilade's total width — which is true for any query interval entirely to the right of the populated region.

---

## Question 15 [gregory]

> When `recombinend` sorts children by the diagonal sum of their two displacement coordinates, does correctness require that this diagonal ordering be a total order on children, or would any ordering that groups spatially adjacent children together suffice for rebalancing?

### Gregory's Answer

## KB Synthesis

The diagonal ordering is **not strictly required for correctness** of the saturation postcondition. Any total order on children would suffice — and even a weaker property (grouping spatially adjacent children) is more than necessary. Here is the reasoning from the KB:

## What correctness actually requires

The postcondition of `recombinend` [ST-REBALANCE-2D, Finding 0071] is a saturation property:

> After `recombinend`, no pair of children in the node can be merged without exceeding `max_children`.

Formally: `∀ i,j ∈ children(node): i ≠ j ⟹ ¬ishouldbother(i,j)`

This invariant is achieved by the all-pairs structure of the algorithm: the outer loop iterates over all positions `i`, and the inner loop (which deliberately does **not** break after a successful merge [ST-REBALANCE-2D, Finding 0073]) iterates over all `j > i`. Every pair `(i,j)` with `i < j` in sorted order is examined at least once. If mergeable, the merge occurs; NULL-marking prevents double-counting of depleted donors.

This exhaustive O(n²) pair examination is the mechanism that guarantees saturation — not the specific ordering.

## Why any total order suffices

Given the exhaustive examination structure, any total order on children would preserve correctness:

- Every pair `(i,j)` is still considered (outer loop reaches every non-NULL position; inner loop covers all higher positions)
- `ishouldbother` checks combined son count and reserved status — these are properties of the nodes themselves, not of their ordering
- NULL-marking correctly tracks depletion under any ordering

The ordering only determines **which node becomes receiver vs donor** for a given pair, not whether the pair is examined. Since `ishouldbother` is symmetric in terms of the capacity check (`dest.sons + src.sons ≤ limit`), swapping receiver and donor roles doesn't change whether a merge is possible — only which node absorbs which.

## What the diagonal ordering actually provides

[ST-REBALANCE-2D, Finding 0071] describes the diagonal key as `cdsp.dsas[0] + cdsp.dsas[1]` (L1-norm), and the source comment explicitly calls it "the compare crums diagonally hack" — signaling this is a heuristic, not a theorem.

The diagonal provides **spatial locality**: children with nearby L1-norm positions in 2D address space are sorted adjacent, making it more likely that adjacent children in the sorted array are spatially proximate and thus candidates for productive merges. This is a performance heuristic that reduces wasted `ishouldbother` evaluations but is not required for the saturation invariant.

## Structural evidence from the asymmetry

[ST-SPLIT-2D] provides the clearest evidence against a strict correctness requirement: the SPAN enfilade uses diagonal ordering for **both** split and rebalance (a consistent basis), while the POOM enfilade uses diagonal for rebalance but **SPANRANGE-only** (single dimension) for split. If diagonal ordering were a correctness requirement — say, to maintain some invariant relating split points to merge candidates — both operations on the same enfilade type would need to use the same ordering. The asymmetry confirms the diagonal is an independent heuristic choice for each operation.

## Summary

The saturation postcondition requires only that all pairs are examined and merges occur when possible. The diagonal total order satisfies this requirement, but so would any total order, and even a partial order that groups spatially adjacent children would be more than sufficient. The code comment ("hack") and the cross-operation asymmetry [ST-SPLIT-2D] both confirm the diagonal is an engineering pragmatism for spatial locality, not a correctness invariant of the rebalancing algorithm.

## Code Exploration

Now I have everything I need. Let me synthesize the full answer from the source.

---

## Answer

### The short answer

Correctness does **not** require the diagonal ordering to be a total order. For the SPAN and POOM enfilades that `recombinend` operates on, retrieval is address-interval–based per child, not left-to-right accumulative. Any ordering that selects which node absorbs which suffices to produce a valid tree. The diagonal sort is explicitly labeled a "hack" in the code and serves as a proximity heuristic, not a structural invariant.

---

### What `recombinend` actually does

`recombinend` [recombine.c:104–131] is called only for SPAN and POOM enfilades (the `recombine` dispatch at recombine.c:22–34 sends GRAN to `recombineseq`). It:

1. Recurses into children [recombine.c:114–116]
2. Calls `getorderedsons` to get a sorted child array [recombine.c:118]
3. Runs a nested loop over all `(i, j)` pairs with `i < j`, calling `takeovernephewsnd` whenever `ishouldbother` returns true [recombine.c:120–128]

The nested loop has both `break` statements commented out:
```c
/*break;*/
/*break;//zzz6/16/84 reg//*/
```
[recombine.c:124–125]

That means **all pairs are tried**, not just adjacent ones. Whatever the sort order, the loop visits every combination.

---

### How the sort key is computed

`getorderedsons` [recombine.c:270–280] collects children and passes them to `shellsort`. Inside `shellsort` [recombine.c:296–299]:
```c
for(i=0;i<n;i++){/* build up a list of sumps of disp[0] and dsp[1]*/
               /* for compare crums diagonally hack */
    tumbleradd(&v[i]->cdsp.dsas[0],&v[i]->cdsp.dsas[1],&tarray[i]);
    tarrayp[i] = &tarray[i];
}
```
The sort key is `cdsp.dsas[0] + cdsp.dsas[1]`. For POOM crums, `wisp.h` defines `dsas[I=0]` as the i-stream displacement and `dsas[V=1]` as the v-stream displacement [wisp.h:19–21]. For SPAN, `dsas[ORGLRANGE=0]` and `dsas[SPANRANGE=1]` [wisp.h:15–16]. The sum is computed with `tumbleradd` and compared with `tumblercmp` [tumble.c:72–85], which is a total order on tumblers (it compares sign, then `exp`, then mantissa lexicographically).

The word **"hack"** appears in the comment inline at recombine.c:297 — the author knew this was a pragmatic approximation.

---

### Why retrieval does not require child ordering in 2D enfilades

The critical contrast is between granfilade and spanfilade/poomfilade retrieval.

**Granfilade** (`findcbcseq` [retrie.c:191–206]) accumulates an offset as it scans:
```c
for (; getrightbro (ptr); ptr = ptr->rightbro) {
    if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
        break;
    dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);
}
```
The scan is left-to-right only and never backtracks. **Children must be in sorted order** or it will skip the right one.

**2D retrieval** (`findcbcnd` [retrie.c:208–227]) works differently:
```c
prologuend (father, offsetptr, &grasp, (typedsp*)NULL);
for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
    if (retr = findcbcnd (ptr, &grasp, address, index))
        break;
```
`prologuend` computes `grasp = offsetptr + father->cdsp` [retrie.c:334–339] once, and passes the **same** `grasp` to every child iteration. Each child's `whereoncrum` [retrie.c:345–398] independently checks `[grasp + child->cdsp, grasp + child->cdsp + child->cwid)` against the query address. There is no offset accumulation across siblings. The scan finds the first child whose absolute interval contains the address, regardless of sibling order.

`findcbcinarea2d` [retrie.c:229–268] likewise iterates all children with `crumqualifies2d`, checking each child's individual `cdsp` and `cwid` — no ordering assumption.

---

### Why the merge itself does not require ordering

`eatbrossubtreend` [recombine.c:205–233] performs the actual tree restructuring:
```c
makeroomonleftnd (me, &offset, &bro->cdsp, &grasp);
fixdspsofbroschildren (me, bro);
getleftson (bro)->leftbroorfather = getrightmostbro (getleftson (me));
getrightmostbro (getleftson (me))->rightbro = getleftson (bro);
```

`makeroomonleftnd` [makeroom.c:13–49] expands `me`'s bounding box leftward (per dimension) to cover `bro->cdsp` if needed. It does this correctly for any relative position of `bro` vs `me`:
```c
if (tumblercmp (&origin->dsas[i], &grasp->dsas[i]) == LESS) {
    tumblersub (&grasp->dsas[i], &origin->dsas[i], &base);
    tumblersub(&origin->dsas[i],&offset->dsas[i],&newdsp.dsas[i]);
    expandcrumleftward ((typecorecrum*)father, &newdsp.dsas[i], &base, i);
    prologuend ((typecorecrum*)father, offset, grasp, (typedsp*)NULL);
}
```
If `bro->cdsp < me->cdsp` in some dimension (i.e., the sort put `me` first even though `bro` is geometrically to the left), `expandcrumleftward` [makeroom.c:52–74] shifts `me->cdsp`, grows `me->cwid`, and adjusts all existing children's `cdsp` values to compensate. The operation is fully correct for any relative ordering.

`fixdspsofbroschildren` [recombine.c:259–268] re-expresses each of `bro`'s children's displacements relative to `me`'s (possibly new) position:
```c
for (nephew = getleftson (bro); nephew; nephew =(typecorecrum *)getrightbro (nephew)){
    dspadd (&bro->cdsp,&nephew->cdsp, &nephew->cdsp, me->cenftype);
    dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
    ivemodified(nephew);
}
```
This is a pure coordinate transformation that is correct regardless of which node absorbed which.

After the merge, `bro`'s children are appended to the right of `me`'s children. Since 2D retrieval uses absolute per-child intervals and scans all siblings, the appended order is irrelevant to correctness.

---

### What the diagonal sort actually provides (heuristics only)

The sort provides three practical benefits that are not correctness requirements:

1. **Proximity heuristic**: Nodes with smaller diagonal sums are closer to the enfilade origin in combined address space. Merging `sons[i]` (smaller) with `sons[j]` (larger, `j > i`) tends to merge geometrically adjacent nodes, preserving tree locality.

2. **Partial-merge quality**: When `takeovernephewsnd` can only partially absorb `bro` (because `me` fills up), it calls `getorderedsons(bro, sons)` [recombine.c:184] and migrates `sons[0], sons[1],...` in diagonal order. Transferring smaller-diagonal children first keeps natural address ordering among remaining siblings.

3. **Determinism**: Without the sort, the order of merges would depend on the arbitrary left-to-right linked-list order of children, which is less predictable.

None of these are required by the tree invariants or the retrieval algorithm.

---

### Why a "grouping" ordering would also suffice

The question asks whether any ordering that "groups spatially adjacent children together" would be sufficient. The answer from the code is **yes**, and in fact even stronger: any ordering at all would produce a correct tree, because:

- `findcbcnd` and `findcbcinarea2d` scan all children and test absolute `cdsp` intervals — no ordering invariant is consulted.
- `makeroomonleftnd` handles all geometric cases regardless of which node is `me` and which is `bro`.
- `fixdspsofbroschildren` performs a dimension-wise coordinate transformation that is correct for any relative position.

The total-order property of `tumblercmp` over diagonal sums is used to make `shellsort` well-defined, but it could be replaced by any consistent ordering (random shuffle, row-major order, etc.) without breaking the tree.

---

### Contrast with granfilade

`recombineseq` [recombine.c:38–68] calls `eatbrossubtreeseq` and `takeovernephewsseq`, which assume sibling-list order corresponds to address order (because `findcbcseq` accumulates offsets left-to-right and never backtracks). For that code path a stable address ordering is a true invariant. But `recombinend` is a separate path for 2D enfilades with fundamentally different retrieval semantics, and no such ordering invariant exists there.

---

## Question 16 [gregory]

> The granfilade uses `MAXBCINLOAF=1` (one entry per bottom crum), while the POOM uses `MAX2DBCINLOAF=4`. Is the essential property that bottom crum occupancy is bounded above, or does the POOM also require a minimum occupancy guarantee (e.g., at least 2 entries after a split)?

### Gregory's Answer

## KB Synthesis

The answer differs by enfilade type, and the short version is: **the upper bound is the essential property; the minimum occupancy guarantee is only `sons ≥ 1` for both types, not `sons ≥ ⌈M/2⌉` or any stronger claim.**

---

## GRAN (M_b = 1): point constraint, not a range

For the granfilade, the upper and lower bounds collapse to the same value. `MAXBCINLOAF = 1` means:
- `toomanysons` triggers at > 1 (any overflow)
- `toofewsons` triggers at < 1 (empty, which is Bug 0019)
- Valid occupancy is exactly `sons = 1`

[SS-GRAN-BOTTOM-SINGLETON], [INV-ENFILADE-OCCUPANCY]: "The occupancy invariant at the bottom level of a GRAN is `sons = 1` (exactly one entry per bottom crum)." There is no minimum-of-2 to enforce because the maximum already makes it impossible. The "minimum guarantee" question is vacuous here — the bounds are identical.

---

## POOM (M_b = 4): upper bound is essential; minimum is `sons ≥ 1`

**The formally stated invariant** ([INV-ENFILADE-OCCUPANCY]) is:

```
forall node in enfilade:
  node.sons >= 1   (except empty root — Bug 0019)
  node.sons <= max_children(node.height, enfilade.type)
```

The lower bound is `1`, not `⌈M_b/2⌉ = 2` and not `B-1 = 3`.

**Why `toofewsons` does not provide a minimum-of-3 guarantee:**

The `toofewsons` predicate triggers rebalancing when `sons < B-1 = 3`, but rebalancing via `recombinend` is only *attempted* when `ishouldbother` returns TRUE — i.e., when the combined son count of a pair fits within `MAX2DBCINLOAF = 4` [ST-REBALANCE-2D].

The POOM split strategy (`splitcrumpm`) peels off the single child with the largest SPANRANGE displacement [ST-SPLIT-2D], producing a `4 + 1` distribution when a 5-son node overflows. For this pair: `4 + 1 = 5 > 4`, so `ishouldbother = FALSE`. Rebalancing cannot proceed. The 1-son node persists.

Later, further insertions or deletions might bring pairs into a mergeable range (`combined ≤ 4`), but there is no mechanism that *guarantees* recovery to `sons ≥ 2` or `sons ≥ 3` after a split.

**[INV-ENFILADE-OCCUPANCY]** documents this explicitly: [SS-ENFILADE-TREE] (Finding 0060) notes the EN-4 invariant (`2 ≤ sons ≤ M`) is violated for GRAN height-1 non-root nodes because M_b=1 makes it unsatisfiable. The analogous POOM violation (post-split 1-son nodes when M_b=4 produces 4+1 that cannot be immediately rebalanced) is structurally present but less visible.

---

## Summary

| Enfilade | M_b | Hard upper bound | Hard lower bound | `toofewsons` trigger | Post-split min |
|----------|-----|-----------------|-----------------|---------------------|----------------|
| GRAN | 1 | 1 | 1 (point) | sons < 1 | 1 |
| POOM | 4 | 4 | 1 | sons < 3 | 1 (from 4+1 peel) |

The essential property is the **upper bound** (`sons ≤ max_children`): it is hard, enforced via the `toomanysons` → `splitcrumupwards` loop [SS-SPLIT]. The minimum guarantee (`sons ≥ 1`) is also a hard invariant (its violation is Bug 0019 [EC-EMPTY-DOC]). The `toofewsons` threshold at `sons < 3` for POOM is a *rebalancing heuristic*, not a guaranteed post-condition — because `ishouldbother`'s capacity check can prevent the rebalancing from executing when it is most needed (immediately after a peel-one split).

## Code Exploration

That confirms it. Here is the full answer.

---

## Occupancy Bounds in the Granfilade and POOM

### The Essential Property Is the Upper Bound Only

The code enforces a strict maximum occupancy per height-1 parent crum, but **no minimum occupancy is enforced after a split**. The POOM does not require (e.g.) at least 2 entries per bottom crum after a split. Here is the complete evidence.

---

### 1. The Three Predicates and Their Thresholds

All three occupancy predicates live in `genf.c:239-261` and dispatch on `is2dcrum()` (any non-GRAN type):

```c
// genf.c:244
return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum((typecorecrum*)ptr)?MAX2DBCINLOAF:MAXBCINLOAF)));
// genf.c:252
return (ptr->numberofsons < (ptr->height > 1 ? MAXUCINLOAF -1 : (is2dcrum((typecorecrum*)ptr)?MAX2DBCINLOAF:MAXBCINLOAF)));
// genf.c:260
return (ptr->numberofsons < (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum((typecorecrum*)ptr)?MAX2DBCINLOAF:MAXBCINLOAF)));
```

For a **height-1** crum (the parent whose direct children are bottom crums), `ptr->height > 1` is FALSE. So the thresholds become:

| Predicate | GRAN height-1 | POOM height-1 | Upper crums (height > 1) |
|---|---|---|---|
| `toomanysons()` | `> 1` | `> 4` | `> 6` |
| `toofewsons()` | `< 1` (i.e., 0) | `< 4` | `< 5` |
| `roomformoresons()` | `< 1` (i.e., 0) | `< 4` | `< 6` |

Key observation: for POOM height-1 crums, **`toofewsons` and `roomformoresons` use the same threshold as `toomanysons`**. A node with 1, 2, or 3 sons is simultaneously "too few" and "has room for more." The only valid fully-occupied state would be exactly 4 sons.

---

### 2. `toofewsons()` Is Dead Code

This is the decisive fact. `toofewsons()` is **defined but never called**:

```
backend/genf.c:247:         bool toofewsons(typecuc *ptr)
backend/recombine.c:54:     /*if (ptr->leftson && toofewsons (ptr)) {**/
```

The only non-definition occurrence is **commented out** in `recombine.c:54`. It was replaced by `roomformoresons()` at some point:

```c
// recombine.c:53-54
if (ptr->leftson && roomformoresons (ptr)) {
/*if (ptr->leftson && toofewsons (ptr)) {**/
```

No live code path calls `toofewsons()`. It enforces nothing.

---

### 3. POOM Splits Create Nodes With Exactly 1 Son

`splitcrumpm()` in `split.c:117-128` selects the son with the largest `SPANRANGE` displacement and hands it to `peelcrumoffnd()`:

```c
// split.c:117-128
int splitcrumpm(typecuc *father)
{
    typecorecrum *ptr, *correctone;
    for(correctone=ptr=findleftson(father);ptr;ptr = findrightbro(ptr)) {
        if (tumblercmp (&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    }
    peelcrumoffnd(correctone);
}
```

`peelcrumoffnd()` at `split.c:130-169`:
1. Calls `disown(ptr)` to remove one child from the overfull parent
2. Calls `createcrum(father->height, father->cenftype)` to make a new sibling
3. Calls `adopt(new, RIGHTBRO, father)` — new sibling placed next to original
4. Calls `adopt(ptr, LEFTMOSTSON, new)` — the one peeled child becomes new's only son

**Result: the new node has exactly 1 son.** There is no post-split check that raises this to a minimum of 2. The original parent retains `(n−1)` sons, where `n > MAX2DBCINLOAF = 4`, so it has at least 4.

Compare this to GRAN's `splitcrumseq()` at `split.c:70-93`:

```c
// split.c:82-89
halfsons = father->numberofsons / 2;
for (i = 0, ptr = findrightmostson(father); i < halfsons && ptr; ++i, ptr = next) {
    next = findleftbro(ptr);
    disown(ptr);
    adopt(ptr, LEFTMOSTSON, new);
    ...
}
```

GRAN uses a **half-split** — both halves end up with approximately equal occupancy. The POOM uses a **peel-one** split — the new sibling gets exactly 1 son.

---

### 4. `splitcrumupwards` Only Checks the Upper Bound

The loop that triggers splits as they propagate upward:

```c
// split.c:27
for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
    if (isfullcrum((typecorecrum*)father)) {
        levelpush(father);
        splitcrum((typecuc*)findleftson(father));
        return(TRUE);
    }
    splitcrum(father);
    splitsomething = TRUE;
}
```

The only predicate tested is `toomanysons()`. The loop terminates when the node is no longer over-full. There is no parallel "while too few sons, try to merge" loop.

---

### 5. Recombine Is Opportunistic, Not a Minimum Guarantee

`recombinend()` in `recombine.c:104-131` does try to merge underpopulated siblings, but it is conditional and lazy:

```c
// recombine.c:112
if (father->height < 2 || !father->modified)
    return(0);
```

It only runs when `father->height >= 2` and `father->modified` is set. It calls `ishouldbother()` to decide whether to merge two height-1 siblings:

```c
// recombine.c:162
return (dest->numberofsons + src->numberofsons <= (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)&&randomness(.3));
```

`randomness(.3)` is hardcoded to return `TRUE` (the probabilistic code is dead):

```c
// recombine.c:133-135
bool randomness(float probability)
{   static float i = 0;
    return(TRUE);
```

So whenever two height-1 POOM siblings together have `<= MAX2DBCINLOAF = 4` sons, they will be merged by `recombinend()`. This is a space-efficiency heuristic — it consolidates `{1,3}`, `{2,2}`, `{1,2}`, `{1,1}` sibling pairs. But:

- It **does not guarantee** that any single node reaches a particular occupancy. A node with 1 son alongside a sibling with 4 sons (`1+4=5 > 4`) would **not** be merged.
- It only fires if `father->height >= 2`. A fresh POOM tree with height 1 gets no recombination at all.
- GRAN's `recombineseq()` has an even stricter gate — `father->height < 3` — so no recombination happens for GRAN height-1 or height-2 parents.

---

### 6. The Disk Format Confirms Partial Occupancy Is Normal

`coredisk.h:49-51`:
```c
typedef struct struct2ddbcloaf {
    typediskloafhedr x2ddbcloafhedr;
    type2ddbc d2dbcarray[MAX2DBCINLOAF];  // fixed array of 4 slots
} type2ddbcloaf;
```

The on-disk loaf always allocates space for exactly `MAX2DBCINLOAF = 4` 2D bottom crums. Actual occupancy is tracked by `typediskloafhedr.numberofcrums`. The disk format explicitly supports 1, 2, 3, or 4 entries per loaf — there is no minimum enforced at the serialization layer either.

---

### 7. The GRAN Special Case: Upper Bound Collapses to Exact Occupancy

With `MAXBCINLOAF = 1`:
- `toomanysons()` fires when `numberofsons > 1`, i.e., at 2 sons
- `toofewsons()` fires when `numberofsons < 1`, i.e., at 0 sons
- `roomformoresons()` fires when `numberofsons < 1`, i.e., at 0 sons

A GRAN height-1 crum can never hold more than 1 son (splits fire immediately at 2) and can never hold 0 sons (it would be garbage-collected as empty). The maximum is 1, the implicit minimum is 1: every GRAN height-1 crum holds **exactly** 1 bottom crum. This makes the GRAN's "upper bound" trivially equal to "exact occupancy" — but it is still expressed as a maximum, not a minimum.

The comment in `enf.h:27` makes the rationale explicit:

```c
#define MAXBCINLOAF    1        /* so text will fit *//* as you wish */
```

The note `/* as you wish */` confirms this is a tunable parameter, not a structural invariant derived from minimum-occupancy logic.

---

### Conclusion

**The essential shared property is the upper bound alone.** Both the granfilade and the POOM enforce a strict maximum occupancy per height-1 parent crum (`MAXBCINLOAF = 1` and `MAX2DBCINLOAF = 4` respectively). Neither structure enforces a minimum occupancy guarantee through any active code path.

For the POOM specifically:
- `toofewsons()` [genf.c:247] would provide a minimum-occupancy check (firing when count < 4), but it is **dead code** — defined and never called.
- POOM splits via `peelcrumoffnd()` [split.c:130] create new nodes with **exactly 1 son**, the minimum possible.
- `recombinend()` [recombine.c:104] is a lazy consolidation heuristic that may raise occupancy over time, but guarantees no floor.
- The on-disk format [coredisk.h:49-51] accommodates 1 to 4 entries per loaf, with partial occupancy as a first-class state.

The GRAN's `MAXBCINLOAF = 1` is a degenerate case where the maximum trivially coincides with the only valid occupancy, so there is no room in which a minimum guarantee could even be distinct from the maximum. The POOM's `MAX2DBCINLOAF = 4` leaves that room open but does not fill it with an enforced lower bound.

---

## Question 17 [gregory]

> When `incontextlistnd` performs insertion-sort by V-address during retrieval, is this sorting necessary because the tree traversal order can differ from logical V-order, or is it a defensive measure against a specific class of tree shapes produced by certain operation sequences?

### Gregory's Answer

## KB Synthesis

The sorting in `incontextlistnd` is **necessary**, not merely defensive. The root cause is that 2D enfilade tree structure uses diagonal ordering (L1-norm) for rebalancing, which fundamentally breaks the correspondence between sibling order and V-address order.

## Why Tree Traversal Order Differs from V-Order in 2D Enfilades

`[ST-REBALANCE-2D]` (Finding 0071) documents the critical mechanism: `recombinend` orders children by sorting via `comparecrumsdiagonally`, which uses the key `cdsp.dsas[0] + cdsp.dsas[1]`. For a POOM, dimension 0 is ORGLRANGE (I-space) and dimension 1 is SPANRANGE (V-space), so the sort key is `I-address + V-address` — an L1-norm diagonal sweep across the 2D address space, not a pure V-address ordering.

After rebalancing, a left-to-right sibling walk (`findcbcinarea2d`) yields contexts in diagonal order. A POOM with entries at `(I=1, V=5)` and `(I=3, V=2)` would have the second entry sorted first (diagonal key 5 vs 6), even though the second entry has a smaller V-address. Without insertion-sort, the returned V-spans would emerge in I+V diagonal order.

`[ST-SPLIT-2D]` adds a further complication: POOM splits peel by SPANRANGE dimension only (`cdsp.dsas[SPANRANGE]`), while SPAN splits use the diagonal. This means split boundaries don't align with the rebalance ordering either.

## Why 1D Enfilades Don't Need It

The contrast with `oncontextlistseq` makes the necessity explicit. `[SS-CONTEXT-LIST]` states the choice of accumulation function depends on enfilade type:

- **GRAN (1D)**: insertions always go as RIGHTBRO of the retrieval position (`[SS-ENFILADE-TREE]`, Finding 0041), and sibling traversal is left-to-right. Because 1D inserts always append to the right of the current position, the tree naturally maintains sequential order. `oncontextlistseq` (append-preserving) suffices.
- **POOM/SPAN (2D)**: diagonal rebalancing destroys any sequential ordering that may have existed at insertion time. `incontextlistnd` (insertion-sort) is required.

## The Invariant It Maintains

`[INV-RETRIEVAL-V-SORTED]` formalizes this: the result list is sorted by left boundary in the queried dimension, and this holds **regardless of tree structure** — after any sequence of splits, rebalances, or out-of-order insertions. `[INV-RETRIEVAL-TREE-INDEPENDENCE]` states the consequence: "tree-internal reorganization (splits, rebalances, rotations) does not change the observable result ordering."

The insertion-sort is therefore not a defensive measure against *specific* tree shapes from *particular* operation sequences — it is a universal requirement for 2D enfilades, because the diagonal ordering used in `recombinend` is applied to all rebalancing operations without exception.

## Code Exploration

Now I have all the evidence I need. Let me compile the complete analysis.

---

## Answer

### `incontextlistnd` — Why the Insertion Sort Is Structurally Necessary

The sort is **not** a defensive measure against exotic tree shapes. It corrects a structural mismatch that arises from three independent, normal-case properties of the 2D enfilade.

---

### 1. The call chain

`vspanset2ispanset` and `ispan2vspanset` in `orglinks.c:389-402` both call `permute`, which calls `span2spanset`, which calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```
[orglinks.c:435]

This routes through `retrieveinarea` → `findcbcinarea2d` [retrie.c:87-110], which builds the context list by calling:

```c
incontextlistnd (headptr, context, index1);
```
[retrie.c:263]

`incontextlistnd` [context.c:75-111] performs an insertion sort keyed on `grasp.dsas[index]` — that is, sorted by the `index1` dimension's starting address.

---

### 2. The POOM tree is indexed by V, not by I

The constant definitions are:

```
I  = 0     V  = 1     (wisp.h:19-20)
```

Every call to `insertnd` for POOM content passes `index = V`:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
[orglinks.c:130]

`insertmorend` uses `cdsp.dsas[index]` = `cdsp.dsas[V]` to find where in the subtree to descend, and `insertcbcnd` places the new leaf as `RIGHTMOSTSON` [insertnd.c:262] — appended to the right of all existing leaves, with `cdsp = origin - grasp`.

This means the tree's primary traversal order is V-order only if leaves happen to be inserted in monotone V-order. That condition is broken routinely.

---

### 3. `makeroomonleftnd` inverts leaf order for leftward insertions

When a new item's V-address is less than the current root's `grasp` (i.e., an insertion to the left of all existing content), `makeroomonleftnd` calls `expandcrumleftward`:

```c
for (; ptr; ptr = (typecorecrum *)findrightbro(ptr)) {
    tumbleradd(base, &ptr->cdsp.dsas[index], &ptr->cdsp.dsas[index]);
```
[makeroom.c:64-66]

This shifts **all existing children's** `cdsp.dsas[V]` upward by `base`. The new leaf is then appended rightmost with its small V-displacement. The sibling sequence becomes: `[existing leaves, now with large V-cdsp] → [new leaf, small V-cdsp]`. The rightmost leaf has the smallest V-address. This is **backwards V-order**, produced by a completely normal second insertion at a smaller V-address.

---

### 4. `recombinend` never reorders leaves

`recombinend` in `recombine.c` checks:

```c
if (father->height < 2  || !father->modified)
    return(0);
```
[recombine.c:112]

Leaves have `height == 0`; their direct parents have `height == 1`. The guard `height < 2` means `recombinend` **skips all height-1 nodes** — the only nodes that could resort leaf siblings. Leaves are permanently left in insertion order regardless of how many subsequent operations occur.

---

### 5. Higher-level nodes are sorted diagonally, not by V or I

For nodes with `height >= 2`, `recombinend` calls `getorderedsons` → `shellsort`, which sorts siblings by:

```c
tumbleradd(&v[i]->cdsp.dsas[0], &v[i]->cdsp.dsas[1], &tarray[i]);
```
[recombine.c:298]

This is `cdsp[I] + cdsp[V]` — a **diagonal** sort, not V-only or I-only. Left-to-right traversal of height-2+ nodes gives diagonal order, which neither matches V-order nor I-order in general.

---

### 6. Consequence for both retrieval directions

**V→I conversion** (`vspanset2ispanset`): `index1 = V`. The POOM tree is V-indexed, but leaf-level children are in insertion order (not V-order), and higher nodes are diagonal-sorted. The sort in `incontextlistnd` corrects this to V-order.

**I→V conversion** (`ispan2vspanset`): `index1 = I`. The entire tree is V-indexed; traversal produces leaves in V-order, which has no relationship to I-order. The sort corrects this to I-order.

In both cases the sort is **load-bearing**.

---

### Conclusion

The sort in `incontextlistnd` corrects a genuine structural mismatch, not a defensive guard. Three independent properties combine to ensure that 2D enfilade traversal order never matches the logical address order of `index1`:

1. **Leaves are appended rightmost** by `insertcbcnd` [insertnd.c:262], not placed in V-sorted position.
2. **`makeroomonleftnd` inverts leaf order** for any leftward insertion [makeroom.c:64-66], a normal case for `docopy` where text fragments arrive in arbitrary V-sequence.
3. **`recombinend` skips height-1 nodes** [recombine.c:112], so leaves are never re-sorted post-insertion; and higher nodes are sorted diagonally [recombine.c:298], not by any single dimension.

Any of these three alone is sufficient to make the sort mandatory. All three arise from ordinary single-insert and copy operations — not from pathological operation sequences.

---

## Question 18 [gregory]

> Does the width stored in an upper crum need to equal the exact sum of its children's widths, or is it sufficient for the width to be an upper bound that contains all children — i.e., could a "bounding box" semantics work for 2D enfilades instead of exact aggregation?

### Gregory's Answer

## KB Synthesis

## Upper Crum Width: Exact Summation vs. Bounding Box

The answer differs by enfilade type — and both semantics are already present in the implementation.

### 1D (GRAN): Exact Summation

For GRAN enfilades, `setwidseq` computes each upper crum's width as the exact sum of its children's widths [SS-ENFILADE-TREE, Finding 0066]. The root displacement is always zero. Positional navigation requires exact aggregation: to find the N-th byte, you compare cumulative widths left-to-right at each level. An overestimate would break position-based descent.

### 2D (POOM, SPAN): Tight Bounding Box

For POOM and SPAN enfilades, `setwispnd` produces a **tight bounding box**, not an exact sum [SS-ENFILADE-TREE, Finding 0066]:

> `root.cdsp` and `root.cwid` together form a bounding box: `root.cdsp` is the upper-left corner (minimum address), `root.cdsp + root.cwid` is the lower-right corner (maximum extent).

The algorithm:
1. Finds `mindsp` = minimum displacement across children
2. Absorbs `mindsp` into the parent's `cdsp` (shifting the origin)
3. Subtracts `mindsp` from every child's `cdsp` (making children relative)
4. Sets `cwid` to cover from the new origin to the maximum child extent

The result is always the *minimal* bounding box — not an overestimate, but the tightest possible covering.

**Why this differs from summation:** Consider two crums at V-positions 1.1 (width 0.3) and 1.7 (width 0.2). Their combined V-extent is 0.9 (from 1.1 to 2.0), not 0.5 (sum of widths). The bounding box captures the *range*, not the *total size*.

### Would Loose Bounding Box Semantics Work?

For correctness of the retrieval algorithms, **any upper bound would preserve correctness** — but at a cost to efficiency.

`whereoncrum` [SS-WHEREONCRUM, Finding 0062] classifies addresses into five cases relative to `[grasp, reach)`. An overestimated `cwid` would expand the reach, causing some subtrees to be entered unnecessarily (false positives during search), but no valid entries would be missed.

`findcbcinarea2d` [SS-ENFILADE-TREE, Finding 0041] traverses all siblings and recurses into qualifying subtrees. A loose bounding box means more subtrees qualify — more traversal, same results.

The two-blade knife for INSERT [SS-TWO-BLADE-KNIFE, Finding 0054] classifies POOM entries into shift/no-shift regions using `whereoncrum`. An overestimated reach could pull entries into the ONMYRIGHTBORDER case prematurely, but the `findaddressofsecondcutforinsert` mechanism is address-arithmetic-based, not width-based, so this wouldn't affect subspace isolation [FC-SUBSPACE].

`isemptyenfilade` for 2D enfilades checks both `cwid == 0` AND `cdsp == 0` [SS-ENFILADE-TREE, Finding 0066]. With a loose bounding box, an empty enfilade might retain a non-zero phantom `cwid`, breaking the emptiness predicate.

### Summary

| Enfilade | Semantics | Algorithm | Loose box works? |
|----------|-----------|-----------|-----------------|
| GRAN (1D) | Exact sum | `setwidseq` | No — breaks positional navigation |
| POOM (2D) | Tight bounding box | `setwispnd` | Partially — retrieval stays correct, but `isemptyenfilade` breaks |
| SPAN (2D) | Tight bounding box | `setwispnd` | Same as POOM |

The implementation maintains tight bounding boxes for 2D enfilades because: (1) `setwispnd`'s min-absorption gives the tightest possible box, (2) `isemptyenfilade` relies on exact zero-check, and (3) tightness minimizes unnecessary traversal. A loose upper bound would preserve retrieval correctness but break the empty-detection invariant and degrade performance.

## Code Exploration

I now have all the evidence needed. Here is my full answer.

---

## Does the upper crum's width need to be an exact aggregate, or can it be a loose upper bound?

The answer differs fundamentally between the two enfilade types, and the code makes the distinction explicit.

---

### GRAN (1D Sequential): Exact Sum is Mechanically Required

**`wisp.c:150–168` — `setwidseq`** computes the parent width as the exact sum of children:

```c
clear (&sum, sizeof (sum));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)){
    widopseq (&sum, &ptr->cwid, &sum);   // sum += child->cwid
}
// ...
movewisp (&sum, &father->cwid);          // parent->cwid = exact sum
```

This is not a policy choice — it is mechanically required by the traversal algorithm.

**`retrie.c:191–206` — `findcbcseq`** navigates by accumulating a running offset:

```c
for (; getrightbro (ptr); ptr = ptr->rightbro) {
    if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
        break;
    dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);
    // offset += this sibling's cwid
}
```

**`retrie.c:351–353` — `whereoncrum` for GRAN** defines each sibling's interval as exactly `[offset, offset + cwid)`:

```c
case GRAN:
   tumbleradd (&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
   return (intervalcmp (&offset->dsas[WIDTH], &right, address));
```

The traversal works as follows: scan siblings left to right; if the address falls within `[offset, offset+cwid)`, descend; otherwise, advance `offset += cwid` and try the next sibling. The running offset is the cumulative sum of all previously-skipped siblings' widths.

**Why an overestimate breaks this:** If `cwid` is larger than the actual content:

- The interval `[offset, offset+cwid)` is too wide
- An address just past the true end but inside the overestimated range triggers a descent
- The descent finds nothing (the address isn't actually there)
- Critically: the `offset` was never advanced past this sibling — the loop broke to descend
- All siblings to the right are now unreachable

This is a hard correctness failure. An overestimate by even one unit causes false misses. An underestimate has the symmetric failure: addresses within the crum are not found, and the offset advances too early.

**Conclusion for GRAN: the parent width must equal the exact sum of children's widths.**

---

### SPAN/POOM (2D Non-Deterministic): Already Bounding Box, Not Sum

**`wisp.c:171–228` — `setwispnd`** computes the parent width as the **tight bounding box** of children, not the sum:

```c
// Step 1: find the minimum displacement (upper-left corner of all children)
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp,
             (unsigned)dspsize(ptr->cenftype));

// Step 2: normalize — subtract mindsp from each child's cdsp
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);

// Step 3: new width = max(cdsp + cwid) = far corner of bounding box
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
        (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
        (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));

// Step 4: store
movewisp (&newdsp, &father->cdsp);    // adjusted upper-left
movewisp (&newwid, &father->cwid);    // tight bounding box extent
```

The aggregation operation is `max(cdsp + cwid) − min(cdsp)` (after normalizing cdsp to zero). This is the tight bounding hull, not a sum.

**`retrie.c:208–227` — `findcbcnd`** uses `cwid` only for pruning, not for position accumulation:

```c
if ((cmp = whereoncrum (father, offsetptr, address, index))
      < ONMYLEFTBORDER || cmp > THRUME )
    return (NULL);                          // prune: not in bbox
if (father->height != 0) {
    prologuend (father, offsetptr, &grasp, (typedsp*)NULL);
    for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
        if (retr = findcbcnd (ptr, &grasp, address, index))
            break;
}
```

**`retrie.c:355–374` — `whereoncrum` for SPAN/POOM** checks `[offset + cdsp, offset + cdsp + cwid)`:

```c
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index],&ptr->cdsp.dsas[index], &left);
    // left = offset + cdsp
    cmp = tumblercmp(address,&left);
    if(cmp == LESS){ return(TOMYLEFT); }
    else if(cmp == EQUAL){ return(ONMYLEFTBORDER); }
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    // right = left + cwid = offset + cdsp + cwid
    cmp = tumblercmp(address,&right);
    if(cmp == LESS){ return(THRUME); }
    ...
```

The interval is `[offset + cdsp, offset + cdsp + cwid)`. Each node's position (`cdsp`) is stored independently — there is no running offset accumulation when traversing siblings.

**Would a loose upper bound work for SPAN/POOM?**

- **An overestimate (loose upper bound)**: The pruning check `whereoncrum > THRUME` would fire less aggressively, causing unnecessary descent into subtrees that contain nothing. All true matches would still be found. Correctness is preserved; only efficiency suffers.
- **An underestimate**: The pruning check would fire too aggressively, skipping subtrees that do contain valid results. This is a correctness failure (false negatives).
- **The tight bounding box** (what the code computes): maximum pruning with no false negatives.

**Conclusion for SPAN/POOM: the parent width IS already bounding-box semantics.** The aggregation operator is `max(cdsp + cwid) − min(cdsp)`, computed by `lockmax`/`lockmin` in `setwispnd`. A loose upper bound would preserve correctness but reduce traversal efficiency. The tight bounding box is optimal.

---

### The Key Asymmetry

| Enfilade type | `cwid` role in traversal | Exact required? | Overestimate effect |
|---|---|---|---|
| GRAN | Position accumulation (`offset += cwid`) | **Yes — exactly** | Corrupts running offset; subsequent siblings unreachable |
| SPAN/POOM | Pruning only (`address within [offset+cdsp, offset+cdsp+cwid)?`) | No — upper bound sufficient | Reduces pruning efficiency only |

For GRAN, the parent's `cwid` is both a measure of content span and a positional token consumed by the traversal algorithm. The two roles coincide only when `cwid` is exact.

For SPAN/POOM, each node carries its own absolute displacement (`cdsp`), so no position accumulation happens. The width is a pure bounding box used only for early exit. The current implementation maintains the **tight** bounding box — the minimum value that is still a valid upper bound — which is exactly "bounding box semantics."

---

## Question 19 [gregory]

> After a split promotes a new sibling via `splitcrumupwards`, must the parent's displacement and width be recomputed from scratch over all children, or does the split algorithm maintain them incrementally — and which approach does correctness actually require?

### Gregory's Answer

## KB Synthesis

## After `splitcrumupwards`: Displacement/Width Recalculation

### What the Implementation Does

The split algorithm handles structural changes (moving children to a new sibling), then **full recomputation from scratch** handles the displacement/width invariants — as two separate phases.

`splitcrumupwards` (`split.c:16-43`) fixes occupancy overflow by creating a new sibling via `splitcrum` (dispatching to `splitcrumpm` or `splitcrumsp` for 2D enfilades, `splitcrumseq` for GRAN). The `adopt(new, RIGHTBRO, ptr)` call wires the new sibling into the tree [ST-SPLIT-2D, SS-ENFILADE-TREE]. After `splitcrumupwards` returns, the caller proceeds to `setwispupwards`, which walks from the modified node up to the root calling `setwispnd` at each level [ST-INSERT, Finding 0066].

`setwispnd` (`wisp.c:171-228`) does **not** perform an incremental update. It:
1. Scans **all** children to find `mindsp` — the minimum displacement across the entire child set
2. Adds `mindsp` to the parent's `cdsp` (absorbs the new minimum)
3. Subtracts `mindsp` from every child's `cdsp` (makes all displacements relative)

This is a full scan at each level, repeated all the way to the root [SS-ENFILADE-TREE, INV-ENFILADE-RELATIVE-ADDRESSING].

For 1D GRAN enfilades, `setwidseq` (`wisp.c:150-168`) similarly recomputes the parent's `cwid` by summing all children's widths from scratch, not incrementally [SS-ENFILADE-TREE, Finding 0066].

### Why Correctness Requires From-Scratch Recomputation

**For 2D enfilades (POOM, SPAN):** The parent's `cdsp` must equal the **minimum** displacement among its children — this is the invariant that `setwispupwards` maintains and that `prologuend` (`retrie.c:334-339`) relies on when computing `grasp = offset + ptr->cdsp` [INV-ENFILADE-RELATIVE-ADDRESSING]. After a split moves some children to the new sibling:

- The original node may have lost its previous minimum-displacement child
- The new sibling received some children, but which has the new minimum across the original node's remaining children is unknown without scanning
- The parent now sees an additional child (the sibling) with its own `cdsp`

No incremental approach can correctly determine the new minimum at either the original node or the parent without examining all remaining children. The minimum is not maintained with any auxiliary structure (no second-minimum tracking, no heap). Stale `cdsp` values would corrupt every subsequent retrieval by making `grasp` calculations wrong.

**For 1D GRAN enfilades:** The parent's `cwid` must be the **sum** of children's widths. After a split, some children moved away, so the sum changes. Width of the sibling must be initialized, and parent's width must reflect both nodes. Again, this requires a fresh sum over all remaining children.

**`levelpush` case at the fullcrum:** When the root overflows, `levelpush` pushes all existing children down one level and installs them as children of a new intermediate node, then the old root regains height=H+1 with the new intermediate as sole child [SS-ENFILADE-TREE, Finding 0058]. The intermediate node's `cdsp` and `cwid` must then be computed over all the moved children — only a full scan produces the correct minimum/sum.

### The Incremental Alternative Would Fail

An incremental update would need to:
- Track the minimum of a dynamic multiset (children's `cdsp` values) with O(1) delete-minimum
- Or track a running sum that adjusts for removed and added children

Neither structure is maintained. After `splitcrum` moves the `k` rightmost children (by diagonal ordering in 2D [ST-SPLIT-2D]) to the new sibling, the original node's minimum displacement is unknown without scanning its residual children. A naïve increment — "subtract the moved children's contribution and add the sibling's" — fails because:
1. The sibling's `cdsp` hasn't been established yet when the parent needs updating
2. The minimum among the original node's remaining children may have changed to any survivor

The two-phase design (structural split, then `setwispupwards` full recomputation) is therefore both what the implementation does and what correctness requires. [SS-ENFILADE-TREE, INV-ENFILADE-RELATIVE-ADDRESSING, INV-ENFILADE-OCCUPANCY]

## Code Exploration

I have everything. Here is the complete answer.

---

## Split Algorithm: Displacement & Width — From Scratch, Not Incremental

### The Short Answer

After `splitcrumupwards` promotes a new sibling, the parent's displacement (`cdsp`) and width (`cwid`) **are recomputed from scratch by scanning all current children**. There is no delta or incremental update. This full-scan approach is what correctness requires, not just an implementation convenience.

---

### The Code Path

`splitcrumupwards` [split.c:16-44] is the entry point. It loops upward through ancestors while `toomanysons` returns true:

```c
for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
    if (isfullcrum((typecorecrum*)father)) {
        levelpush(father);
        splitcrum((typecuc*)findleftson(father));   // split.c:30
        return(TRUE);
    }
    splitcrum (father);                              // split.c:37
    splitsomething = TRUE;
}
```

Every path through `splitcrum` [split.c:47-67] ends with the same call:

```c
setwispupwards(father, 0);                           // split.c:66
```

The type-specific split routines add more `setwispupwards` calls on top of that:

- **`splitcrumseq`** [split.c:70-93] (GRAN): `setwispupwards(father, 0)` then `setwispupwards(new, 0)` [lines 91-92] — one call for the original node (now holding the left half), one for the new sibling (holding the right half).
- **`peelcrumoffnd`** [split.c:130-169] (SPAN/POOM): `setwispupwards(father, 0)`, `setwispupwards(new, 0)`, `setwispupwards(ptr, 1)` [lines 166-168] — three separate upward passes.
- **`levelpush`** [genf.c:263-294]: `setwispupwards(new, 1)` [line 288] after transferring all children to the new intermediate node.

None of these calls pass a delta. They all pass the affected node and let `setwispupwards` recompute upward from it.

---

### What `setwispupwards` Actually Does

`setwispupwards` [wisp.c:83-111]:

```c
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather ((typecorecrum*)ptr);
    changed = setwisp ((typecorecrum*)ptr);
    ...
}
```

It walks from the modified node toward the apex, calling `setwisp` at each level. It stops only when `setwisp` returns FALSE (the stored value was already correct). The early-termination is an optimization, not an incremental delta. Each individual `setwisp` call is a **full scan of all children**.

#### GRAN case — `setwidseq` [wisp.c:150-168]:

```c
clear (&sum, sizeof (sum));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)){
    widopseq (&sum, &ptr->cwid, &sum);       // sum += child->cwid
}
```

Iterates every sibling from left to right, accumulates the sum, stores it. No memory of the previous value, no delta.

#### SPAN/POOM case — `setwispnd` [wisp.c:171-228]:

**Pass 1** — find the new minimum displacement across all children:

```c
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr)) {
    lockmin (...&mindsp, ...&ptr->cdsp, ...&mindsp, ...);   // wisp.c:195
}
```

**Pass 2** — normalize all children's stored displacements by subtracting that minimum, then compute the new bounding-box width:

```c
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    if (!lockiszerop) {
        dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...);       // wisp.c:211
    }
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid, ...);
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid, ...);  // wisp.c:214
}
```

Then the parent gets:

```c
dspadd (&father->cdsp, &mindsp, &newdsp, ...);   // new parent dsp = old_parent_dsp + min_child_dsp
movewisp (&newdsp, &father->cdsp);               // wisp.c:224
movewisp (&newwid, &father->cwid);               // wisp.c:225
```

This normalization step actively **writes back to every child** to subtract the minimum offset. That mutation requires scanning all children regardless.

---

### Why Correctness Requires From-Scratch Recomputation

#### For GRAN (sequential enfilades):

The invariant is `parent->cwid = Σ child->cwid` across all children. After `splitcrumseq` moves the right half of children to the new sibling, `father->cwid` is stale — it encoded the sum of all children, but `father` now has only the left half. The only way to restore the invariant is to sum the current set of children. There is no valid delta because the moved children's widths are no longer available under `father`.

#### For SPAN/POOM (2D enfilades):

The invariant is that a crum's own `cdsp` is a canonical offset such that all children's `cdsp` fields are expressed in local coordinates with the minimum-displacement child at position zero. When a split creates a new sibling and that sibling is inserted into the parent's child list, the parent has a new set of children with potentially different minimum displacement. The normalization step (`setwispnd`) must:

1. Find the new minimum across all children — requires scanning all children.
2. Subtract it from all children's `cdsp` — requires writing all children.
3. Re-derive the bounding box — requires scanning all children again.

There is no incremental shortcut. You cannot compute the new minimum by knowing only which child was added; you must compare the new child's displacement to every surviving child's displacement. And if the minimum changed, you must update every child's stored displacement.

#### The Two-Pass Ordering in `splitcrumseq`

`splitcrumseq` calls `setwispupwards(father, 0)` first [split.c:91], then `setwispupwards(new, 0)` [split.c:92]. At the time the first call propagates through the grandparent, `new->cwid` is still 0 (as initialized by `createcrum`). The grandparent's wisp is therefore computed wrong on the first pass. The second call (`setwispupwards(new, 0)`) fixes `new->cwid` and then propagates up again, recomputing the grandparent correctly for the second time. This is not a bug — `setwispupwards` is idempotent and convergent — but it demonstrates that the algorithm depends on the full-scan at each level, not on a carefully maintained delta, to reach the correct answer.

---

### `levelpush` Path

When `splitcrumupwards` hits the apex [split.c:28-35], it calls `levelpush(father)` which:

1. Creates `new` at the same height as the apex [genf.c:279]
2. Transfers all children of the apex to `new` via `transferloaf` [genf.c:282]
3. Increments the apex's height [genf.c:285]
4. Adopts `new` as the sole child of the apex [genf.c:286]
5. Calls `setwispupwards(new, 1)` [genf.c:288] — full-scan recomputation of `new`'s wisp, then propagates to the apex

Then `splitcrum(findleftson(father))` = `splitcrum(new)` runs and splits `new` the usual way. Same full-scan recomputation again.

---

### Summary

| What happens | How wisp is maintained |
|---|---|
| `splitcrumseq` splits GRAN node | `setwidseq` scans ALL children and sums `cwid`; called separately for `father` and `new` |
| `peelcrumoffnd` splits SPAN/POOM node | `setwispnd` scans ALL children; normalizes `cdsp` of every child; called separately for `father`, `new`, and the peeled `ptr` |
| `levelpush` grows the tree height | `setwispupwards(new, 1)` recomputes from scratch up to apex |
| `splitcrumupwards` loop | Delegates entirely to `splitcrum → setwispupwards`; no explicit wisp arithmetic in the loop itself |

**The split algorithm recomputes displacement and width from scratch over all children at every affected level. Incremental maintenance would be incorrect for SPAN/POOM because the displacement normalization step in `setwispnd` [wisp.c:211] writes back to every child, and computing the correct normalized minimum requires scanning every child. There is no representation of a "delta" in the data structures, and the algorithm makes no attempt at one.**

---

## Question 20 [gregory]

> If two bottom crums in the same POOM have V-spans that are logically adjacent (the end of one equals the start of the next) but map to non-contiguous I-addresses, does the enfilade guarantee they remain as separate crums, or could a rebalance operation merge them into a single crum with a discontinuous I-mapping?

### Gregory's Answer

## KB Synthesis

They are guaranteed to remain as separate crums. Rebalancing never inspects or fuses the content of bottom crums — it operates purely at the tree-structure level.

**What rebalancing actually does**

From [ST-REBALANCE-2D], `recombinend` performs two operations:
- `eatbrossubtreend`: one height-1 node absorbs all **children** (bottom crums) from another height-1 node, then the donor is freed
- `takenephewnd`: individual bottom crums are moved from one height-1 node to another via `adopt`

In both cases, the bottom crums are **moved**, not modified. Their V-origin, V-width, I-origin, and I-width fields are untouched by rebalancing. The rebalancer has no knowledge of semantic adjacency or I-address contiguity — it only compares displacement coordinates to decide merge order (the diagonal key in `getorderedsons`).

**Why content fusion cannot happen**

The only mechanism that merges two separately-created bottom crums into one is `isanextensionnd` [ST-INSERT Finding 0062]. It is called exclusively within the INSERT path (`insertnd` → `isanextensionnd`), and it requires **both** conditions to hold:
1. Same `homedoc` (I-address origin document)
2. New content's I-origin exactly equals the existing crum's I-reach (contiguous in I-space)

If I-addresses are non-contiguous, condition 2 fails at creation time, a new crum is created instead of extending the existing one, and there is no subsequent path that re-evaluates this check. Rebalancing code in `recombine.c` contains no calls to `isanextensionnd` or any equivalent adjacency check.

**The `homedoc` invariant further reinforces separation**

From [ST-VCOPY Finding 0046], `isanextensionnd` also rejects extension when `homedoc` differs. So even if two adjacent crums happened to have contiguous I-addresses, they would not be merged by rebalancing if they came from different source documents. The B-tree structure preserves provenance boundaries.

**Summary**

Two bottom crums that are V-adjacent but I-non-contiguous will remain as separate crums for the lifetime of the enfilade. The rebalancer ([ST-REBALANCE-2D], [SS-ENFILADE-TREE]) reorganizes the tree to satisfy occupancy bounds ([INV-ENFILADE-OCCUPANCY]), shuffling bottom crums between parent nodes as needed — but it never inspects, merges, or rewrites the content mappings within those crums. Content fusion is strictly an insertion-time operation gated by `isanextensionnd`.

## Code Exploration

I now have all the evidence needed. Here is the complete answer:

---

## Answer: V-Adjacent, I-Non-Contiguous POOM Bottom Crums Cannot Be Merged by Rebalance

**The enfilade guarantees they remain as separate crums.** There is no code path — not insertion coalescing, not `recombinend`, not deletion — that would merge two bottom crums whose V-spans are adjacent but whose I-addresses are non-contiguous.

---

### 1. POOM Bottom Crum Structure

From `enf.h:109-131`, a `type2dcbc` (2D core bottom crum) carries:
- `cdsp.dsas[I]` and `cdsp.dsas[V]`: displacement from parent's grasp in both dimensions
- `cwid.dsas[I]` and `cwid.dsas[V]`: extent in both dimensions  
- `c2dinfo.homedoc`: the document ISA

From `wisp.h:18-22`, the index constants are:
```c
#define I  0
#define V  1
```
And `dspsize(POOM) = DSPSIZEPM = 2` — meaning every wisp comparison covers **both** I and V together.

---

### 2. `isanextensionnd` — The Only Path That Merges a Bottom Crum

The only place an existing bottom crum is ever enlarged is `insertnd.c:249-258`:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ...
        return(FALSE);
    }
}
```

`isanextensionnd` is defined at `insertnd.c:301-309`:

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
- `grasp[I] = offset[I] + cdsp[I]`, `grasp[V] = offset[V] + cdsp[V]`
- `reach[I] = grasp[I] + cwid[I]`, `reach[V] = grasp[V] + cwid[V]`

`lockeq` (`wisp.c:261-267`) iterates over all `loxize` tumblers:
```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
       if (!tumblereq (lock1++, lock2++))
           return(FALSE);
    return(TRUE);
}
```

Because `dspsize(POOM) = 2`, `lockeq` tests **both** `reach.dsas[I] == origin[I]` AND `reach.dsas[V] == origin[V]`.

**Consequence:** If two crums are V-adjacent (`reach[V] == origin[V]`) but I-non-contiguous (`reach[I] ≠ origin[I]`), `lockeq` returns `FALSE`, `isanextensionnd` returns `FALSE`, and a new distinct bottom crum is created at `insertnd.c:260-274`. **No coalescing occurs during insertion.**

---

### 3. `recombinend` — The Rebalance Operation Cannot Touch Bottom Crums

The rebalance entry point `recombine.c:22-34` dispatches to `recombinend` for POOM:
```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case POOM:
            recombinend (father);
    }
}
```

`recombinend` (`recombine.c:104-131`) begins with a hard guard:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);
    ...
}
```

This means:
- **Height-0 nodes** (bottom crums themselves) are never touched.
- **Height-1 nodes** (whose children ARE bottom crums) are never touched — because height 1 < 2.
- `recombinend` recursively visits children, but each recursive call on a height-1 child returns immediately.

The restructuring operations — `takeovernephewsnd` and `eatbrossubtreend` — only move height-1 nodes between height-2 parents. When `eatbrossubtreend` (`recombine.c:205-233`) merges two siblings, it splices `bro`'s child list onto `me`'s child list:

```c
getleftson (bro)->leftbroorfather = getrightmostbro (getleftson (me));
getrightmostbro (getleftson (me))->rightbro = getleftson (bro);
bro->leftson->isleftmost = FALSE;
me->numberofsons += bro->numberofsons;
```

If `me` and `bro` are height-1 nodes, their children are bottom crums (height 0). This operation grafts a group of bottom crums from `bro` into `me` as additional siblings. Each bottom crum retains its individual `cdsp`/`cwid` — it is **relocated in the tree, not merged with another crum**. `fixdspsofbroschildren` (`recombine.c:259-268`) only adjusts relative displacements to account for the change of parent; it does not alter widths or fuse crums:

```c
int fixdspsofbroschildren(typecuc *me, typecuc *bro)
{
    for (nephew = getleftson (bro); nephew; nephew = getrightbro(nephew)) {
        dspadd (&bro->cdsp,&nephew->cdsp, &nephew->cdsp, me->cenftype);
        dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
        ivemodified(nephew);
    }
}
```

---

### 4. `splitcrumpm` — Only Splits, Never Merges

`split.c:117-128` selects the child with the greatest V-displacement and peels it off into a new sibling node via `peelcrumoffnd`. This is a pure splitting operation; it has no merge path.

---

### 5. No Implicit Merge in `deletend` or `rearrangend`

Both `edit.c:75` (`deletend`) and `edit.c:139` (`rearrangend`) call `recombine` after their structural edits. As established in point 3, `recombine` cannot merge bottom crums — it only reorganizes height ≥ 2 structure.

---

### Summary

| Code path | Can merge bottom crums? | Why not |
|---|---|---|
| `isanextensionnd` (insertnd.c:301) | No — unless both I and V adjacent | `lockeq` tests all `dspsize(POOM)=2` components; I mismatch returns `FALSE` |
| `recombinend` (recombine.c:104) | No | Guard `height < 2` blocks operation on height-1 parents of bottom crums |
| `eatbrossubtreend` (recombine.c:205) | No | Splices sibling lists; adjusts `cdsp` offsets but never fuses two crums into one |
| `splitcrumpm` / `splitcrumupwards` (split.c) | No | Split-only operations |
| `deletend` / `rearrangend` (edit.c) | No | Delegated to `recombine`, same constraint |

**Two bottom crums in the same POOM with logically adjacent V-spans but non-contiguous I-addresses are structurally guaranteed to remain as separate crums.** The enfilade has no mechanism that examines the I-addresses of sibling bottom crums and fuses them based on V-adjacency alone. A rebalance can move bottom crums between upper-level parents, but each crum retains its individual I/V displacement and width throughout.
