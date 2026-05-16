# Consultation Answers — COPY Operation

**Inquiry:** What is the precise effect of placing existing Istream content at a position in a Vstream? What is preserved about the content's identity, what shifts, and what invariants must the completed operation maintain?
**Date:** 2026-03-21 15:28
**Questions:** 19 (10 nelson, 9 gregory)

---

## Question 1 [nelson]

> When existing content is placed at a position in a document, is the result a reference to the same content or a new independent copy of it?

### Nelson's Answer

## A Reference — Always a Reference

When you place existing content at a position in a document, the result is a **reference to the same content**, not a new independent copy. This is the entire point.

The COPY operation in FEBE creates a new Vstream mapping that points to the **same Istream addresses** as the original. No new bytes are created in permanent storage. The document's virtual byte stream simply includes a reference to bytes that already exist elsewhere:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The placed content **appears** as part of your document — it has an ordinal position in your byte stream "just as if" it were native. But it is not native. It is fetched from its home location when needed. The connection to the original is structural and permanent.

### Why This Matters

This is not a minor implementation detail. It is the architectural foundation that makes everything else work:

1. **Attribution is automatic.** Because the placed content retains its original I-address, you can always trace it back to its home document. "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

2. **Royalties flow correctly.** The original author gets paid when their bytes are delivered, regardless of which document arranges them. "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

3. **No copying means no divergence.** "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

4. **Correspondence is computable.** When two documents share Istream content, the system can identify which parts correspond — enabling version comparison, intercomparison, and refractive link following.

### The Two Operations Compared

| | INSERT | COPY |
|---|---|---|
| **Creates new Istream content?** | Yes | No |
| **Adds to Vstream arrangement?** | Yes | Yes |
| **Content identity** | New I-addresses | Shares source I-addresses |
| **Relationship to source** | None (fresh bytes) | Structural reference |

INSERT is how you create original content. COPY is how you include existing content. The distinction maps directly to the Istream/Vstream separation: INSERT adds to both; COPY adds only to Vstream.

### The Metaphor

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Painted content (INSERT) is yours — new bytes at your I-address. Clear glass (COPY) is a window through to someone else's bytes at their I-address. The reader sees one coherent document. But the system knows exactly which bytes are native and which are inclusions.

### What a "Copy" Loses

If someone were to make an actual independent copy — extracting bytes and re-storing them as new content — they would sever every connection that makes Xanadu valuable:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

The live reference participates in the network. The dead copy does not.

### Delete Does Not Destroy the Reference

Even if the placing document "deletes" the included content from its current version, the original bytes remain in Istream:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The reference can be severed from a particular Vstream arrangement, but the underlying content is permanent and other arrangements that include it are unaffected.

---

**In short:** Xanadu has no mechanism for duplicating content within the system. What looks like "placing content" is always the creation of a new view — a Vstream arrangement — over content that exists once and forever in Istream. The word "copy" in COPY is perhaps unfortunate; "include" or "transclude" better captures what actually happens. The bytes do not move. The bytes do not multiply. A new finger simply points at them.

---

## Question 2 [nelson]

> Does placing content into a document add any new bytes to permanent storage, or does it solely change the document's arrangement?

### Nelson's Answer

## It depends on the operation.

Xanadu has two address spaces, and the answer differs sharply depending on which operation places the content:

### Operations that ADD new bytes to permanent storage (Istream)

**INSERT** and **APPEND** create new content — bytes the user types or provides. These bytes are appended to the Istream (the permanent, append-only store) and simultaneously mapped into the document's Vstream (current arrangement).

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

New bytes get permanent I-addresses encoding their home document. Those addresses never change.

### Operations that ONLY change arrangement (Vstream)

**COPY** is transclusion — it creates a Vstream mapping to *existing* Istream content. No new bytes are created in permanent storage. The included bytes share the same I-addresses as the originals:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Content identity is based on creation, not value. Two users typing identical text independently produce different I-addresses. But COPY shares the original's I-address — that's how the system distinguishes "wrote the same words" from "quoted from the original."

**REARRANGE**, **DELETE**, and **CREATENEWVERSION** also change only the Vstream arrangement. DELETE doesn't remove bytes from Istream; it removes them from the current view:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

CREATENEWVERSION creates a new Vstream arrangement over the same Istream content — effectively a whole-document transclusion.

### Summary

| Operation | New Istream bytes? | Vstream change? |
|-----------|-------------------|-----------------|
| INSERT | Yes | Yes |
| APPEND | Yes | Yes |
| COPY | No — shares existing I-addresses | Yes |
| REARRANGE | No | Yes |
| DELETE | No | Yes (removal) |
| CREATENEWVERSION | No | Yes (new arrangement) |

The architectural insight: a document IS its Vstream-to-Istream mapping. Only operations that bring genuinely new content into existence touch the permanent store. Everything else — quoting, rearranging, versioning, deleting — is purely a change of arrangement over content that already exists and will exist forever.

---

## Question 3 [nelson]

> Must the original content's permanent identity remain unchanged and retrievable at its original address after it is placed elsewhere?

### Nelson's Answer

## Yes — absolutely and by design.

This is one of Xanadu's most fundamental invariants. The original content's permanent identity (its Istream address) **must** remain unchanged and retrievable at its original address after being placed elsewhere. This is not a feature but the architectural foundation on which permanence, attribution, royalties, and link survivability all depend.

---

### The Istream Guarantee

Content lives permanently in Istream. Its address never changes, and the content at that address never changes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The phrase "home locations" is key. Content has a **home** — the document where it was originally created. That home is permanent. When content appears in another document, it is fetched from its home, not duplicated.

### COPY Is Reference, Not Duplication

The COPY operation — the mechanism by which content is "placed elsewhere" — creates a Vstream mapping to existing Istream content. It does **not** create new Istream content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The curated sources confirm: "This is transclusion — the copy shares I-addresses with the source." The destination document gains a virtual reference; the source document's Istream content is untouched.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The word "virtual" is doing essential work. These are not actual copies — they are references that resolve to the original Istream addresses.

### The Original Remains Retrievable

Nelson guarantees that you can always trace back to the source:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is structural, not metadata. The I-address itself encodes the originating server, account, and document. To fetch the content, the system must request it from its home location. The connection **cannot** be severed because the fetching mechanism requires it.

### Even "Deletion" Cannot Remove the Original

If the owner deletes content from their current version, the Istream content persists:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The diagram on page 4/9 shows "DELETED BYTES" as content that is "not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The Istream content is never destroyed.

### The Append-Only Foundation

The entire storage model is built on this principle:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is appended to the permascroll. Nothing is overwritten. Nothing is removed. The I-address is a permanent coordinate in an ever-growing space.

### Why This Must Be So

Four of Nelson's fundamental guarantees depend on this invariant:

1. **Permanence**: "Any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19] — If placing content elsewhere could alter the original, addresses would not be permanent.

2. **Attribution**: The I-address encodes origin. If content were duplicated rather than referenced, the duplicate would have a different I-address, severing the attribution chain.

3. **Royalties**: "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43] — Royalties flow to the owner of the home document. If the original were not retrievable at its original address, the royalty mechanism would break.

4. **Link survivability**: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43] — Links point to I-addresses. If placing content elsewhere could change those addresses, links would break.

### The Metaphor

Nelson's glass-pane metaphor captures this precisely:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

When you look through a window, you see the original — you do not see a copy that replaced it. The original is still there, at its original address, unchanged.

---

### Summary

The answer is **yes**, unconditionally. The original content's permanent identity must remain unchanged and retrievable at its original address after it is placed elsewhere. This is the central architectural invariant of Xanadu — the separation of permanent content (Istream) from mutable arrangement (Vstream). COPY creates references, not duplicates. The original is always at home, always retrievable, always attributable.

---

## Question 4 [nelson]

> If the same content appears in multiple documents through placement, must the system guarantee that all appearances resolve to identical bytes?

### Nelson's Answer

## Yes — and the guarantee is stronger than identity of value. It is identity of instance.

When content appears in multiple documents through the COPY operation (Nelson's "inclusion," "quote-window," or "transclusion"), all appearances resolve to **the same bytes** — not merely equal bytes, but the very same Istream content at the very same permanent address.

### The Architectural Basis

The Istream/Vstream separation makes this a structural invariant, not a runtime check:

1. **COPY creates a reference, not a duplicate.** The COPY operation maps Vstream positions in the target document to existing Istream addresses from the source. No new bytes are created in Istream.

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents." [LM 2/36]

2. **Istream content is immutable.** Bytes at an Istream address never change. The permascroll is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

3. **All appearances fetch from the same home location:**

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When Document A and Document B both include the same passage through COPY, both documents' Vstreams contain mappings to the same Istream addresses. Rendering either document fetches the same bytes from the same location.

### Identity vs. Equality

This distinction matters. Two users who independently type "hello" create **different** Istream bytes at different addresses. Those bytes are *equal* in value but *distinct* in identity. But when one user transcludes the other's "hello," both appearances share the **same** Istream address — they are identical in the strongest sense.

As the provenance documentation captures: "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

This is also how the system knows to pay royalties to the right person and how FINDDOCSCONTAINING works — it traces shared Istream origin.

### The Caveat: Trust, Not Verification

The guarantee is **architectural**, not **cryptographic**. Nelson explicitly specifies no tamper detection:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

If a Storage Vendor is compromised or dishonest, the bytes at an Istream address could theoretically be altered. Nelson's enforcement model relies on contractual trust in the franchise, not on hashes or signatures. The system guarantees identical resolution *given honest infrastructure* — which is the same assumption that makes permanent addresses meaningful at all.

### Summary

The answer is not merely "yes, the system guarantees identical bytes" but something deeper: **there is only one copy.** The COPY operation does not duplicate content — it creates an additional Vstream reference to the same Istream content. Identical resolution is not a property that must be *enforced*; it is a consequence of there being nothing to diverge from. The content exists once; all placements are views of that single instance.

---

## Question 5 [nelson]

> What happens to content already occupying the target position in the document — is it displaced, overwritten, or must the operation only target empty positions?

### Nelson's Answer

Let me check the original pages for the INSERT and COPY operation specifications to give you the most precise answer.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-233.txt</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-234.txt</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-233.png</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-234.png</file_path>
</parameters>
</tool_call>

Content is **displaced (shifted forward), never overwritten**. There is no overwrite operation in Xanadu. This follows from both the explicit operation specifications and the deeper architectural principles.

---

## The Explicit Specification

**INSERT** is unambiguous:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The phrase "increased by the length of the inserted text" is the definition of displacement. Content at and after the target position shifts rightward to make room. Nothing is overwritten.

**COPY** follows the same pattern:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY places transcluded content at a V-address. Since V-addresses form a dense, gapless sequence (positions 1 through N), inserting material at position K necessarily shifts everything from K onward — exactly as INSERT does.

**APPEND** avoids the question entirely:

> "This appends \<text set\> onto the end of the text space of the document \<doc id\>." [LM 4/67]

It targets the position after the last byte. There is nothing to displace.

**REARRANGE** transposes regions — it swaps, not overwrites:

> "Rearrange transposes two regions of text." [LM 4/67]

---

## Why Overwrite Is Architecturally Impossible

Three layers of the design rule out overwrite:

**1. Istream is append-only.** Content in Istream never changes:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Overwriting would require destroying Istream content, which contradicts the append-only guarantee.

**2. Vstream is an arrangement, not a container.** The document's V-stream is a mapping from positions to I-addresses. "Editing" means changing the mapping:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

INSERT changes the mapping by shifting all subsequent V→I entries forward and inserting new entries at the target. DELETE changes the mapping by removing entries and closing the gap. Neither operation touches the underlying I-stream content.

**3. The non-destruction guarantee is absolute:**

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

An overwrite operation would "damage" whatever was at the target position — destroying the V-stream reference to that content. This violates the guarantee. The correct operation is always: INSERT (which preserves everything) plus optionally DELETE (which removes from V-stream only, preserving I-stream).

---

## The Operation Must Only Target Occupied or End Positions

V-stream addresses are always dense — there are no gaps:

> "The digit after the one indicates the byte position in the current ordering of bytes." [LM 4/30]

If a document has 100 bytes, valid V-addresses are 1 through 100 (for targeting existing content) plus position 101 (for appending). There are no "empty positions" to target. Every INSERT goes between or before existing content, shifting what follows.

---

## Summary

| Operation | What happens to existing content at target? |
|-----------|---------------------------------------------|
| **INSERT** | Displaced — V-addresses shift forward by insertion length |
| **COPY** | Displaced — same as INSERT (material inserted at target) |
| **APPEND** | N/A — targets position after last byte |
| **REARRANGE** | Transposed — regions swap positions |
| **DELETE** | N/A — removes from V-stream, gap closes |

There is no OVERWRITE, REPLACE, or PUT operation. If you want to "replace" content, you DELETE the old span and INSERT the new content — two operations, preserving the old content in Istream for historical backtrack.

---

## Question 6 [nelson]

> After placement, if someone examines the document, must the system be able to reveal that the content originated from a specific prior location rather than being freshly authored?

### Nelson's Answer

# Yes — Origin Revelation Is a Fundamental Guarantee

After COPY places content into a document, the system **must** be able to reveal that the content originated from a specific prior location. This is not an optional feature — it is an architectural invariant that follows directly from how COPY works.

## COPY Creates Transclusion, Not Duplication

The COPY operation is defined as:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Critically, **COPY shares I-addresses with the source**. The copied content retains the permanent Istream addresses of the original document where those bytes were created. It does not receive new I-addresses. The destination document's Vstream now maps to I-addresses that belong to another document.

## The System Distinguishes Native from Non-Native Bytes

Nelson explicitly defines two categories of content within any document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

After COPY, the placed content consists of **non-native bytes** — inclusions whose I-addresses encode their home document. The system knows these bytes were not authored here because their I-address tumbler encodes a different `Node.0.User.0.Document` origin.

## The User-Facing Guarantee

Nelson states this as an absolute:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not a "can if you look hard enough" capability. It is a design invariant. For any character in any document, the system reveals its origin.

## Content Identity Is Based on Creation, Not Value

Two documents containing identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words independently" from "quoted from the original":

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The I-address IS the provenance. There is no separate provenance metadata that could be stripped or lost.

## FINDDOCSCONTAINING Operationalizes This

The system provides a dedicated operation for tracing content origin:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This works precisely because COPY preserves I-addresses. The system can find every document that contains bytes from a given source — because those bytes share I-addresses with the source.

## Why This Must Be So

The entire economic and attribution model depends on it. Royalties flow to the original author when their bytes are delivered — which requires the system to know whose bytes they are:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

"Determined automatically" means structurally — from the I-addresses, not from user-supplied metadata. If the system could not reveal that content originated elsewhere, it could not compute royalty splits, could not maintain attribution, and could not support the "step through the window" navigation that lets readers reach the original context.

## Summary

After COPY, examining a document **must** reveal non-native content and its origin. This is not an optional inspection capability but an architectural consequence of how Xanadu works: COPY shares I-addresses, I-addresses encode home documents, and the system always distinguishes native from non-native bytes. The guarantee is structural and unseverable.

---

## Question 7 [nelson]

> Must the source document from which the content originates remain completely unaffected by the placement into a different document?

### Nelson's Answer

## Yes — Absolute Non-Modification of the Source

This is one of the most emphatically stated guarantees in Literary Machines. The source document must remain completely unaffected when its content is placed into another document. Nelson states this principle repeatedly from multiple angles.

### The Explicit Guarantee

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—**without damaging the originals**. This is done by inclusion links." [LM 2/45]

This is not qualified. "Without damaging" means without any modification whatsoever to the source.

### Why It's Structurally Impossible to Affect the Source

Transclusion works by **reference**, not copy. The destination document's Vstream creates a mapping to the source's Istream content. No operation touches the source document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The COPY operation in FEBE inserts a Vstream mapping *in the destination*. The source is read, never written.

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents." [LM 2/36]

### Ownership Forbids It

Even if the system *could* modify the source, ownership rules would prohibit it:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If Bob transcludes from Alice's document, Bob has no authority to modify Alice's document, and the system provides no mechanism by which his transclusion could do so.

### Even In-Links Don't Touch the Source

One might ask: does the *link* created by transclusion modify the source? No. Nelson explicitly separates in-links from the document itself:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

The transclusion link lives in the *destination* document (or wherever the link creator places it). The source document's contents are untouched.

### The Reverse Also Holds

Remarkably, even when the source owner *deletes* content from their own document, the transcluding document is unaffected:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is because deletion only removes Vstream mappings; Istream content is permanent. Both documents operate independently on their own Vstreams over shared Istream content.

### The Glass Pane Metaphor

Nelson's metaphor captures the non-interference precisely:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

You see *through* to the source. Looking through glass does not change what is on the other side.

### Summary

The source document is unaffected in every dimension:
- **Content**: No bytes added, removed, or rearranged
- **Vstream**: No mappings changed
- **Istream**: Immutable by definition
- **Out-links**: Unchanged (transclusion links live elsewhere)
- **Ownership**: Unchanged
- **Version history**: Unchanged

The only effect is *economic*: the source owner's cash register increments when transcluded content is delivered to readers, generating royalty. But that is accounting metadata external to the document, not a modification of the document itself.

---

## Question 8 [nelson]

> Does the act of placing content at a position establish any persistent relationship between the source location and the destination, or is it a one-time arrangement with no ongoing dependency?

### Nelson's Answer

## COPY Establishes a Persistent Structural Relationship; INSERT Does Not

The answer depends entirely on *which* operation places the content.

### INSERT / APPEND: No Ongoing Relationship

INSERT and APPEND create **new native bytes** in the document's Istream. These bytes get fresh I-addresses belonging to that document. There is no source to maintain a relationship with — the content is born here.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

### COPY (Transclusion): Persistent Structural Dependency

COPY does not duplicate bytes. It creates a Vstream mapping that points to the **same I-addresses** as the source. This is not a one-time snapshot — it is an ongoing structural reference.

The persistence manifests in five ways:

**1. Shared identity.** The transcluded bytes in the destination have the *same* I-addresses as in the source document. Two documents containing identical text created independently have *different* I-addresses. Transcluded content shares them. This is how the system distinguishes "wrote the same words" from "quoted from the original."

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

**2. Origin is permanently traceable.** Because the I-address encodes the home document (Node.0.User.0.Document.0.Element), you can always determine where transcluded content came from — not by metadata that could be stripped, but by the address itself.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**3. Discovery works because the relationship persists.** FINDDOCSCONTAINING "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. This operation is only possible *because* the shared I-addresses create an ongoing, queryable relationship between source and destination.

**4. Version correspondence derives from it.** SHOWRELATIONOF2VERSIONS computes which parts of two documents correspond by examining shared I-addresses. This is not metadata — it is a structural property that emerges from the COPY relationship and persists as long as the content exists.

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**5. Royalty accounting depends on it.** The system splits payment between original author and quoter precisely because the shared I-addresses identify who created what:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

### The Retrieval Mechanism Enforces the Dependency

Non-native bytes are not cached copies — they are fetched from their home:

> "All other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This means the destination document *operationally depends* on the source's continued existence in Istream. The relationship is not just bookkeeping; it is the retrieval path.

### Two Modes of Ongoing Relationship

Nelson specifies that transclusions can be either:

- **Location-fixed** (floating in time): updates propagate automatically — you always see the current state of the source
- **Time-fixed**: shows the version at a specific moment, but you can ask "What has this passage become?"

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

Both modes maintain the relationship. The difference is only whether the *view* floats or is pinned.

### Summary

| Operation | Creates new I-addresses? | Ongoing relationship? | Discoverable via FINDDOCSCONTAINING? |
|-----------|-------------------------|----------------------|--------------------------------------|
| INSERT | Yes (native bytes) | No | No — content is native |
| COPY | No (shares source I-addresses) | Yes — structural, permanent | Yes — shared I-addresses are the mechanism |

COPY establishes a persistent, structural, queryable dependency between source and destination. It is not a one-time arrangement. The dependency is encoded in the address system itself and cannot be severed within the system.

---

## Question 9 [nelson]

> If a document contains content placed from two different sources, must the system preserve the distinct origin identity of each portion, or may it treat the combined result as a single undifferentiated span?

### Nelson's Answer

## The system MUST preserve distinct origin identity. This is not optional — it is structural.

### The Architectural Reason

Every byte in Xanadu has a permanent Istream address encoding its home document:

```
Node.0.User.0.Document.0.Element
```

When you COPY (transclude) content from two different sources into your document, each portion retains its original I-addresses. The Vstream arranges them into a contiguous sequence for the reader, but the underlying I-addresses remain distinct. Merging them into one undifferentiated span is architecturally impossible without destroying the addressing model itself.

Nelson states this as a user-facing guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And from the technical specification:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The phrase "home locations" (plural) is significant. Each non-native span has its own home, and retrieval goes back to that home. A compound document with content from two sources necessarily makes two separate requests to two separate homes.

### Identity Is Based on Creation, Not Value

Even if the content from two sources happens to be textually identical, the system treats them as distinct:

Content identity is based on creation origin, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address only when it shares the same origin. This is how the system distinguishes "wrote the same words" from "quoted from the original."

### Why Merging Would Violate Core Guarantees

Treating combined content as a single undifferentiated span would break at least four fundamental mechanisms:

1. **Attribution.** If portions from Source A and Source B were merged, you could no longer "ascertain the home document of any specific word or character" [LM 2/40]. The attribution guarantee is structural — encoded in the I-address — not metadata that could survive a merge.

2. **Royalties.** Different owners receive royalties for their respective content:

   > "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

   "Determined automatically" means from the I-addresses. If the system cannot distinguish which bytes came from which source, it cannot split royalties.

3. **FINDDOCSCONTAINING.** This operation "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. It works by tracing I-addresses. If origin identity were lost, this operation would fail — you could not find which documents share content with a given source.

4. **Correspondence and version comparison.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Correspondence is determined by shared I-addresses. Merging destroys this signal.

### The Glass Pane Metaphor Confirms It

Nelson's metaphor for compound documents makes the separation visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Each window is a distinct opening to a distinct source. The glass pane model has no concept of "merging" two windows into one — each remains a separate transparent region showing content from its specific origin.

### Summary

The system **must** preserve distinct origin identity for each portion. This is not a policy choice but an architectural invariant: the I-address of every byte permanently encodes its home document, and the system's guarantees of attribution, royalty, discoverability, and correspondence all depend on this encoding being preserved through all operations, including composition of content from multiple sources.

---

## Question 10 [nelson]

> Must the completed placement be an all-or-nothing operation — either fully applied with all guarantees holding, or not applied at all — or may it leave the document in a partial state?

### Nelson's Answer

## Atomicity of Placement Operations

Nelson never uses the terms "atomic" or "transaction." But the architecture mandates all-or-nothing through a different principle: **canonical order as an internal mandate**.

### The Canonical Order Mandate

From Nelson's description of Barus's enfilade contribution:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The phrase "internal mandate" is significant — this is not a desirable property but a system invariant. After any change, the structure is in canonical order. There is no acknowledged intermediate state where canonical order is violated.

This is reinforced at the network level:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition." [LM 4/72]

"At all times" and "canonical operating condition" leave no room for partial states.

### Why Partial Application Violates the Architecture

A placement (INSERT, COPY, APPEND) modifies the Vstream mapping. Consider what a partial state would mean:

1. **Vstream density violation.** V-addresses are always dense and contiguous from position 1. A partial insertion would either leave a gap (content placed but V-addresses not updated) or create an overlap (V-addresses shifted but content not yet placed). Neither is a valid Vstream state.

2. **Link coherence violation.** Nelson specifies that after INSERT, "the v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66]. If only some following addresses were shifted, links referencing the unshifted portion would resolve to wrong content — violating the link survivability guarantee.

3. **Part-pounce integrity.** Nelson guarantees that any part of any version can be materialized on demand: "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. A partially-applied placement would produce an incoherent view when pounced upon.

### REARRANGE as Evidence

The REARRANGE operation is especially telling. It "transposes two regions of text" [LM 4/67] — a compound modification (remove region A, remove region B, place B where A was, place A where B was). If this could leave a partial state (one region moved, the other not), the document would contain duplicated or missing content. Nelson describes it as a single FEBE command, implying it completes as a unit.

### What Nelson Specifies vs. What He Leaves to Implementation

**Explicitly specified:** The system is always in canonical order after a change. There is no discussion of partial states, rollback, or recovery from incomplete operations — not because he forgot, but because the architecture doesn't admit them.

**Not specified:** The mechanism by which atomicity is achieved. Whether this is through write-ahead logging, copy-on-write, or some property of enfilade structure is left to the implementor. Nelson designs at the semantic level, not the concurrency-control level.

### My Answer

The completed placement must be all-or-nothing. This follows from the canonical order mandate [LM 1/34], the "at all times unified and operational" requirement [LM 4/72], and the structural properties of the Vstream (dense addressing, link coherence, part-pounce integrity). Nelson does not discuss partial states because his architecture does not admit them — every operation either leaves the system in canonical operating condition or does not happen.

---

## Question 11 [gregory]

> When `docopy` calls `vspanset2sporglset` on the source document, does the conversion split a single V-span into multiple sporgls if the underlying POOM maps that V-range to non-contiguous I-addresses (e.g., after a prior insertion created a gap), and if so, how many DOCISPAN entries does the target receive — one per sporgl or one for the whole operation?

### Gregory's Answer

## KB Synthesis

Yes, the split happens, and the target receives one DOCISPAN entry per sporgl.

**Step 1: vspanset2sporglset splits on I-address contiguity**

[SS-LINK-ENDPOINT] Finding 0037 documents the exact mechanism:

> The conversion chain is: V-span → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → separate I-span per contiguous I-address region → separate sporgl per I-span.

The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) iterates over every I-span returned by `vspanset2ispanset` and creates one sporgl per contiguous I-address region. If the POOM maps a V-range to N non-contiguous I-address regions — whether due to prior insertions interleaving content from multiple sources, or a link orgl allocation creating a gap ([INT-LINK-INSERT] Finding 0063) — then N sporgls are produced from that single V-span input.

**Step 2: insertspanf creates one DOCISPAN entry per sporgl**

[SS-DOCISPAN] Finding 0047 and [ST-COPY] Finding 0047 are direct:

> DOCISPAN entries have per-span granularity, not per-byte. `insertspanf` loops over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct.

> COPY of fragmented source content (3 non-contiguous regions) creates 3 DOCISPAN entries.

The call chain in `docopy` (`do1.c:45-65`) is: `specset2ispanset` (converts V-specs to I-spans, same fragmentation logic) → `insertpm` (updates POOM) → `insertspanf(..., DOCISPAN)` (one `insertnd` per I-span).

**Concrete answer**

If the source V-span maps to N non-contiguous I-address regions:
- `vspanset2sporglset` produces N sporgls
- `insertspanf` makes N `insertnd` calls → N DOCISPAN entries in the target

[INV-SPANF-GROWTH] captures the cost implication: `|new_DOCISPAN_entries| = |ispanset(source_content)|`, proportional to I-space fragmentation, not byte count. Heavily edited source content (many small I-spans) is more expensive to COPY than pristine content (one large I-span).

---

## Code Exploration

I have all the information needed. Here is the full answer.

---

## Tracing `docopy`'s V→I Conversion and DOCISPAN Entry Count

### 1. Premise correction: `docopy` does not call `vspanset2sporglset`

`docopy` [do1.c:45-65] calls `specset2ispanset`, not `vspanset2sporglset`:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)    // do1.c:54
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // do1.c:60
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)      // do1.c:62
```

`vspanset2sporglset` [sporgl.c:35] is called from `specset2sporglset` [sporgl.c:14], which is used exclusively by link operations (`domakelink`, `docreatelink`, `findlinksfromtothreesp`). The two paths are structurally parallel but distinct.

---

### 2. The actual V→I conversion chain

**`specset2ispanset`** [do2.c:14-46] iterates over the specset. For each `VSPECID` item it calls:

```c
vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
// do2.c:36
```

**`vspanset2ispanset`** [orglinks.c:397-402] is a thin wrapper:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

**`permute`** [orglinks.c:404-422] iterates over every V-span in the vspanset, calling `span2spanset` for each one:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex,
                                  targspansetptr, targindex);  // orglinks.c:415
}
```

**`span2spanset`** [orglinks.c:425-454] is where the POOM query happens:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);  // orglinks.c:435

for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);  // orglinks.c:444
}
```

---

### 3. Does a single V-span split into multiple I-spans?

**Yes.** The mechanism is `findcbcinarea2d` [retrie.c:229], called through `retrieverestricted` → `retrieveinarea`:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), &localoffset, ...);  // recurse into children
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);             // retrie.c:263
    }
}
```

`findcbcinarea2d` finds **every leaf crum** whose V-interval intersects the query V-span. If a prior `doinsert` split the mapping — creating two POOM leaf crums at non-contiguous I-addresses that together cover the original V-range — both leaf crums qualify and both produce a separate context entry. There is no merging step anywhere in this path.

Back in `span2spanset`, each context entry is converted by `context2span` [context.c:176] into a single I-span, clipped to the V-restriction bounds, and appended to the output ispanset via `onitemlist`. So **one V-span → N I-spans, one per qualifying leaf POOM crum**.

---

### 4. How many DOCISPAN entries does the target receive?

**One per I-span** — never one for the whole operation.

**In `insertpm`** [orglinks.c:100-132]:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);
    // ...compute crumwidth.dsas[V]...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance vsaptr for next item
}
```

Each I-span produces one `insertnd` call → one new POOM crum in the target document. The vsaptr is advanced by that crum's V-width before the next iteration, so the fragments land at successive but adjacent V-positions in the target.

**In `insertspanf`** [spanf1.c:15-54]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // unpack lstream, lwidth, linfo from each ISPANID item...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
}
```

Same iteration, one `insertnd` on the spanfilade per I-span, all tagged `DOCISPAN`.

---

### Summary

| Step | What happens |
|------|-------------|
| `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` | Queries the source document's POOM via `findcbcinarea2d`, which returns **one context entry per leaf POOM crum** intersecting the V-span |
| `context2span` + `onitemlist` | Each context entry becomes a separate I-span in the ispanset; **no consolidation is performed** |
| `insertpm` loop | Calls `insertnd` once per I-span on the target's POOM; vsaptr advances after each, so fragments are laid consecutively |
| `insertspanf` loop (DOCISPAN) | Calls `insertnd` once per I-span on the spanfilade |

**Conclusion:** If the source document's POOM maps a single V-span to N non-contiguous I-regions (e.g., because a prior insertion interleaved foreign content), `vspanset2ispanset` produces N I-spans. `insertpm` inserts N POOM crums into the target, and `insertspanf` inserts **N separate DOCISPAN entries** into the spanfilade — one per I-region, not one for the whole operation.

---

## Question 12 [gregory]

> When `isanextensionnd` detects that copied I-addresses are contiguous with an existing POOM entry in the target (reach == origin), does the extension silently merge the copy into the pre-existing crum — and if so, is the resulting crum distinguishable from one created by a single bulk insertion of the same content?

### Gregory's Answer

## KB Synthesis

## `isanextensionnd` Merge Behavior and Distinguishability

### Does extension silently merge?

Yes — unconditionally. When `isanextensionnd` at `insertnd.c:293-301` finds both conditions true:
1. `homedoc` of new content matches the existing crum's `homedoc`
2. `new_content.origin == existing_crum.reach` (contiguous)

...the existing crum's width is extended in-place at `insertnd.c:243`. No new crum is allocated, no structural change occurs. The merge is silent — no log entry, no flag, no metadata distinguishing "extended via COPY" from "extended via INSERT." [ST-VCOPY, Finding 0046; ST-INSERT, Finding 0062]

### Is the resulting crum distinguishable from a bulk INSERT?

**Yes, via the `homedoc` field.**

[INV-IADDR-PROVENANCE] establishes that the `homedoc` field records the I-address *origin* document — where INSERT first allocated the content — not the document that last copied it. This field is preserved through extension.

- **Bulk INSERT** into target doc T: allocates fresh I-addresses, creates a crum with `homedoc = T`
- **COPY** from source doc S into target T, extended via `isanextensionnd`: the I-addresses remain native to S, and the crum has `homedoc = S`

Since `isanextensionnd` requires homedoc match as a precondition for extension [ST-VCOPY, Finding 0046], crums from different provenance sources are never merged together — they are created as separate crums. The extension path only fires when copying content from the *same* source document as an already-present crum.

### Observable consequence

The `homedoc` distinction is operationally significant. [ST-INSERT Finding 0033] notes that sequential same-document INSERTs produce contiguous I-addresses that consolidate into a single span on comparison. But [INT-LINK-INSERT, Finding 0063] shows CREATELINK (which allocates into the same granfilade range as INSERT) breaks contiguity. Similarly, COPY-extended and INSERT-native crums will produce **different `compare_versions` results** when compared against their respective source documents: the COPY crum's content shares I-addresses with the source (yields a match), while the INSERT crum's content has fresh I-addresses (yields no match).

### Summary

| | Crum structure | `homedoc` | I-address provenance | `compare_versions` vs source |
|---|---|---|---|---|
| Bulk INSERT | Identical format | Target doc | Native to target | No match |
| COPY (extended crum) | Identical format | Source doc | Native to source | Match |

Once extended, the two crums are structurally isomorphic. The only discriminator is `homedoc`. [INV-IADDR-PROVENANCE]

---

## Code Exploration

Now I have everything needed for a precise answer.

---

## Answer: `isanextensionnd`, Silent Merging, and Distinguishability

### 1. What `isanextensionnd` tests

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

Two conditions must both hold:

1. **Same home document** — `tumblereq` compares the incoming `infoptr->homedoc` against the candidate crum's `c2dinfo.homedoc` (`wisp.h:107-109`: `homedoc` is the only field in `type2dbottomcruminfo`). Different source document → FALSE, no merge.

2. **`reach == origin`** — `prologuend` computes:
   - `grasp = offsetptr + ptr->cdsp` (crum's absolute start)
   - `reach = grasp + ptr->cwid` (crum's absolute end)

   `lockeq` then compares `reach.dsas[0..dspsize-1]` against `originptr->dsas[0..dspsize-1]`. For POOM (`dspsize = 2`, `wisp.h:26`), this compares both the I-dimension and V-dimension simultaneously. The copied content must start at *exactly* the end of the existing crum in both dimensions.

---

### 2. Yes — the merge is silent and in-place

When `isanextensionnd` returns TRUE, the caller `insertcbcnd` (`insertnd.c:249-258`) takes this path:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // line 251
        ivemodified (ptr);
        setwispupwards (father,1);
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);
    }
}
```

Line 251 is the entire merge operation: `dspadd` adds the new `width` into the existing crum's `cwid` field. Then `ivemodified` marks it dirty and `setwispupwards` propagates the width change up the tree. The function returns — **no new crum is allocated**.

The non-extension path (`insertnd.c:260-274`) is never reached:

```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);   // sets offset
movewisp (width, &new->cwid);                                  // sets width
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);            // sets homedoc
ivemodified (new);
setwispupwards ((typecuc*)new, 0);
setwispupwards (father, 1);
splitsomething = splitcrumupwards (father);
rejuvinate (new);                                              // sets age
return(splitsomething);
```

---

### 3. Is the resulting crum distinguishable?

**No.** Here is the complete set of fields in a `type2dcbc` (`enf.h:109-131`):

| Field | Type | Semantics |
|---|---|---|
| `isapex` | bit | tree structure flag |
| `height` | SINT | 0 for bottom crum |
| `cenftype` | SINT | GRAN/SPAN/POOM |
| `modified` | bit | dirty flag |
| `isleftmost` | bit | sibling position |
| `nextcrum`, `prevcrum` | pointers | grim reaper ring |
| `age` | unsigned char | grim reaper hint |
| `leftbroorfather`, `rightbro` | pointers | tree navigation |
| `cwid` | typewid | width (I + V tumblers) |
| `cdsp` | typedsp | offset (I + V tumblers) |
| `c2dinfo.homedoc` | tumbler | source document |

None of these fields record the **history of how `cwid` was accumulated**. After a successful extension:

- `cwid` holds the arithmetic sum of the original width and the extension — identical to what `movewisp` would store for a single bulk insertion of the total span
- `cdsp` is unchanged (set when the crum was first created)
- `c2dinfo.homedoc` is unchanged (the extension gate checks it matches, so it stays)
- `modified` is set — but it would be set in either case

The **only structural difference** is the `age` field. On the extension path, `rejuvinate` is **not** called — the crum keeps its original age. On the new-crum path (`insertnd.c:273`), `rejuvinate(new)` is called to set a fresh age. But `age` is purely an internal grim-reaper scheduling hint (`enf.h:41`); it is not visible via FEBE and carries no semantic content about what I-addresses are stored.

---

### 4. Summary

| Question | Answer |
|---|---|
| Does `isanextensionnd` merge on `reach == origin`? | **Yes** — unconditionally, in-place, via `dspadd` at `insertnd.c:251` |
| Is a new crum created? | **No** — the non-extension path (`createcrum`, `adopt`, `rejuvinate`) is bypassed entirely |
| Is the result distinguishable from a single bulk insertion? | **No** — `cwid`, `cdsp`, and `c2dinfo.homedoc` are identical; no provenance field exists in `type2dcbc`; `age` differs but is invisible to FEBE |

The POOM bottom crum is an opaque interval: it records where a span of I-addresses begins (`cdsp`), how wide it is (`cwid`), and which document they came from (`homedoc`). Whether that width was reached in one shot or via successive contiguous extensions is not recorded anywhere in the struct.

---

## Question 13 [gregory]

> If document A transcludes content from document B, and document C then transcludes that same content from document A, do all three documents' POOMs point to the original I-addresses from B's initial creation — i.e., is transclusion identity preserved transitively through arbitrary copy chains?

### Gregory's Answer

## KB Synthesis

Yes — transclusion identity is preserved transitively through arbitrary copy chains, and all three POOMs point to B's original I-addresses. Here is how the KB entries support this:

## The Mechanism: VCOPY shares, never allocates

When B inserts content, `inserttextingranf` allocates fresh I-addresses α in the granfilade [SS-ADDRESS-SPACE, Finding 0033]. Those I-addresses are permanent [INV-IADDR-IMMUTABILITY].

When A transcludes from B via VCOPY, the call chain is:

```
docopy → specset2ispanset → insertpm
```

`specset2ispanset` reads B's POOM to extract the I-addresses (α) currently mapped there. `insertpm` places those same α into A's POOM without calling `inserttextingranf` [ST-VCOPY, Finding 0046]. No new I-addresses are allocated.

When C transcludes from A, the identical mechanism runs: `specset2ispanset` reads A's POOM, finds α there (because VCOPY placed them there), and `insertpm` writes α into C's POOM.

The sporgl is the carrier that preserves identity through each hop — it packages `(origin: IAddress, width, source_doc)` and passes the origin I-address through unchanged [INT-SPORGL-TRANSCLUSION, SS-SPORGL].

## The Invariant

This is stated directly in [INV-TRANSITIVE-IDENTITY, Finding 0018]:

> Content identity flows transitively through transclusion chains. If A transcludes from B, and B transcludes from C, then A and C share content identity for the transcluded portion — even though A never directly referenced C.

The concrete example:
```
C: "ABCDEFGHIJ"
B: vcopies all of C              → B's POOM maps to C's I-addresses
A: vcopies "DEFGH" from B       → A's POOM maps to C's original I-addresses

compare_versions(A, C) → "DEFGH" shared
find_documents("DEF" from C) → [A, B, C]
```

## Why it cannot fail

Two structural facts preclude identity loss at any hop:

1. **VCOPY never creates new I-addresses.** The only operation that allocates fresh I-addresses is `inserttextingranf`, called only by INSERT [ST-INSERT, Finding 0036]. VCOPY goes through `docopy` → `insertpm`, which writes existing I-addresses into the destination POOM [PRE-COPY, Finding 0046].

2. **I-addresses in the granfilade are immutable and permanent.** DELETE removes POOM mappings but leaves the granfilade untouched [FC-GRANF-ON-DELETE]. No operation can change what content an I-address refers to [INV-IADDR-IMMUTABILITY].

## Depth limit?

The KB records no depth limit on this transitivity for transclusion chains. (There is a separate Bug 0012 crash for deep *version* chains in `compare_versions`, but that is a different operation [EC-COMPARE-VERSIONS-LINK-CRASH, Finding 0018].) For pure transclusion, INV-TRANSITIVE-IDENTITY is stated unconditionally, and the mechanism is purely structural — each hop is identical.

**Summary:** After B→A→C, all three documents' POOMs contain mappings to B's original I-addresses. `compare_versions(B, C)` reports shared content; `find_documents` returns all three from a search against any of those I-addresses. The chain can extend to arbitrary depth without loss.

---

## Code Exploration

Now I have everything I need to trace the complete execution path. Here is my full answer.

---

## Transclusion Identity Through Copy Chains: Is It Preserved Transitively?

**Answer: Yes.** All three documents' POOMs point to the same original I-addresses from B's initial creation, and this holds through arbitrarily deep copy chains. Here is the full proof from source.

---

### Step 1: Original content creation in B

When text is first inserted into B (`doinsert`, `do1.c:87-123`):

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` calls `inserttextgr` (`granf2.c:83-109`), which:
1. Allocates a new permanent I-address via `findisatoinsertgr` → `findisatoinsertmolecule` (`granf2.c:158-181`)
2. Stores text bytes at that I-address in the granfilade
3. Returns `ispanset` — a `typeispan` with `stream = lsa` (the freshly-allocated permanent I-address) and `width = textlength`

Then `docopy(taskptr, docisaptr, vsaptr, ispanset)` is called with those I-spans.

Inside `docopy` (`do1.c:53-64`):
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
...
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

`specset2ispanset` (`do2.c:24-26`) detects `itemid == ISPANID` and passes the I-spans through unchanged:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
```

`insertpm` (`orglinks.c:100-131`) then installs the crum in B's POOM:
```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
movetumbler (&lstream, &crumorigin.dsas[I]);   // I = original granfilade address
movetumbler (vsaptr, &crumorigin.dsas[V]);      // V = position in B
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

**Result**: B's POOM contains a crum mapping `V-address in B → original I-address in granfilade`.

---

### Step 2: A copies from B (FEBE `copy` command)

The client sends `copy(docisa=A, vsa=Y, specset=[B at V=X..X+n])`.

`copy` in `fns.c:41-46` routes to `docopy(taskptr, &docisa_A, &vsa_Y, specset)` where `specset` is a `VSPECID` pointing into B's V-space.

In `docopy`, `specset2ispanset` hits the `VSPECID` branch (`do2.c:27-38`):
```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

`docorgl` is **B's POOM**. `vspanset2ispanset` (`orglinks.c:397-402`) calls:
```c
return permute(taskptr, orgl, ispanptr, V, ispansetptr, I);
```

`permute` (`orglinks.c:404-422`) → `span2spanset` → `retrieverestricted(orgl, span, V, NULL, I, NULL)` (`retrie.c:56-85`). This walks B's POOM looking for crums whose V-dimension intersects the requested V-span, then for each matching crum calls `context2span(c, restriction, V, &foundspan, I)` (`context.c:176-212`):

```c
/* idx1=V (restriction), idx2=I (target) */
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
foundspanptr->itemid = index2itemid (idx2, context);   // → ISPANID
```

`grasp.dsas[I]` and `reach.dsas[I]` come from the POOM crum's stored I-coordinates — the **exact same I-addresses from B's original creation**. These form the returned `ispanset`.

`insertpm` then stores these I-addresses into **A's POOM** at new V-addresses from `vsa_Y` (`orglinks.c:105,113`):
```c
movetumbler (&lstream, &crumorigin.dsas[I]);  // = original I-address from B
movetumbler (vsaptr, &crumorigin.dsas[V]);    // = new V-position in A
```

**Result**: A's POOM crum has `cdsp.dsas[I]` = the original I-address from B's creation.

---

### Step 3: C copies from A (second hop)

Identical machinery. The client sends `copy(docisa=C, vsa=Z, specset=[A at V=Y..Y+n])`.

`specset2ispanset` finds `docorgl` = **A's POOM** and calls `vspanset2ispanset` with A's POOM. The permutation walks A's POOM, whose crums already have `cdsp.dsas[I]` = original I-addresses from B. `context2span` extracts those same I-coordinates and returns them as I-spans.

`insertpm` stores them in **C's POOM** at yet another V-position — but the same original I-addresses.

**Result**: C's POOM crum has `cdsp.dsas[I]` = the original I-address from B's creation.

---

### Why This Is Structurally Inevitable

The POOM is a 2D enfilade that maps V↔I. The V→I permutation (`vspanset2ispanset` → `permute` → `context2span`) **reads I-coordinates out of existing POOM crums**. It never consults the granfilade during a copy — it only consults the source document's POOM. Since copying writes those same extracted I-addresses into the destination POOM, each subsequent transclusion hop reads out the same I-addresses again.

The content allocation only happens once — in `inserttextgr` (`granf2.c:92-108`) — at the moment of original insertion. From that point forward, every `copy` operation is purely a coordinate-space remapping: V-address in source → I-address via source POOM → stored at new V-address in destination POOM.

This means the I-address is **invariant under any number of copy hops**. Documents B, A, C, and arbitrarily many more all have POOM crums whose I-dimension points into the same granfilade storage location.

---

### One Structural Caveat: `rearrangepm`

If document A is rearranged after being copied from B (`dorearrange` → `rearrangepm`, `orglinks.c:137-142`), its V-order changes via `rearrangend`. But rearrangement only moves V-coordinates within the POOM — it does not alter the I-coordinates of existing crums. So when C subsequently copies from A, the permutation still extracts the original I-addresses from the crums, regardless of their new V-positions. Transclusion identity is preserved even across rearrangements.

---

### Summary of the Call Chain

```
B creation:    inserttextgr → alloc I-address → insertpm → B's POOM[V_B → I_orig]
A copies B:    specset2ispanset → vspanset2ispanset(B's POOM) → context2span → I_orig
               → insertpm → A's POOM[V_A → I_orig]
C copies A:    specset2ispanset → vspanset2ispanset(A's POOM) → context2span → I_orig
               → insertpm → C's POOM[V_C → I_orig]
```

The key lines:
- **Allocation (once)**: `granf2.c:94` — `findisatoinsertgr` assigns the permanent I-address
- **V→I lookup**: `do2.c:34-38` — uses the source document's POOM, not the granfilade
- **I extracted**: `context.c:206-207` — `grasp.dsas[I]` from the POOM crum's stored I-coordinate
- **I installed**: `orglinks.c:105` — `movetumbler(&lstream, &crumorigin.dsas[I])` — same value stored in destination POOM

Transclusion identity is preserved completely and transitively through arbitrary copy chains.

---

## Question 14 [gregory]

> When copying a V-span that includes content from multiple original insertions (and therefore multiple contiguous I-address runs), does the ordering of the resulting sporgl entries in the target POOM preserve the source document's V-ordering, or could the 2D enfilade's diagonal-sort rebalancing (`recombinend`) reorder them?

### Gregory's Answer

## KB Synthesis

## Answer: V-Ordering Is Preserved, Rebalancing Cannot Change It

The answer has two independent parts: (1) does insertion preserve V-ordering, and (2) can rebalancing corrupt it?

---

### Part 1 — Insertion Preserves V-Ordering

When `docopy` processes a multi-sporgl copy, the pipeline is:

```
source V-span
  → vspanset2ispanset → permute → span2spanset → retrieverestricted
  → incontextlistnd (insertion-sort by V-address)
  → sporgls in V-sorted order
  → insertpm, one call per sporgl, in that V-sorted order
  → target POOM entries at consecutive target V-positions
```

The critical step is `incontextlistnd` [SS-CONTEXT-LIST, INV-RETRIEVAL-V-SORTED]. It performs explicit insertion-sort by left-boundary V-address (`totaloffset.dsas[V]`) during tree traversal, regardless of sibling order in the source POOM. The resulting sporgl list is always V-sorted before it reaches `insertpm`.

Each sporgl is then placed at a target V-position (source offset mapped to target space). Since the sporgls arrive in V-address order, the target POOM receives them at monotonically increasing V-positions. [ST-INSERT, ST-VCOPY Finding 0046]

---

### Part 2 — Diagonal-Sort Rebalancing Cannot Corrupt V-Ordering

`recombinend` sorts children by diagonal key `cdsp.dsas[0] + cdsp.dsas[1]` before considering merges [SS-ENFILADE-TREE Finding 0071, ST-REBALANCE-2D]. For POOM, dimension 0 = I-space and dimension 1 = V-space. Two sporgls with the same diagonal sum but different individual coordinates (e.g., high-I/low-V and low-I/high-V) could become siblings in any order after rebalancing.

But this does not affect observable results because of [INV-RETRIEVAL-TREE-INDEPENDENCE] and [INV-RETRIEVAL-V-SORTED]:

> "The V-ordering of retrieval results is **independent of the internal B-tree structure**... `incontextlistnd` re-sorts during retrieval regardless of discovery order."

Rebalancing only moves crums between sibling slots. It never changes the `cdsp.dsas[V]` value stored in any individual crum — it only changes which crums are adjacent siblings. When a subsequent query traverses the POOM via `findcbcinarea2d`, it walks siblings in whatever tree order they land in, then `incontextlistnd` insertion-sorts the discovered contexts into V-order before returning.

---

### Summary

| Phase | Mechanism | V-ordering guaranteed? |
|-------|-----------|----------------------|
| Source extraction | `incontextlistnd` insertion-sort | Yes — V-sorted by construction |
| Target insertion | Sporgls inserted in V-sorted order | Yes — positions assigned monotonically |
| Post-insert rebalancing | Diagonal-sort changes sibling order only | Does not affect assignments |
| Retrieval from target | `incontextlistnd` re-sorts unconditionally | Yes — tree-structure-independent |

V-ordering of the copy result is preserved both in the assignments (structural guarantee from insertion order) and in all retrieval operations (query-layer guarantee from [INV-RETRIEVAL-V-SORTED]). The 2D diagonal-sort rebalancing [ST-REBALANCE-2D] is irrelevant to this question — it optimizes merge candidates spatially but cannot change what V-address any crum is responsible for.

---

## Code Exploration

Now I have enough source to answer definitively. Let me trace the full execution path.

---

## Answer

The source document's **V-ordering is fully preserved** in the copy. `recombinend`'s diagonal sort operates only on internal tree nodes and is **coordinate-preserving** — it cannot reorder the semantic (I↔V) mapping of bottom crums.

Here is the chain of evidence, cited line-by-line.

---

### 1. The entry point: `docopy`

`do1.c:45–65` shows the copy pipeline:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (...)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)  // ← the meat
    && insertspanf (...) );
}
```

The specset (source V-specs) is first converted to an I-span set, then passed to `insertpm`.

---

### 2. V→I conversion produces a V-ordered sporgl list

`specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d`:

`retrie.c:252–264`:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // index1 = V
    }
}
```

Each bottom crum that overlaps the source V-span is collected by `incontextlistnd`, which **sorts by V-coordinate**:

`context.c:75–111` — the function walks the list and inserts each new context in ascending V-address order:
```c
// on beginning
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist; *clistptr = c;  return(0);
}
// in middle
for (; nextc = clist->nextcontext; clist = nextc) {
    if ((whereoncontext(clist,...) > ONMYLEFTBORDER)
     && (whereoncontext(nextc,...) < ONMYLEFTBORDER)) {
        c->nextcontext = nextc; clist->nextcontext = c;  return(0);
    }
}
// on end
clist->nextcontext = c;
```

So the resulting context (and therefore sporgl) list is **in ascending V-order** from the source document.

---

### 3. `insertpm` assigns target V-addresses in that V-order

`orglinks.c:100–132`:
```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address of this run
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-address = current vsaptr
    shift = tumblerlength (vsaptr) - 1;
    inc   = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
/**/tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // ← advance vsaptr
}
```

Because `sporglset` is V-ordered (step 2), each successive I-run is given the next sequential target V-address. If the source had runs at V=10 and V=20, they are inserted at Vtarget and Vtarget+10, respectively — preserving document order.

---

### 4. `insertnd` calls `recombinend`; what does it do?

`insertnd.c:70–77`:
```c
if (bothertorecombine || (fullcrumptr->height != oldheight)) {
    recombine (fullcrumptr);
}
```

For a POOM, `recombine` calls `recombinend` (`recombine.c:31`).

`recombinend` (`recombine.c:104–131`):
```c
int recombinend(typecuc *father)
{
    if (father->height < 2 || !father->modified) return(0);
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend (ptr);                  // recurse first

    getorderedsons (father, sons);          // sort sons by diagonal
    n = father->numberofsons;
    for (i = 0; i < n-1; i++)
        for (j = i+1; sons[i] && j < n; j++)
            if (ishouldbother(sons[i], sons[j]))
                takeovernephewsnd (&sons[i], &sons[j]);  // merge subtrees

    if (father->isapex) levelpull (father);
}
```

`getorderedsons` sorts internal-node children by **diagonal magnitude** (`dsas[0] + dsas[1]`):

`recombine.c:296–310`:
```c
for (i = 0; i < n; i++) {
    tumbleradd(&v[i]->cdsp.dsas[0], &v[i]->cdsp.dsas[1], &tarray[i]);
    tarrayp[i] = &tarray[i];
}
// shellsort by that sum
```

This sort determines **which pairs of sibling internal nodes to merge** — it is a storage-efficiency heuristic. It does **not** touch bottom crums.

---

### 5. The merge operations are coordinate-preserving

**`eatbrossubtreend`** (`recombine.c:205–233`) merges bro's children into me by re-linking the sibling pointers, then calling `fixdspsofbroschildren`:

`recombine.c:259–268`:
```c
int fixdspsofbroschildren(typecuc *me, typecuc *bro)
{
    for (nephew = getleftson(bro); nephew; nephew = getrightbro(nephew)) {
        dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);  // make absolute
        dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);   // re-relativize to me
        ivemodified(nephew);
    }
}
```

**`takenephewnd`** (`recombine.c:235–257`) does the same for individual nodes:
```c
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype); // absolute
adopt (nephew, RIGHTMOSTSON, me);
...
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);   // re-relativize
```

In both cases, the nephew/bro's **absolute (I, V) coordinates are preserved**. Only the stored relative displacement (`cdsp`) is updated to reflect the new parent. No crum ever changes its semantic address in the 2D space.

---

### 6. Retrieval never depends on sibling order

POOM retrieval (`findcbcinarea2d`, `retrie.c:229–268`) scans all siblings and uses `crumqualifies2d` / `whereoncrum` for coordinate-based filtering. It does not rely on siblings being in any particular left-to-right order. The result of `recombinend` restructuring has zero impact on what coordinates get returned.

---

## Conclusion

**V-ordering is preserved; `recombinend` cannot reorder it.**

The path is:

1. **`incontextlistnd`** (`context.c:75`) builds the sporgl list in **ascending V-order** from the source.
2. **`insertpm`** (`orglinks.c:100–132`) assigns target V-addresses sequentially to each I-run, preserving the source V-order in the target POOM.
3. **`recombinend`** (`recombine.c:104`) restructures internal POOM nodes using a diagonal-sort to guide merging, but both merge operations (`eatbrossubtreend`, `takenephewnd`) recalculate stored displacements so that every bottom crum's **absolute (I, V) position is unchanged**.
4. POOM retrieval is coordinate-based, not sibling-order-based, so the restructuring is semantically invisible.

The only thing `recombinend`'s diagonal sort determines is which internal subtrees become siblings — a performance question, not a correctness one. The copied content in the target POOM faithfully encodes the source V-ordering across all I-address runs.

---

## Question 15 [gregory]

> For self-transclusion (copying within the same document), if the target V-position falls within the source V-span being copied, what is the resulting POOM state — does the system snapshot the source mapping before applying shifts, or does the shift from `makegappm` alter the source span mid-operation?

### Gregory's Answer

## KB Synthesis

## Self-Transclusion with Target Inside Source Span

The system **snapshots the source mapping before any shifting occurs**. This follows necessarily from the call sequence in `docopy`, combined with the single-threaded execution model.

### Mechanism

`docopy` (`do1.c:45-65`) executes two phases strictly sequentially:

1. **Source read phase**: `specset2ispanset` traverses the POOM to convert the source V-span `[s, s+w)` into I-addresses `i₁..iₙ`. This completes entirely before any modification.

2. **Insertion phase**: `insertpm` → `insertnd` → `makegappm` inserts those I-addresses at target position `t`, constructing a two-blade knife `[t, next_subspace_boundary)` and shifting all POOM entries in that range rightward by `w` [SS-TWO-BLADE-KNIFE, ST-INSERT].

Because the single-threaded event loop guarantees run-to-completion semantics [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH], `specset2ispanset` returns a complete I-address list before `makegappm` touches any POOM entries. The shift in phase 2 does affect the tail of the source span (entries at `[t, s+w)` move to `[t+w, s+2w)`), but those I-addresses were already captured in phase 1.

### Resulting POOM State

For source span `[s, s+w)` → `i₁..iₙ`, target `t` where `s ≤ t < s+w`:

| V-range | Content | Source |
|---|---|---|
| `[s, t)` | original prefix | unchanged (before knife) |
| `[t, t+w)` | **full copy** of `i₁..iₙ` | newly inserted |
| `[t+w, s+2w)` | original suffix | shifted from `[t, s+w)` |
| `[s+2w, ...)` | remainder | shifted from `[s+w, ...)` |

The copy contains the complete source span (captured before the shift), while the original source span is split at `t` with the copy interleaved.

### Caveat

The KB confirms self-transclusion works generally [EC-SELF-TRANSCLUSION] and that the POOM is a multimap tolerating duplicate I-addresses at multiple V-positions [SS-POOM-MULTIMAP]. However, the specific case of target-within-source is not directly tested — the documented self-transclusion scenario uses a target position *after* the source span (Finding 0028 §2, Finding 0039). The answer above is inferred from the `docopy` call sequence and `makegappm` mechanics, not from a golden test of this exact configuration.

---

## Code Exploration

I have all the evidence needed. Here is the full answer.

---

## Self-Transclusion: Source Snapshot vs. `makegappm` Shifts

### Execution Path

The entry point for copy is `docopy` in `do1.c:45`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // ← line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)         // ← line 55
    && acceptablevsa (vsaptr, docorgl)                                   // ← line 56
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // ← line 60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)       // ← line 62
    ...
```

The answer to the question turns on the ordering of these two calls: **`specset2ispanset` runs at `do1.c:54`, before `insertpm` at `do1.c:60`.**

---

### What `specset2ispanset` does: snapshot in I-space

`specset2ispanset` is defined in `do2.c:14`:

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    ...
    for (; specset; ...) {
        if (...VSPECID...) {
            findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
            && (ispansetptr = vspanset2ispanset(taskptr, docorgl,
                    ((typevspec *)specset)->vspanset, ispansetptr))
        }
    }
```

This calls `vspanset2ispanset` (`orglinks.c:397`), which calls `permute` → `span2spanset` → `retrieverestricted`. The result is `ispanset`: a list of **I-spans** (permascroll addresses). These are the permanent, document-independent coordinates for the source content — not V-positions.

**This snapshot is complete and frozen before `insertpm` is ever called.**

---

### What `insertpm` + `makegappm` does: V-shift only

`insertpm` in `orglinks.c:75` loops over the pre-computed `ispanset` (passed in as `sporglset`):

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);   // I-address, I-width
    movetumbler(&lstream, &crumorigin.dsas[I]);           // I-dim: from snapshot
    movetumbler(&lwidth,  &crumwidth.dsas[I]);            // I-dim: from snapshot
    movetumbler(vsaptr,   &crumorigin.dsas[V]);           // V-dim: target position
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);                         // line 131
}
```

`insertnd` (`insertnd.c:15`) is called for the POOM case and immediately calls `makegappm` (`insertnd.c:54`):

```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);  // ← line 54
    ...
    bothertorecombine = doinsertnd(...);             // ← line 57
```

Inside `makegappm` (`insertnd.c:124`), the guard clause first checks whether the target is actually within the document's V-range:

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
|| tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* for extensions to bc without calling cut */
```

If the target V-position is within the document (including within the source span), `makegappm` proceeds. It makes cuts, finds the intersection node, and then classifies each child by `insertcutsectionnd` (`edit.c:207`). Nodes that return `case 1` — meaning they are **to the right of the insertion point** — get their V-displacement shifted:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // line 162
    ivemodified(ptr);
```

This shifts `cdsp.dsas[V]` (the V-displacement) of POOM nodes that are right of the target. It does **not** touch `cdsp.dsas[I]` — I-addresses are untouched.

---

### The Critical Answer

**The system snapshots the source mapping before applying shifts.** Here is why:

1. `specset2ispanset` at `do1.c:54` walks the POOM tree and converts source V-spans to I-spans (permascroll addresses). This produces a fully materialized `ispanset` linked list in task memory.

2. `insertpm` at `do1.c:60` uses this `ispanset` directly. It reads `lstream` and `lwidth` from the pre-computed sporgls — these are the I-coordinates captured before any modification.

3. `makegappm` runs inside `insertnd` and shifts V-displacements of POOM nodes to the right of the insertion point. But the `ispanset` is already in memory; it is not derived from the POOM again. The I-coordinates in the sporgl loop (`lstream`, `lwidth` in `orglinks.c:101–109`) are read from the pre-computed snapshot and are immune to the V-shift.

**When the target V-position falls within the source V-span,** `makegappm` will shift rightward POOM nodes — including nodes that encode the portion of the source span to the right of the insertion point. But because the I-span content was already captured at `do1.c:54`, `insertpm` still inserts the correct permascroll content. After the operation, the part of the original source span that was to the right of the target V-position will occupy a new, shifted V-address in the POOM tree, but the inserted transcluded content correctly references the original permascroll I-addresses.

There is no mid-operation aliasing hazard. The POOM is the mutable structure; the `ispanset` is the immutable content descriptor derived from it before mutation begins.

---

## Question 16 [gregory]

> Does `docopy` advance the document's I-address allocation counter (the high-water mark queried by `findisatoinsertmolecule`), or does the counter remain unchanged because no new granfilade content is created — and if unchanged, does a subsequent text insertion in the target document receive I-addresses that are unaffected by the copy?

### Gregory's Answer

## KB Synthesis

`docopy` does **not** advance the I-address allocation counter. Here is the full reasoning.

## The Allocation Mechanism

The allocator (`findisatoinsertmolecule`) works by querying the granfilade tree for the highest existing I-address below a document-scoped upper bound, then incrementing by 1 [SS-ADDRESS-SPACE, Finding 0061]. There is no cached counter — the high-water mark is derived on-demand from the granfilade tree state.

## What `docopy` Does and Does Not Do

From [ST-COPY] Finding 0064 and [ST-VCOPY] Finding 0046:

- `docopy` calls `insertpm` to add V→I mappings in the **target's POOM** using the source's existing I-addresses
- `docopy` calls `insertspanf` to create DOCISPAN entries in the **spanfilade**
- `docopy` does **not** call `inserttextingranf` or `findisatoinsertgr` — no new content entries are added to the granfilade

The copied I-addresses originate in the source document's namespace. Placing them into the target's POOM does not create new granfilade entries. The granfilade tree, which the allocator scans, is unchanged.

## Consequence for Subsequent Insertions

Because no granfilade content is added, `findpreviousisagr` returns the same maximum I-address before and after the copy. A subsequent INSERT into the target allocates from that unchanged maximum — contiguous with whatever was last directly inserted into the target.

This is confirmed by [INV-MONOTONIC] Finding 0077, which establishes the contiguity-breaking predicate: only operations that call `findisatoinsertmolecule` or `findisatoinsertgr` for content break I-address contiguity. The breaking set is `{INSERT, CREATELINK}`, not `{INSERT, CREATELINK, VCOPY}`. Analogously, CREATENEWVERSION — which uses the same `docopyinternal` / `docopy` pathway — also leaves content I-address allocation unaffected, which is why INSERT → VERSION → INSERT yields one contiguous shared span pair [INV-MONOTONIC, Finding 0077].

## Contrast with CREATELINK

The contrast is explicit in [ST-CRUM-BOUND] Finding 0063: CREATELINK calls `createorglingranf` which allocates a link orgl in the granfilade, advancing the maximum I-address and breaking contiguity for subsequent text INSERTs. `docopy` has no such call and therefore produces no such effect.

## Summary

| Operation | Adds to granfilade content? | Advances allocation counter? |
|-----------|---------------------------|------------------------------|
| INSERT | Yes (`inserttextingranf`) | Yes |
| CREATELINK | Yes (`createorglingranf`) | Yes |
| VCOPY / `docopy` | No | **No** |
| VERSION / `docopyinternal` | No | No |
| DELETE | No | No |

`docopy` leaves the granfilade content space — and therefore the high-water mark queried by `findisatoinsertmolecule` — entirely unchanged. A subsequent INSERT in the target document receives I-addresses contiguous with the target's prior insertions, as if the copy had never occurred [FC-GRANF-ON-DELETE, ST-COPY, INV-MONOTONIC].

---

## Code Exploration

I have the complete call chain. Here is the full answer.

---

## Does `docopy` advance the I-address allocation counter?

**No. `docopy` does not touch the granfilade and therefore cannot advance the counter queried by `findisatoinsertmolecule`. A subsequent text insertion in the target document receives I-addresses entirely unaffected by the copy.**

---

### What `docopy` actually does

`docopy` [do1.c:45–65]:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)

/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)

&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`specset2ispanset` converts the caller-supplied V-specs into **already-existing** I-spans (the source content's I-addresses in the granfilade). No new content is created.

`insertpm` [orglinks.c:75–134] uses those I-spans to insert V↔I mappings into the document's **POOM** (organizational enfilade — the `orgl`):

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

`insertnd` operates on `(typecuc*)orgl` — the POOM — not on the global `granf`. The POOM is a separate POOM-type enfilade that was previously embedded in the granfilade as a `GRANORGL` crum when the document was created. Modifying the POOM's internal structure does **not** add any new crums to the granfilade itself.

`insertspanf` similarly operates on `spanf`, not on the granfilade.

**`docopy` calls `insertseq` on neither the granfilade nor anything that `findpreviousisagr` traverses.**

---

### How the I-address counter actually works

`findisatoinsertmolecule` [granf2.c:158–181] is a static function called only from `findisatoinsertgr` [granf2.c:130–156], which is called only from `inserttextgr` and `createorglgr`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // ... increments lowerbound to get next available address
```

It calls `findpreviousisagr` [granf2.c:255–278], which **recursively traverses the granfilade** looking for the rightmost crum at or below `upperbound`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // granf2.c:264
        return(0);
    }
    for (ptr = findleftson(...); ptr; ptr = findrightbro(ptr)) {
        if (THRUME || ONMYRIGHTBORDER || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // recurse
```

At the leaf level, `findlastisaincbcgr` [granf2.c:280–284] only adjusts the offset for `GRANTEXT` crums:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
}
```

`GRANORGL` crums (document entries) are traversed but do not modify the offset at the leaf. Only actual text content (`GRANTEXT`) written via `insertseq` advances the high-water mark.

---

### The `doinsert` order confirms this

`doinsert` [do1.c:87–123] shows the canonical sequence:

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)   // ① allocates new I-address, writes GRANTEXT to granf
    && docopy (taskptr, docisaptr, vsaptr, ispanset)                   // ② maps that I-span into V-space
```

Step ①: `inserttextingranf` → `inserttextgr` → `findisatoinsertgr` → `findisatoinsertmolecule` — allocates the next I-address and calls `insertseq` [granf2.c:99] to write a `GRANTEXT` crum into the granfilade. **This is the only step that advances the counter.**

Step ②: `docopy` → `insertpm` → `insertnd` on the POOM, plus `insertspanf`. **The granfilade is not touched.**

---

### Conclusion

| Operation | Modifies granfilade? | Advances `findisatoinsertmolecule` counter? |
|---|---|---|
| `inserttextingranf` / `inserttextgr` | Yes — via `insertseq` on `granf` [granf2.c:99] | **Yes** |
| `docopy` → `insertpm` | No — writes to POOM (`orgl`) only [orglinks.c:130] | **No** |
| `docopy` → `insertspanf` | No — writes to `spanf` only | **No** |

**`docopy` advances neither the granfilade's content nor its I-address high-water mark.** The counter is a property of which `GRANTEXT` crums exist in the granfilade; `docopy` adds none. A subsequent `doinsert` (or `inserttextingranf`) in the target document calls `findpreviousisagr` on the same granfilade state that existed before the copy, and allocates I-addresses from the same high-water mark. The copied content's I-addresses are those of the **source** document's (or permascroll's) existing granfilade entries — they live in a different part of the I-address namespace and are invisible to the target document's allocation scan.

---

## Question 17 [gregory]

> When copying a specset containing multiple V-spans from different source documents, does `docopy` process each span independently against its respective source POOM, and does the target receive one contiguous V-range or multiple disjoint ranges corresponding to each source span?

### Gregory's Answer

## KB Synthesis

**Short answer:** `docopy` processes each VSpec against its own source document's POOM independently. The target receives **one contiguous V-range** (starting at the caller-specified insertion point), but the content is stored internally as multiple POOM crums — one per source provenance group — that cannot merge across source-document boundaries.

---

**Processing: each span against its own source POOM**

`specset2ispanset` converts each VSpec to I-spans by looking up V→I mappings in the document named by that VSpec's doc tumbler. Spans from different source documents therefore traverse different POOM trees independently. This is confirmed by the cross-document vcopy scenario in [ST-VCOPY (Finding 0003)]: "Cross-document vcopy works atomically; all spans are placed into the target in a single operation" — atomic here means the whole specset is submitted as one request, not that a single tree lookup handles all sources.

**Target V-addresses: contiguous**

Content from span 1 is placed at `[target_vpos, target_vpos + width₁)`, span 2 at `[target_vpos + width₁, target_vpos + width₁ + width₂)`, and so on in VSpec order [SS-SPECSET], [INV-SPECSET-ORDER]. The result is a single contiguous V-range in the target.

`retrieve_vspanset` confirms this: [INV-VSPAN-CONSOLIDATION] states the enfilade returns maximally consolidated spans, and contiguous V-addresses would be reported as a single span.

**Internal POOM crums: NOT merged across sources**

At the crum level, content from different source documents stays separate. `isanextensionnd()` at `insertnd.c:293-301` requires both V-contiguity AND matching `homedoc` before extending an existing crum. Content transcluded from doc A has a different `homedoc` than content from doc B, so they are stored as separate POOM crums even though their V-addresses are adjacent [INV-IADDR-PROVENANCE]:

> "crums from different source documents are never merged … the extension check's `homedoc` condition means crums from different source documents are never merged"

**Observable consequence**

`compare_versions` between the target and source A reveals only the A-derived portion; between target and source B reveals only the B-derived portion [ST-VCOPY (Finding 0003)]:

> "compare returns TWO shared regions — one per copied span"
> "per-span identity is preserved, not merged into a single region"

So from the caller's perspective the target has one contiguous V-span; from the identity/provenance perspective it has multiple independent I-address records with different origins — which is precisely what enables transitive content tracking [INV-TRANSITIVE-IDENTITY].

---

## Code Exploration

---

## Answer: How `docopy` handles a multi-source specset

### The call chain

`docopy` [`do1.c:45`] executes in two distinct phases:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    typeispanset ispanset;
    typeorgl docorgl;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // Phase 1
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // Phase 2
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) );
}
```

---

### Phase 1 — `specset2ispanset`: each V-span is resolved against its own source POOM

`specset2ispanset` [`do2.c:14`] iterates over all specs in the specset:

```c
for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    ...
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(
          findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
        && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))))
            return (FALSE);
    }
}
```
[`do2.c:27–38`]

For each `VSPECID` in the specset, it calls `findorgl` with that spec's own `docisa`. If the specset has two V-specs referencing document A and document B, `findorgl` is called twice — once with A's ISA, once with B's ISA — yielding two separate POOM `orgl` handles. Then `vspanset2ispanset` (→ `permute` → `span2spanset` → `retrieverestricted`) uses each document's own POOM to translate its V-ranges to I-spans. **Yes: each V-span is processed against its respective source POOM.** The resulting I-spans are all chained into one flat `ispanset` linked list.

---

### Phase 2 — `insertpm`: all I-spans are packed into one contiguous V-range

`insertpm` [`orglinks.c:75`] receives the flat `ispanset` (passed as its `sporglset` argument) and iterates:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);
    shift = tumblerlength (vsaptr) - 1;
    inc   = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
/**/tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);    // ← advances vsaptr
}
```
[`orglinks.c:100–131`]

The critical line is **`orglinks.c:131`**: after inserting each I-span as a POOM crum, `vsaptr` is advanced by that crum's V-width. The next I-span gets the immediately following V-address. There are no V-gaps between spans from different source documents.

**Result: the target document receives one contiguous V-range** from the initial `vsaptr` to `vsaptr + Σ(all copied widths)`, regardless of how many source documents the specset spans.

---

### What about crum merging?

`isanextensionnd` [`insertnd.c:301`] checks whether two adjacent I-spans can be merged into the same POOM crum:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    ...
    return (lockeq (reach.dsas, originptr->dsas, ...));
}
```
[`insertnd.c:305–308`]

The `homedoc` field (from `type2dbottomcruminfo`, `wisp.h:108`) identifies the source document. However, because `docopy` calls `specset2ispanset` (not `specset2sporglset`), the items in the ispanset have `itemid == ISPANID`. When `unpacksporgl` processes an ISPANID item, it **zeroes the homedoc**:

```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler (&((typeispan *)sporglptr)->width,  widthptr);
    tumblerclear (&infoptr->homedoc);    // ← homedoc = 0 for plain I-spans
}
```
[`sporgl.c:180–183`]

Contrast this with the SPORGLID path (used by `specset2sporglset` in `docreatelink`), which does preserve the `sporgladdress` as `homedoc` [`sporgl.c:187`].

So in the POOM crums written by `docopy`, all `c2dinfo.homedoc` fields are zero — the per-span source document identity is not preserved in the target's POOM structure. Spans from different source documents that happen to be I-adjacent (which is impossible since they come from different permascrolls) would be merged; in practice they are stored as separate crums simply because their I-ranges don't abut.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does `docopy` process each V-span against its respective source POOM? | **Yes** — `specset2ispanset` calls `findorgl` with each spec's `docisa` separately | `do2.c:35` |
| Does the target receive contiguous or disjoint V-ranges? | **One contiguous V-range** — `insertpm` advances `vsaptr` after each I-span, packing all spans without gaps | `orglinks.c:131` |
| Is source document identity preserved in the target's POOM? | **No** — `specset2ispanset` produces plain ISPANID items; `unpacksporgl` zeros `homedoc` for ISPANID entries | `sporgl.c:183` |

The design collapses multi-source content into a flat contiguous V-span in the target. The V-space of the target grows by the total size of all copied content, contiguously, but the POOM crums record no memory of which source document each chunk came from.

---

## Question 18 [gregory]

> After a copy places content at V-position `v` in the target, does `find_documents_containing` immediately return the target document for those I-addresses, or is there any scenario (analogous to APPEND's missing `insertspanf` call) where the DOCISPAN entry is not created?

### Gregory's Answer

## KB Synthesis

**Yes — COPY always creates DOCISPAN entries immediately.** There is no scenario analogous to APPEND's omission.

## The Standard Path

All document placement operations that use `docopy` follow the same call chain [ST-INSERT, Finding 0036]:

```
docopy → insertpm (POOM update)
       → insertspanf(..., DOCISPAN) (spanfilade update)
```

This covers:
- **INSERT** (`doinsert` → `inserttextingranf` → `docopy`)
- **VCOPY/COPY** (`docopy` directly)
- **CREATENEWVERSION** (`docopyinternal` → `insertspanf`) [ST-VERSION-CREATE, Finding 0046]

After any of these, `find_documents_containing` returns the target document immediately [ST-INSERT, Finding 0036]:
> `∀ α ∈ new_i_addresses: doc ∈ FINDDOCSCONTAINING(α)`

## The One Exception: APPEND

APPEND (`doappend`) has the `insertspanf(taskptr, spanf, docptr, textset, DOCISPAN)` call explicitly **commented out** — the code comment reads `/*zzz dies this put in granf?*/` [EC-APPEND-NO-DOCISPAN, Finding 0036]. Content added via APPEND is not discoverable through `find_documents`.

## Granularity of DOCISPAN Creation

For COPY specifically, the number of DOCISPAN entries created equals `|ispanset(source_content)|` — one per contiguous I-address run, not per byte [ST-COPY, Finding 0047]. Copying fragmented content (e.g., transcluded from multiple sources) creates multiple entries. Copying contiguous content creates exactly one.

## Monotonicity

Once created, DOCISPAN entries are never removed [INV-SPANF-WRITE-ONLY, Finding 0057]. DELETE does not call any spanfilade function — it modifies only the POOM [ST-DELETE, Finding 0057]. So after COPY, the target document remains discoverable for those I-addresses permanently, even if the content is later deleted from the document's V-stream [INV-IADDRESS-PERMANENT, Finding 0023].

---

## Code Exploration

---

## Answer

**`docopy` unconditionally calls `insertspanf(DOCISPAN)` — there is no scenario analogous to the APPEND omission.**

---

### The COPY Path

`docopy` [do1.c:45–65] is the canonical copy implementation:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // V → I
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)        // open target
&& acceptablevsa (vsaptr, docorgl)                                  // always TRUE [do2.c:112]
&& asserttreeisok(docorgl)
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)         // place in POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // ← DOCISPAN index [do1.c:62]
&& asserttreeisok(docorgl)
);
```

The `insertspanf(..., DOCISPAN)` call at `do1.c:62` is present, uncommented, and runs immediately after `insertpm`. It is **not** analogous to the APPEND situation.

The FEBE `copy` handler at `fns.c:35–47` simply delegates to `docopy`:
```c
if (getcopy(taskptr, &docisa, &vsa, &localspecset)
&&  docopy(taskptr, &docisa, &vsa, localspecset))
    putcopy(taskptr);
```

No interleaving, no alternative path.

---

### What `insertspanf(DOCISPAN)` Does

`insertspanf` [spanf1.c:15–54]:
1. Computes `crumorigin.dsas[ORGLRANGE]` = `prefixtumbler(docisa, DOCISPAN=4, ...)` [line 22] — this encodes the target document's ISA in the ORGL dimension with span-type prefix `4`.
2. For each I-span in `ispanset`, sets `crumorigin.dsas[SPANRANGE]` = the I-address and calls `insertnd` [line 51] to insert a crum into the spanfilade.
3. **Always returns `TRUE`** [line 53], including if `sporglset` is empty.

`finddocscontainingsp` [spanf1.c:151–188] queries this index by:
- Setting `docspace.stream` = DOCISPAN (= 4) via `tumblerincrement(..., 0, DOCISPAN, ...)` [line 168]
- Calling `retrieverestricted(spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, ...)` [line 171] for each I-span

This directly reads the crums written by `insertspanf` in `docopy`. The target document is discoverable **immediately** after the `copy` call returns.

---

### The APPEND Contrast

`doappend` [do1.c:25–32] reads:

```c
return (appendpm (taskptr, docptr, textset)/*&&
   appendpm includes insertspanf!  insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
);
```

The `insertspanf` call is **commented out** in `doappend`. The author's inline note "appendpm includes insertspanf!" is the justification. Tracing the chain: `appendpm` [orglinks.c:17–27] → `doinsert` [do1.c:87–123] → `docopy` [do1.c:45–65] → `insertspanf`. So the DOCISPAN call *does* happen via `docopy` even for APPEND, but the code comment and the omission in `doappend` itself create the misleading impression of a gap. Finding 0036 documents this surface reading.

---

### Edge Cases That Could Suppress the DOCISPAN Entry

The only scenarios where `insertspanf` is not reached in `docopy` are:

1. **`specset2ispanset` fails** [do1.c:54] — the source V-address can't be resolved to I-addresses (e.g., document not open, invalid V-address). The entire operation fails; `docopy` returns FALSE.
2. **`findorgl` fails** [do1.c:55] — the target document doesn't exist or isn't open for write (`WRITEBERT`). Copy fails entirely.
3. **`insertpm` fails** [do1.c:60] — `insertpm` returns FALSE if `vsaptr` is zero [orglinks.c:86–91]. Copy fails entirely.
4. **`ispanset` is empty** — `insertspanf` iterates over `sporglset` [spanf1.c:25]; if the list is empty (e.g., source V-spans resolve to zero I-spans), the loop never executes. `insertspanf` returns TRUE but no crum is inserted. This is a vacuous copy (nothing was placed in the POOM by `insertpm` either), not a partial success.

In none of these cases does `insertpm` succeed while `insertspanf` is skipped. There is no "half-written" state analogous to INSERT writing content to the granfilade but APPEND failing to register it in the spanfilade. The `&&` chain in `docopy` is structurally correct: `insertpm` and `insertspanf` are both required steps, both in the same chain, with no alternative execution path that could omit the second.

---

### Conclusion

After a successful `copy` placing content at V-position `v` in the target document, `find_documents_containing` **immediately** returns the target document for those I-addresses. The DOCISPAN entry is created by `insertspanf` [do1.c:62] as the final step of `docopy`, in a single atomic operation within one FEBE request [bed.c event loop]. There is no scenario analogous to APPEND's missing call where the POOM is updated but the spanfilade index is not.

---

## Question 19 [gregory]

> If the source V-span maps to I-addresses that were originally created in a third document (the source document itself acquired them via an earlier copy), does the DOCISPAN entry in the spanfilade record the immediate source document or the original creating document as the document component of the indexed I-span?

### Gregory's Answer

## KB Synthesis

The DOCISPAN entry records the **destination document** — neither the immediate source nor the original creator.

The mechanism is in `docopy()` at `do1.c:45-65`, which contains the call:

```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The `docisaptr` parameter is the ISA of the document being **written into** (the copy destination). [SS-DOCISPAN, Finding 0036] makes this explicit:

> `do1.c:62` — `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` in `docopy()`

So for a transclusion chain A → B → C:

1. A inserts content (INSERT): DOCISPAN records `I-spans → A`
2. B copies from A (VCOPY): DOCISPAN records `I-spans → B`
3. C copies from B (VCOPY): DOCISPAN records `I-spans → C`

After step 3, `FINDDOCSCONTAINING(I-spans)` returns `{A, B, C}`. Each document accumulated its own DOCISPAN entry at the time it received the content — regardless of where the content originally came from. The spanfilade is append-only [INV-SPANF-WRITE-ONLY], so all three entries persist indefinitely.

This is why [FC-CONTENT-SPANF-ISOLATION, Finding 0018] observes that deleting content from source document A doesn't remove A from `FINDDOCSCONTAINING` results — each DOCISPAN entry is independent and permanent, tied to the destination at copy time. [INV-IADDR-PROVENANCE] separately tracks the *native* (creating) document via the `homedoc` field in POOM crums, but that is distinct from the DOCISPAN index.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Answer

The DOCISPAN entry records **the destination document** (the document receiving the copy) — not the immediate source document, and not the original creating document.

This is not a choice between two alternatives the question offers; the code shows a third answer.

---

### The Full Trace

Call the three documents:
- **A** — the original creator of the content
- **B** — copied from A (immediate source in our scenario)
- **C** — now copying from B (`docisaptr = C`)

#### 1. `docopy` dispatches two operations [`do1.c:53–64`]

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && ...
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // line 62
    );
}
```

`docisaptr` is C throughout. `specset` describes content in B (a V-spec with `docisa = B`).

#### 2. `specset2ispanset` looks up B's POOM to resolve I-addresses [`do2.c:27–38`]

```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
}
```

`((typevspec *)specset)->docisa` is B. `findorgl` opens **B's granfilade (POOM)**. `vspanset2ispanset` → `permute` → `span2spanset` walks B's POOM and produces a set of `ISPANID` spans — raw permascroll I-addresses. These are the same addresses A originally allocated; B's POOM maps B's V-space to them. The returned `ispanset` carries `ISPANID` items — there is no document tag on them, only the permascroll stream/width coordinates.

#### 3. `insertspanf` stores the entry in the spanfilade [`spanf1.c:22–53`]

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22: ORGLRANGE key = C + DOCISPAN
    ...
    for (; sporglset; ...) {
        if (((typeitemheader *)sporglset)->itemid == ISPANID) {
            movetumbler (&((typeispan *)sporglset)->stream, &lstream);
            movetumbler (&((typeispan *)sporglset)->width, &lwidth);
            movetumbler (isaptr, &linfo.homedoc);                   // line 29: homedoc = C
        }
        ...
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
    }
}
```

`isaptr` is the `docisaptr` passed in from `docopy` — it is **C**. Two fields are set from it:

- **`crumorigin.dsas[ORGLRANGE]`** — the enfilade key in the document-ISA dimension, set by `prefixtumbler(isaptr, DOCISPAN, ...)` to C's ISA under the DOCISPAN prefix. This is what `finddocscontainingsp` queries to enumerate documents containing an I-span.
- **`linfo.homedoc`** — the bottom-crum payload field (defined in `wisp.h:108` as `tumbler homedoc` inside `type2dbottomcruminfo`), also set to C's ISA.

The SPANRANGE key (`lstream`/`lwidth`) is the permascroll I-address — the one that A originally allocated when it created the content.

---

### What This Means

The spanfilade records the chain of custody this way:

| When | Spanfilade entry (DOCISPAN) |
|------|----------------------------|
| A inserts content | `(DOCISPAN:A, permascroll-P)` — homedoc = A |
| B copies from A | `(DOCISPAN:B, permascroll-P)` — homedoc = B |
| C copies from B | `(DOCISPAN:C, permascroll-P)` — homedoc = C |

Every document in the copy chain gets its own independent DOCISPAN entry, all pointing to the same permascroll I-address range. The `homedoc` field does not track provenance; it records the receiving document.

The copy provenance (A→B→C) is **not preserved in the spanfilade** at all. What is preserved is the identity of the content itself: the permascroll I-address is invariant across all copies, which is what allows `finddocscontainingsp` to discover every document that includes a given piece of content — they all share the same SPANRANGE key while each has a distinct ORGLRANGE (DOCISPAN) key derived from their own ISA.
