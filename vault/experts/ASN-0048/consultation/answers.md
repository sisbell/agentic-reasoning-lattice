# Consultation Answers — INSERT Operation

**Inquiry:** What happens when new content is added to a document? What is created, what is preserved, and what changes?
**Date:** 2026-03-18 11:18
**Questions:** 18 (8 nelson, 10 gregory)

---

## Question 1 [nelson]

> When new content is added to a document, does the system create a new version of that document, or does the document itself change in place?

### Nelson's Answer

## The document changes in place — but nothing is lost

Nelson's answer is unambiguous: **editing operations modify the document directly**, without creating a new version. But the system's append-only storage ensures every previous state remains reconstructable.

### Two separate operations

The FEBE protocol distinguishes these clearly:

**INSERT** modifies the existing document:
> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

**CREATENEWVERSION** creates a distinct new document:
> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

INSERT, DELETE, REARRANGE, and APPEND all operate on the document's V-space arrangement directly. None of them create new versions.

### How this works without destruction

The key is the I-space / V-space separation:

- **I-space is append-only.** New content is added to permanent storage. Nothing is overwritten.
- **V-space is the current arrangement.** INSERT changes which I-space bytes appear at which positions in the document's virtual byte stream.
- **History is reconstructable.** The system tracks every change chronologically.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

### The "ongoing braid" model

Nelson's metaphor is precise:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The braid is one continuous thing that evolves — not a series of snapshots. Each edit re-twists the braid. The system can reconstruct any prior twist:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

### So what is a "version"?

There are two distinct senses:

1. **Implicit history** — Every prior state of the document is accessible through historical backtrack. These are moments in the braid's evolution, not separate objects.

2. **Explicit version (CREATENEWVERSION)** — A deliberate fork that creates a new document with its own tumbler address, sharing I-space content with the original. This is used for alternative arrangements, published corrections, or branching.

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

### Summary

When you INSERT content into a document, the document itself changes. No new version is created. But the change is non-destructive: new bytes go to I-space (permanent), the V-space mapping updates (current view shifts), and the previous arrangement remains reconstructable. The document is one evolving entity with full history — not a chain of frozen copies.

---

## Question 2 [nelson]

> If a link points to a span of content in the document before the addition, must that link continue to point to exactly the same content afterward?

### Nelson's Answer

# Yes — absolutely and by design.

This is one of Xanadu's most fundamental guarantees. A link must continue to point to exactly the same content after any insertion, deletion, or rearrangement. The mechanism is architectural, not incidental.

## Why: Links Point to Content, Not Positions

Links attach to **bytes** (I-space addresses), not to **positions** (V-space addresses). Nelson is explicit:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

When you insert content into a document, the V-space positions shift — everything after the insertion point gets renumbered:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

But the link doesn't care about V-space positions. It cares about which bytes it is strapped to, and those bytes haven't changed:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## The I-Space / V-Space Separation

This is why the two-address-space architecture exists. I-space addresses are permanent and immutable — a byte's I-address never changes. V-space addresses are ephemeral — they shift with every edit. Links reference I-space, so edits to V-space cannot affect them.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The link's endsets resolve to I-space spans. The document's arrangement (V-space) is a separate mapping that can change freely without disturbing any link.

## The Survivability Guarantee

Nelson states the guarantee directly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

The only condition for a link breaking is if **all** bytes at one of its endsets are deleted. As long as any referenced bytes remain, the link holds. An insertion — adding new content — cannot remove existing bytes, so it cannot break any link. The link continues to point to exactly the same content it always did.

## Summary

| Operation | V-space effect | I-space effect | Link effect |
|-----------|---------------|----------------|-------------|
| **INSERT** | Positions shift after insertion point | No change — new bytes get new I-addresses | **None** — linked bytes unchanged |
| **DELETE** | Gap closes | No change — bytes remain in I-space | Survives if any endset bytes remain |
| **REARRANGE** | Positions change | No change | **None** — linked bytes unchanged |

The answer to your question is not merely "yes" but "yes, and the entire architecture exists to guarantee this." The separation of I-space from V-space, the span-based (not point-based) link model, and the append-only storage design all converge on this single property: **links follow content, not position.**

---

## Question 3 [nelson]

> Does the previous arrangement of the document — the content and its ordering before the addition — remain permanently retrievable as a prior version?

### Nelson's Answer

# Yes — Absolutely and By Design

The permanent retrievability of every prior arrangement is not merely a feature of Xanadu; it is the **foundational storage paradigm**. The entire system is built around the rejection of destructive replacement.

## The Core Guarantee

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

Every prior arrangement — every version, every historical state — remains permanently accessible. You can request "a certain part of a certain version at a certain point in time" and the system reconstructs it.

## Why This Works: I-Space vs V-Space

The mechanism is the separation of **content** (I-space) from **arrangement** (V-space):

- **I-Space** stores content permanently. Bytes at an I-address never change.
- **V-Space** is the document's current arrangement — a mapping from sequential positions to I-space addresses.

When you add content to a document, the new bytes are appended to I-space (getting permanent addresses), and the V-space mapping is updated to include them. But the **previous V-space mapping** — the prior arrangement — is preserved as a version.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

## Append-Only Storage Makes It Inevitable

Nelson explicitly rejects conventional storage:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

His alternative:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, nothing is overwritten. Every change is accumulated. The prior state is not "saved" as a separate copy — it simply *persists* because the system never destroys anything. Reconstruction of any prior arrangement is a matter of replaying the appropriate mappings.

## No "Basic" Version — All Are Equal

There is no privileged "current" version that supersedes others:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

Nelson calls this **prismatic storage**:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another. We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

## Even "Deletion" Preserves Prior State

The delete operation removes content from the current V-space arrangement only. The I-space content remains:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## The User Experience

Nelson envisions users navigating through time as naturally as through space:

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

> "The user must also be able to find his or her notes, look back through time, and study its previous states." [LM 2/15]

The FEBE protocol provides explicit operations for this. `SHOWRELATIONOF2VERSIONS` returns corresponding span pairs between any two versions [LM 4/70], and `RETRIEVEV` can retrieve content from any specific version [LM 4/67].

## Summary

The previous arrangement is **always** permanently retrievable. This is not a convenience feature — it is a structural consequence of append-only I-space storage combined with versioned V-space mappings. The system was designed from the ground up so that no edit, insertion, deletion, or rearrangement can ever destroy a prior state. Nelson called the complete system a **hyperfile** [LM 2/22] — a storage structure that supports not just content but its full version history and the ability to navigate through time.

---

## Question 4 [nelson]

> Can the same content be added to multiple documents simultaneously, and if so, does each addition create separate content or does the system recognize them as the same material?

### Nelson's Answer

# Content Identity: Creation vs. Value

This question goes to the heart of Xanadu's architecture. The answer depends entirely on *how* the content arrives in each document, and the distinction is deliberate and fundamental.

## Two Scenarios, Two Different Answers

### Scenario 1: Independent INSERT into multiple documents

If you type "hello world" into Document A via INSERT, and independently type "hello world" into Document B via INSERT, you have created **two separate pieces of content** with **different I-space addresses**.

The system does **not** recognize them as "the same material." They happen to have identical byte values, but they are distinct content with distinct origins.

From the content provenance design intent:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'"

Each INSERT creates new native bytes in I-space under the target document's control:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

### Scenario 2: COPY (transclusion) from one document to others

If you INSERT "hello world" into Document A, then COPY that content into Documents B and C, all three documents **share the same I-space addresses**. The system absolutely recognizes this as the same material.

The COPY operation is transclusion — it creates a V-space mapping to existing I-space content without creating new bytes:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The curated operations source confirms: "This is transclusion — the copy shares I-addresses with the source."

In Documents B and C, those bytes are "inclusions" or "virtual copies":

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

## Why This Distinction Matters

The I-address is the proof of origin and the basis for:

1. **Attribution** — transcluded content traces back to Document A's owner
2. **Royalties** — when B or C is read, A's owner gets paid for their bytes
3. **Discovery** — `FINDDOCSCONTAINING` finds all documents sharing that I-space content: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]
4. **Correspondence** — version comparison works because shared I-addresses reveal what's the same across documents

If identical text were automatically recognized as "the same," the system would conflate independent creation with deliberate quotation — destroying the distinction between "wrote the same words" and "quoted from the original." That distinction is what makes attribution structural rather than metadata.

## The Architectural Picture

```
Independent INSERT:                  COPY (transclusion):

I-Space:                             I-Space:
  Addr X: "hello world" (Doc A's)      Addr X: "hello world" (Doc A's)
  Addr Y: "hello world" (Doc B's)
                                     V-Space:
V-Space:                               Doc A: [ref X]  (native)
  Doc A: [ref X]                        Doc B: [ref X]  (inclusion)
  Doc B: [ref Y]                        Doc C: [ref X]  (inclusion)

System sees: TWO things              System sees: ONE thing, THREE views
```

## No Simultaneous Multi-Document Operation

The FEBE protocol does not provide a single operation to add content to multiple documents at once. Each INSERT and COPY targets one document. So "adding the same content to multiple documents" is always a sequence: first create it somewhere (INSERT), then share it (COPY). The first step creates content; subsequent COPYs reference it.

This is by design. Content has exactly one home — one I-address, one native document, one owner. The append-only permascroll records it once. Everything else is reference.

---

## Question 5 [nelson]

> Must the system record who performed the addition, and is that authorship attribution permanent and unalterable?

### Nelson's Answer

## Recording and Permanence of Authorship Attribution

### Yes — the system structurally records who performed the addition, and that record is permanent and unalterable

The answer has two layers: **structural origin** (unalterable) and **authorship claims** (disputable).

---

### 1. Structural Origin: Permanent and Unalterable

Every byte created in Xanadu receives a permanent I-space address with the form:

```
Node.0.User.0.Document.0.Element
```

The **User field** encodes which account created the content. The **Document field** encodes which document it was born in. This is not metadata attached to content — it IS the address. To fetch the content, the system must resolve this address, which inherently encodes its origin.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Because I-space is append-only and I-addresses never change, this origin record is **permanent and unalterable**. There is no operation in the FEBE protocol that modifies an I-address after creation. DELETE removes content from V-space (the current arrangement) but leaves I-space untouched. The origin encoding survives all editing operations.

> "Content at an I-address never changes." (derived from the append-only storage model, [LM 2/14])

When content is transcluded into another document, the transclusion references the original I-address — the connection to the creating account cannot be severed:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

---

### 2. What "Who" Means: Account, Not Person

A critical nuance: the I-address records the **account**, not the physical human. Nelson defines the owner as:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)." [LM 2/29]

The parenthetical matters. A publishing company can own a document. An account may represent a person, a company, or (in the case of "John Doe publication") an anonymous walk-in. The structural record is of the account that performed the addition, not a biometric identity.

Nelson also explicitly allows anonymous publication:

> "There is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication.'" [LM 2/60]

Even in this case, the I-address still encodes the account — the bytes came from *somewhere* in tumbler-space. The structural origin is recorded even when the human identity behind the account is unknown.

---

### 3. Author Metalinks: Disputable Social Claims

Separate from structural origin, Nelson defines an **Author metalink** — a link from the author's name to the whole document. This is the social-facing attribution. Critically, it can be contested:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52, footnote]

This means:
- The **structural origin** (I-address encoding account) is unalterable
- The **authorship claim** (Author metalink) is a social assertion that third parties can dispute by creating their own competing Author links

The system does not adjudicate between competing authorship claims. It makes them visible, traceable (each link has a home address identifying who made the claim), and navigable. The user evaluates the competing claims.

---

### 4. Royalty Implications

The permanence of attribution directly serves the royalty mechanism:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The system can determine "who wrote what" precisely because I-addresses permanently encode which account created each byte. Without unalterable origin records, the automatic royalty split would be impossible.

---

### Summary

| Aspect | Recorded? | Permanent? | Alterable? |
|--------|-----------|------------|------------|
| **Structural origin** (I-address: which account created the bytes) | Yes — encoded in address | Yes — I-space is append-only | No — no operation modifies I-addresses |
| **Author metalink** (social authorship claim) | Yes — via Author link | Yes — links persist | Disputable — third parties can create competing claims |
| **Human identity** behind the account | Not guaranteed — anonymous publication allowed | N/A | N/A |

The system **must** record who performed the addition (at the account level), and that record **is** permanent and unalterable. What can be contested is the social interpretation of that record — who the account *represents* — through the Author metalink mechanism.

---

## Question 6 [nelson]

> If the added content was originally composed elsewhere, does the system preserve a connection to its origin, or does addition sever that provenance?

### Nelson's Answer

## Provenance Depends on the Operation

The answer is precisely determined by which FEBE operation adds the content. Xanadu provides two distinct mechanisms, and they differ exactly on this point.

### COPY Preserves Provenance

The **COPY** operation is transclusion — it creates a V-space mapping to the *existing* I-space content rather than creating new bytes:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The "copied" bytes retain their original I-addresses. They are classified as **non-native** content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The provenance is structural — encoded in the I-address itself, which contains the home document's identity:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This connection **cannot be severed** within the system. The I-address of every byte permanently encodes its origin (Node.0.User.0.Document.0.Element). To fetch the content, the system must request it from its home location. Attribution is not metadata that can be stripped — it is the address itself.

### INSERT Severs Provenance

The **INSERT** operation creates **new native bytes** in the document's own I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

If content was originally composed elsewhere — outside the system, or in another document — and is then INSERTed as fresh text, the system assigns it new I-addresses under the receiving document. The connection to its prior existence is severed. The system treats it as original content of this document.

### The Critical Distinction

Content identity in Xanadu is based on **creation**, not **value**. Two documents containing identical text created independently have *different* I-addresses. Transcluded content *shares* the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

This distinction has concrete consequences for the **FINDDOCSCONTAINING** operation:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

COPYed content will be found by this operation (shared I-addresses). INSERTed content will not (new I-addresses, no structural connection).

### The Design Intent

Nelson designed COPY as the proper mechanism for including content from elsewhere *precisely because* it preserves provenance. This is what makes transclusion fundamentally different from traditional copying:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy." [LM 2/48]

The whole architecture pushes users toward COPY (transclusion) and away from INSERT-as-paste, because only the former preserves the web of provenance that makes Xanadu's guarantees work: automatic attribution, royalty flow, origin traceability, and the ability to say "show me what this originally was."

### Summary

| Operation | Provenance preserved? | Content type | I-address |
|-----------|----------------------|--------------|-----------|
| **COPY** | Yes — structurally, permanently | Non-native (inclusion) | Original document's I-address |
| **INSERT** | No — severed at creation | Native (new bytes) | New I-address under receiving document |

If the content was originally composed within the Xanadu system, **use COPY**. If composed outside the system, INSERT is the only option — and provenance to the external origin is not captured by the addressing system. The system preserves connections *within* the docuverse; it cannot create connections to things that never had I-addresses.

---

## Question 7 [nelson]

> Does the act of adding content to a document affect any other document that shares or includes spans from the modified document?

### Nelson's Answer

## No. Adding content to a document does not affect any other document.

This follows directly from the I-space/V-space separation, which is the architectural core of Xanadu.

### Why INSERT/APPEND Cannot Affect Other Documents

**INSERT creates new bytes in I-space with new, unique I-addresses.** Existing bytes — including those transcluded by other documents — retain their permanent I-addresses unchanged.

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The V-stream address shift is **local to the modified document only**. Other documents have their own independent V-space arrangements pointing to specific I-addresses. Those mappings are untouched.

### The DELETE Case Confirms This By Analogy

Nelson is explicit that even the more disruptive operation — deletion — does not propagate:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If deletion from V-space doesn't affect other documents' transclusions, addition to V-space certainly cannot.

### The Architectural Reason

Each document's V-space is an **independent mapping** over shared I-space content:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When document B transcludes content from document A (via COPY), B's V-space records references to specific I-addresses. Those I-addresses are permanent and immutable. Nothing document A does to its own V-space arrangement — inserting, deleting, rearranging — changes the I-space content that B references.

```
Document A (before INSERT):     Document B (transcludes from A):
V-space: [I₁, I₂, I₃]          V-space: [I₂, I₃]

Document A (after INSERT at position 2):
V-space: [I₁, I_new, I₂, I₃]   Document B: still [I₂, I₃]
                                  ↑ completely unaffected
```

### The Window Nuance

Nelson does describe a "location-fixed" windowing mode where a window tracks a position in a changing document, showing whatever is currently there:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

In this mode, what the **window displays** could change if the source document is edited. But this is about the window's **rendering behavior** — what it chooses to show — not about the transcluding document's content being modified. The transcluding document's own V-space mapping and I-space references remain unchanged. The location-fixed window is a front-end presentation concern, not a structural modification to the transcluding document.

### Summary

Adding content to a document:
- Creates new I-addresses (new bytes)
- Shifts V-addresses **within that document only**
- Does **not** alter any I-addresses referenced by other documents
- Does **not** modify any other document's V-space mapping
- Does **not** affect link endsets pointing to the modified document's content

This isolation is not incidental — it is the entire purpose of the I-space/V-space separation. Content identity (I-space) is permanent; content arrangement (V-space) is per-document and independent.

---

## Question 8 [nelson]

> Is there a guarantee that the sequence of all additions to a document is permanently recoverable — not just the current state, but the full history of how the document grew?

### Nelson's Answer

# Yes — with an important nuance about what is guaranteed

Nelson guarantees that **all content is permanently stored** and that **any previous state of a document can be reconstructed**. Together these imply the full growth history is recoverable. But the guarantee is framed as *state reconstruction*, not *operation replay*.

## The explicit guarantee

The strongest statement is on page 2/15:

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

This commits to three things: each change is stored individually, no former change is discarded, and any previous instant is reconstructable.

The append-only storage model is the foundation:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content enters I-space and never leaves. "Deletion" removes content from V-space (the current arrangement) but leaves it intact in I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## The user-facing promise

Nelson promises the user can navigate backward through the full trajectory:

> "The user of such a system may scroll through an individual document, at successive instants of time, alive in the space-time vortex." [LM 2/15]

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The phrase "at successive instants of time" is key — this is continuous history, not periodic snapshots.

## The mechanism: the historical trace enfilade

Nelson designed a specific data structure for this purpose:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

And the underlying enfilade properties ensure that edits preserve canonical order:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

## The nuance

Nelson's guarantee is about **reconstructing states** ("give me this part at this time"), not about **replaying operations** ("show me each INSERT and DELETE in order"). The distinction matters:

- **Guaranteed:** Every byte ever added to I-space persists permanently. Any previous arrangement (V-space state) can be reconstructed. You can scroll through time to see the document at any historical instant.

- **Implied but not explicitly specified:** Whether the system records discrete operation events (INSERT at position 5, DELETE span 7-12) as a replayable log, or whether it stores states from which the operations can be inferred.

The append-only, chronological storage strongly implies that the sequence of additions is implicitly preserved — content arrives in order and is never overwritten. But the FEBE protocol specifies operations (INSERT, DELETE, REARRANGE) as commands to the back end without specifying whether those operations themselves are logged as discrete events.

## Summary

The answer is **yes** — the full history of how a document grew is permanently recoverable. This follows from three interlocking guarantees:

1. **I-space is append-only** — every byte persists forever, filed chronologically
2. **Historical backtrack** — any previous instant can be reconstructed
3. **Non-destruction** — "modifications never damage originals" [LM 2/45]

The document is not a thing that is overwritten; it is "an evolving ONGOING BRAID" [LM 2/14] whose entire trajectory through time is preserved. The guarantee is stated in terms of state reconstruction rather than operation logging, but the effect is the same: nothing is lost, and the full sequence of growth is recoverable.

---

## Question 9 [gregory]

> When `findisatoinsertmolecule` allocates I-addresses for new text, does it scan the entire granfilade subtree under the document's I-address range, or does it use a cached high-water mark — and if it scans, what happens if a CREATELINK has advanced the allocation past the text subrange?

### Gregory's Answer

## KB Synthesis

## `findisatoinsertmolecule`: Scan, Not Cache — and CREATELINK Disrupts It

### It scans the tree on every call

`findisatoinsertmolecule` has no session-local high-water mark. Each INSERT performs a live tree traversal of the granfilade via `findpreviousisagr`, which walks the B-tree to find the highest existing I-address below a document-scoped upper bound, then increments by 1 [SS-ADDRESS-SPACE Finding 0061]:

> *"The allocation is purely derived from current tree state — there is no cached 'next available' pointer. This means allocation is stateless with respect to the session: any session querying the same granfilade tree will allocate identically."*

The upper bound is computed per call from the document ISA hint, scoping the search to the document's allocation subspace [SS-ADDRESS-ALLOC Finding 0065, Finding 0021]. The algorithm: scan down to the bound, take the max, increment by 1. Same pattern for every INSERT, every time.

### CREATELINK advances the text allocation past the text subrange

Link orgls and text characters **share the same monotonic I-address sequence** within a document's allocation space [INT-LINK-INSERT Finding 0063]:

> *"CREATELINK allocates an orgl in the granfilade via `createorglingranf`... This allocation advances the granfilade's maximum I-address. When the next INSERT calls `findpreviousisagr`, it finds the link orgl's I-address as the highest and allocates above it — creating a gap in the text I-address sequence."*

The interaction predicate the KB formalizes: `post(create_link) ⟹ next_text_iaddr > pre(create_link).next_text_iaddr + link_width`.

**Observable consequence**: INSERT "ABC" → CREATELINK → INSERT "DEF" yields **2 shared span pairs** from `compare_versions`, because the I-addresses for "ABC" and "DEF" are non-contiguous — the link orgl occupies the gap between them. Compare with INSERT "ABC" → INSERT "DEF" (no CREATELINK): **1 shared span pair**, contiguous I-addresses.

### VERSION does not disrupt

This is the explicit contrast in [INV-MONOTONIC Finding 0077]:

> *"`CREATENEWVERSION` does NOT break I-address contiguity for subsequent text INSERTs. Unlike CREATELINK, which allocates a link orgl in the content region of the granfilade, VERSION allocates only a document address in a separate tumbler range. The content allocation counter is unaffected."*

Test evidence: INSERT "ABC" → VERSION → INSERT "XYZ" → `compare_versions` returns **1 shared span pair** (contiguous), confirming VERSION doesn't touch `findisatoinsertmolecule`'s allocation space.

### Summary

| Property | Answer |
|----------|--------|
| Cache vs scan | Scan — `findpreviousisagr` on every INSERT |
| CREATELINK effect on text allocation | Disrupts — link orgl advances the granfilade max, gap created |
| VERSION effect on text allocation | None — allocates in a separate document-address range |
| Why | Text and link orgls compete for the same monotonic I-address sequence in the document's granfilade subtree |

Relevant entries: [SS-ADDRESS-SPACE Finding 0061], [SS-ADDRESS-ALLOC Finding 0065], [INT-LINK-INSERT Finding 0063], [INV-MONOTONIC Finding 0077], [ST-INSERT Finding 0033].

---

## Code Exploration

I have everything I need. Here is the full answer:

---

## How `findisatoinsertmolecule` Allocates I-Addresses

### Short answer

**It scans — not with a cached high-water mark.** Every call does a live traversal of the granfilade tree via `findpreviousisagr`. But it is *not* a full subtree scan: it descends a single root-to-leaf path in O(tree-height) time. And CREATELINK cannot contaminate text allocation because the two subranges are bounded by non-overlapping `upperbound` values computed at call time.

---

### 1. The allocation path: always a live scan

`findisatoinsertgr` [granf2.c:130] calls `findisatoinsertmolecule` for all `ATOM`-subtype hints:

```c
// granf2.c:142
findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

Inside `findisatoinsertmolecule` [granf2.c:158-181]:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));                                       // line 163
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    ...
```

`lowerbound` is zeroed fresh every call [granf2.c:163]. There is no field read from a cache or from the crum/node structure. The result comes entirely from `findpreviousisagr`.

---

### 2. What `findpreviousisagr` actually does (single path, not full subtree)

`findpreviousisagr` [granf2.c:255-278]:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
  INT tmp;
  typecorecrum *ptr, *findleftson();

    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // line 264 — leaf: finalize
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // line 272 — descend and return
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // line 275 — accumulate
        }
    }
}
```

The loop at each internal node walks children left to right:
- If a child's span is entirely to the **left** of `upperbound` (below it), its width is added to `offset` [line 275] and we advance to the next sibling.
- As soon as a child's span **straddles** `upperbound` (`THRUME`) or **borders** it (`ONMYRIGHTBORDER`), or there is no right sibling (`!ptr->rightbro`), we recurse into that child [line 272] and immediately return.

At the leaf, `findlastisaincbcgr` [granf2.c:280-284] adds `textlength - 1` to `offset` if the crum is a `GRANTEXT` node, so `offset` ends up pointing at the last character of the last text run straddling `upperbound`.

This is a **single root-to-leaf descent** — O(tree height) — not a full subtree scan. All siblings to the right of the descent path are skipped; only siblings to the left are accumulated into `offset`.

---

### 3. How the `upperbound` is computed — and why subranges don't cross

The constants [xanadu.h:145-146]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

`tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` [granf2.c:162] places `atomtype + 1` two levels below `hintisa` in the tumbler hierarchy (rightshift=2 means appending two more sub-levels):

| Call context | atomtype | `upperbound` |
|---|---|---|
| Text insert (`doinsert`, `do1.c:117`) | TEXTATOM = 1 | `docisa.0.2` |
| Link create (`docreatelink`, `do1.c:207`) | LINKATOM = 2 | `docisa.0.3` |

Actual allocated addresses:
- First text atom: `docisa.0.1.1` (TEXTATOM=1 at depth+2, then +1 at depth+3)
- Subsequent text: `docisa.0.1.2`, `docisa.0.1.3`, …
- First link: `docisa.0.2.1` (LINKATOM=2 at depth+2, then +1 at depth+3)
- Subsequent links: `docisa.0.2.2`, `docisa.0.2.3`, …

In tumbler ordering, with `docisa` ending at mantissa position `L`:
- Text items have mantissa[L+1]=1, mantissa[L+2]=N → all less than `docisa.0.2` (which has mantissa[L+1]=2, mantissa[L+2]=0)
- Link items have mantissa[L+1]=2, mantissa[L+2]=M → all greater than `docisa.0.2`

Therefore the text `upperbound` (`docisa.0.2`) sits exactly at the **seam** between the two subranges: every text address is below it, every link address is above it.

---

### 4. What happens if CREATELINK has advanced allocation past the text subrange

**Nothing.** The text `upperbound` is not derived from any state — it is always `hintisa.0.2`, computed fresh from the document's own I-address. Link addresses at `docisa.0.2.M` are all strictly greater than `docisa.0.2`. When `findpreviousisagr` runs for a text insert with `upperbound = docisa.0.2`, it will never descend into or accumulate past any node whose span lies in `docisa.0.2.*`, because `whereoncrum` will return `TOMYRIGHT` for those nodes (they start after `upperbound`).

The text allocator is structurally blind to the link subrange.

---

### 5. The LINKATOM branch handles the cross-range `lowerbound` explicitly

Because the link `upperbound` is `docisa.0.3` (above both subranges), `findpreviousisagr` for a link allocation *can* return a text address as `lowerbound` if no links exist yet. The LINKATOM branch in `findisatoinsertmolecule` [granf2.c:170-175] accounts for this:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);    // tentative = docisa.0.2
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);            // first link → docisa.0.2.1
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);      // next link → lowerbound+1
}
```

- `tentative = docisa.0.2` — the start of the LINKATOM subrange [granf2.c:171]
- If `lowerbound < tentative` (e.g., `lowerbound` is a text address), it means no links exist yet → first link gets `docisa.0.2.1` [granf2.c:172-173]
- If `lowerbound >= tentative` (it's already a link address), next link gets `lowerbound + 1` [granf2.c:175]

So even though LINKATOM's `upperbound` encompasses the text subrange, the allocation logic re-anchors to `docisa.0.2` as the base of the link subrange, correctly ignoring any text addresses returned by the scan.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Cached high-water mark? | No. `lowerbound` is zeroed on every call. | `granf2.c:163` |
| Full subtree scan? | No. Single O(height) root-to-leaf descent. | `granf2.c:267-277` |
| What does the scan traverse? | The rightmost path straddling `upperbound`; left siblings are accumulated, right siblings skipped. | `granf2.c:275` vs `granf2.c:272` |
| Can CREATELINK advance text allocation? | No. Text `upperbound = docisa.0.2`; link addresses are all > `docisa.0.2`. | `granf2.c:162`, `xanadu.h:145-146` |
| Does LINKATOM search see text addresses? | Yes (its `upperbound = docisa.0.3`), but the branch logic discards them by re-anchoring to `docisa.0.2`. | `granf2.c:171-175` |

---

## Question 10 [gregory]

> In `makegappm`, the V-shift applies `tumbleradd` to every POOM entry at or after the insertion point — does this shift walk the entire tree rightward from the insertion point, or does it exploit the enfilade's displacement-based addressing to apply the shift at an upper crum level without touching every bottom crum?

### Gregory's Answer

## KB Synthesis

The KB is explicit on the mechanism but requires synthesizing across several entries.

## Short answer

`makegappm` exploits the 2D enfilade's **displacement-based addressing** to shift entire subtrees by modifying a single ancestor crum's `cdsp.dsas[V]` field — it does **not** walk every bottom crum. This is the core efficiency property of the enfilade.

## Evidence

**Relative displacement encoding** [SS-ENFILADE-TREE, Finding 0066]:

> Children's displacements are stored relative to the root, not as absolute positions. … `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`

When `insertcutsectionnd` applies `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` at `insertnd.c:162`, modifying an upper crum's displacement implicitly shifts the absolute position of every crum in its subtree **without touching the subtree's children**. This is the point of the displacement hierarchy — a single field update propagates through all descendants via the additive traversal formula.

**How the knife interacts with the tree** [SS-TWO-BLADE-KNIFE, SS-WHEREONCRUM, Finding 0062]:

`insertcutsectionnd` classifies each crum it encounters during tree traversal using `whereoncrum()`. When an entire subtree's range falls strictly within `[blade[0], blade[1])` (case 1, THRUME), the shift is applied to that subtree's root crum and the traversal does not descend further into it. Only crums that **straddle** a blade boundary require descent to a lower level — these are the crums where `whereoncrum()` returns `ONMYLEFTBORDER` or `ONMYRIGHTBORDER`, which trigger `slicecbcpm` to split the crum before reclassifying the pieces [PRE-DELETE, Finding 0075, same mechanism applies in the insert cutting path].

**The normalization step** [ST-INSERT, Finding 0066]:

After `makegappm` applies shifts and `insertnd` places the new content, `setwispupwards` recalculates the root's `cdsp` by finding the new minimum displacement across all children and adjusting sibling displacements to remain relative. This is `setwispnd` absorbing the new minimum:

> `setwispnd` finds `mindsp = min(old_root.cdsp, new_position)`, absorbs: `root.cdsp = 0 + 2.1 = 2.1`, child adjusted: `child.cdsp = 2.1 - 2.1 = 0`

This normalization pass visits immediate children of each upper node, not all bottom crums.

## Implication

The shift is O(log N) in the number of crums affected, not O(N). Only crums at tree levels where a knife boundary cuts through a crum's range require descent — crums whose entire subtree falls in one section get the shift applied at their level. The displacement hierarchy propagates the shift downward for free during subsequent reads via the grasp computation `grasp = offset + ptr->cdsp` [SS-WHEREONCRUM, `retrie.c:334-339`].

---

## Code Exploration

Now I have everything needed for a complete answer. Here it is:

---

## Answer

The V-shift in `makegappm` **exploits displacement-based addressing**. It does not walk the entire tree rightward; it modifies only the displacement fields of direct children of the root crum, and the shift propagates to all their descendants implicitly through position accumulation. Here is the full traced evidence.

---

### 1. `newfindintersectionnd` always returns the root

The function that identifies which node to operate on is at `ndinters.c:38-42`:

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;       // always the root
    clear(offset, sizeof(*offset));
}
```

This is a simplified stub. The original `findintersectionnd` (commented out at `ndinters.c:19-37`) would have descended the tree to find the deepest common ancestor of all nodes spanning the cut. The current implementation unconditionally sets `father = fullcrumptr` (the root). As a result, the shift loop in `makegappm` always operates on the root's direct children.

---

### 2. The shift loop only touches direct children of the root

From `insertnd.c:149-168`:

```c
prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 0:
      case 2:
        break;
      case -1:      /* THRUME */
        gerror("makegappm can't classify crum\n");
        break;
      case 1:       /* 9-17-87 fix */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
        ivemodified(ptr);
        break;
    }
}
```

The loop iterates over **direct children of `father` (the root)** via `findleftson` / `findrightbro`. There is no recursion, no descent. The number of iterations is bounded by `MAXUCINLOAF = 6` (`enf.h:26`). Only children classified as `case 1` have their `cdsp.dsas[V]` modified — no grandchildren, no bottom crums.

---

### 3. Every crum stores a relative displacement; absolute position is accumulated

From the struct definitions in `enf.h:47-48` (same layout in `typecuc`, `typecorecrum`, `typecbc`):

```c
typewid cwid;   // width in each dimension: range of addresses this crum covers
typedsp cdsp;   // displacement: offset from the parent's context
```

From `prologuend` at `retrie.c:336-338`:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, ...);    // absolute start = parent_grasp + cdsp
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, ...); // absolute end = grasp + cwid
}
```

A bottom crum's absolute V-position is the **sum of all `cdsp.dsas[V]` values along the path from root to leaf** — exactly like a displacement tree or finger tree. When `makegappm` does:

```c
// insertnd.c:162
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

...on an internal (upper-crum) child of the root, **all bottom crums in that child's subtree are implicitly shifted by `width` in V-space**, without any of them being touched. There is no explicit visit to any descendant.

---

### 4. How `insertcutsectionnd` selects which children to shift

Before the loop, `makecutsnd` (`ndcuts.c:15-31`) splits the tree at two knife positions:

```c
// insertnd.c:144-148
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```

`blade[0]` is the insertion address; `blade[1]` is a companion point computed from the same address's tumbler structure (designed to provide a clean gap boundary — the comment at `insertnd.c:175` says "for text is 2.1"). After `makecutsnd`, no node spans either cut; each child of the root lies cleanly in one interval.

`insertcutsectionnd` (`edit.c:207-233`) then classifies each child:
- **case 0** — crum is entirely to the left of `blade[0]` → skip (already in place)
- **case 1** — crum starts at or after `blade[0]` but before `blade[1]` → **apply V-shift**
- **case 2** — crum starts at or after `blade[1]` → skip
- **case -1** — crum spans a cut (THRUME) → error

The children that fall in the post-cut interval starting at `blade[0]` receive the shift; their entire subtrees are implicitly moved with them.

---

### 5. The shift logic is the same pattern used for `deletend`

For comparison, `deletend` (`edit.c:31-76`) uses the same blade-and-classify pattern. For delete, `case 2` children (right of the deleted range) have their displacement decremented by `width`:

```c
// edit.c:63
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

Again: only a small number of upper-level nodes are touched; the shift propagates to bottom crums for free.

---

### Conclusion

The V-shift in `makegappm` is **not** a rightward scan of all bottom crums. It is a constant-width sweep over the direct children of the root (bounded by `MAXUCINLOAF = 6`). For each qualifying child, it modifies only that child's V-displacement (`cdsp.dsas[V]` at `insertnd.c:162`). Because every crum's absolute V-address is computed by accumulating displacements up the tree (`prologuend`, `retrie.c:336`), this single displacement update implicitly shifts the entire subtree beneath that child — which may contain arbitrarily many bottom crums — without visiting any of them.

The one caveat is that `newfindintersectionnd` (`ndinters.c:38-42`) has been simplified to always return the root rather than descending to the deepest common ancestor. The older commented-out version would have found a deeper `father`, which would be a more targeted (but still displacement-based) operation. Even with the simplified version, no bottom crums are ever visited; the O(bottom-crums-to-the-right) walk is entirely avoided in both versions.

---

## Question 11 [gregory]

> The `isanextensionnd` coalescing check uses reach-equals-origin adjacency to merge a new insertion into an existing bottom crum — does this coalescing ever fire across a prior DELETE boundary, where two formerly non-adjacent I-spans became adjacent in V-space after intervening content was removed?

### Gregory's Answer

## KB Synthesis

No. `isanextensionnd` coalescing cannot fire across a DELETE boundary. Here is why each part of the mechanism prevents it.

---

## What the coalescing check actually tests

From [ST-INSERT] (Findings 0046, 0062): `isanextensionnd` fires only when two conditions hold simultaneously:

1. The new content has the same **homedoc** as the candidate crum
2. The new content's **I-address origin** equals the candidate crum's **I-address reach**

This is an **I-space adjacency test**, not a V-space adjacency test. Two crums can become V-adjacent after DELETE without triggering coalescing, because what matters is whether the new content's allocated I-address picks up exactly where an existing crum leaves off.

---

## Why DELETE cannot create that I-space condition

**I-address allocation is monotonically increasing and non-reusing** [INV-MONOTONIC], [INV-NO-IADDR-REUSE] (Findings 0033, 0061): Every new INSERT draws from `max_iaddr(granf) + 1`. Deleted I-addresses remain permanently allocated in the granfilade [FC-GRANF-ON-DELETE] — DELETE never modifies the granfilade, so the allocation frontier never retreats.

Consider the concrete scenario:

```
INSERT "ABCDE" → crum₁: V[1.1, 1.6) → I.1..I.5, reach = I.6
DELETE [1.3, 1.6) → removes right half of crum₁
  granfilade: still contains I.1..I.5 (frontier = I.5)
  POOM: only crum₂: V[1.1, 1.3) → I.1, I.2, reach = I.3

INSERT "X" at V 1.3:
  Allocates I.6 (next after granfilade max I.5)
  isanextensionnd: I.6 == crum₂.reach(I.3)? → NO
```

The deleted content (I.3–I.5) is still allocated in the granfilade, so the next INSERT gets I.6, not I.3. The surviving crum's reach (I.3) will never equal a future allocation because the frontier has already passed it.

**I-addresses of surviving crums are immutable** [INV-IADDR-IMMUTABILITY] (Finding 0030, 0064). The reach of `crum₂` remains I.3 regardless of subsequent operations. And since all future allocations are strictly greater than the current granfilade maximum (I.5), and I.5 > I.3, no future new content can produce an origin equal to I.3.

---

## The one case coalescing does fire

Coalescing fires only when new content is allocated at exactly the point where the previous allocation ended — i.e., **consecutive inserts with no intervening I-address-consuming operation** [ST-INSERT] (Finding 0062, 0063). CREATELINK breaks this by advancing the frontier [INT-LINK-INSERT] (Finding 0063). DELETE cannot create such an opportunity because it consumes no I-addresses and cannot rewind the frontier.

---

## Summary

The monotonic, non-reusing I-address allocator is the decisive constraint. After DELETE, the granfilade maximum reflects all I-addresses ever allocated (including deleted content), so any subsequent INSERT gets an address above that maximum. A surviving crum's reach is always below that maximum (it was set when those I-addresses were allocated). The two values cannot meet, so `isanextensionnd` cannot fire across a DELETE boundary.

**Relevant entries:** [ST-INSERT], [INV-MONOTONIC], [INV-NO-IADDR-REUSE], [INV-IADDR-IMMUTABILITY], [FC-GRANF-ON-DELETE], [INT-LINK-INSERT]

---

## Code Exploration

I have all I need. Here is the full analysis.

---

## Does `isanextensionnd` Coalescing Fire Across a Prior DELETE Boundary?

**Short answer: Yes — but only when a subsequent INSERT arrives at a position whose 2D reach-coordinates exactly match an existing crum, and the V-adjacency was created by the delete. The delete itself causes no spontaneous coalescing.**

---

### 1. The Function

**`insertnd.c:301-309`**

```c
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

Two conditions must both hold:

1. **Homedoc match** (`insertnd.c:305`): `tumblereq` on the home-document ISA of the existing crum vs the new insertion's `infoptr->homedoc`.
2. **Full 2D reach-equals-origin** (`insertnd.c:308`): `lockeq` walks `dspsize(ptr->cenftype)` tumblers.

For POOM and SPAN, `DSPSIZEPM = DSPSIZESP = 2` (`wisp.h:24-26`), and the axes are `I=0`, `V=1` (`wisp.h:19-20`). So `lockeq` checks **both** `reach.dsas[I] == originptr->dsas[I]` AND `reach.dsas[V] == originptr->dsas[V]` simultaneously.

`prologuend` computes reach as `offset + cdsp + cwid` in both dimensions (`retrie.c:334-338`):

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach) {
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`lockeq` itself (`wisp.c:261-266`):

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize) {
    while (loxize--)
           if (!tumblereq (lock1++, lock2++))
                    return(FALSE);
    return (TRUE);
}
```

The coalescing site is `insertcbcnd` (`insertnd.c:249-258`): it scans all bottom-crum siblings of the insertion point, and on the first hit widens the existing crum in place:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // insertnd.c:251
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

---

### 2. What DELETE Does to the Tree

`dodeletevspan` (`do1.c:158-167`) calls `deletevspanpm` (`orglinks.c:145-152`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` is called with `index = V`. It cuts the tree, then for each surviving bottom crum at the intersection (`edit.c:47-73`):

```c
switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
  case 1:  disown (...); subtreefree (...); break;          // entirely inside range — gone
  case 2:  tumblersub (&ptr->cdsp.dsas[index], width,       // edit.c:63
                       &ptr->cdsp.dsas[index]);             // V-origin shifted LEFT by width
           break;
}
```

**`index = V`, so only `cdsp.dsas[V]` is modified. `cdsp.dsas[I]` is left untouched.**

After the loop, `deletend` calls `recombine(father)` (`edit.c:75`).

---

### 3. What `recombine` Does (and Does NOT Do) After Delete

`recombine` dispatches to `recombinend` for POOM/SPAN (`recombine.c:22-34`). `recombinend` (`recombine.c:104-131`):

```c
int recombinend(typecuc *father) {
    if (father->height < 2 || !father->modified) return(0);
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend(ptr);                                   // recurse
    getorderedsons(father, sons);
    n = father->numberofsons;
    for (i = 0; i < n-1; i++)
        for (j = i+1; ...; j++)
            if (ishouldbother(sons[i], sons[j]))
                takeovernephewsnd(&sons[i], &sons[j]);      // structural rebalance only
    if (father->isapex) levelpull(father);
}
```

`ishouldbother` checks only capacity: `dest->numberofsons + src->numberofsons <= MAX2DBCINLOAF` (`recombine.c:162`). `takeovernephewsnd` / `eatbrossubtreend` / `takenephewnd` move **internal nodes** between parents — they adjust `cdsp` offsets and re-adopt subtrees, but they never inspect homedoc fields or call `isanextensionnd`. **`recombinend` is structural tree-balancing, not semantic I-span merging.**

**Consequence: after `deletend`, two bottom crums that are now geometrically adjacent remain as separate crums. There is no post-delete coalescing pass.**

---

### 4. Can Coalescing Fire Across the DELETE Boundary?

**Yes — on a subsequent INSERT, under the right geometry.**

The critical constraint is that `lockeq` (`insertnd.c:308`) checks **all two dimensions** of `reach` vs `origin`. A V-delete (`index = V`) shifts only `cdsp.dsas[V]`, never `cdsp.dsas[I]`. So for coalescing to fire after a delete:

- **V-adjacency** must be created by the delete (the rightward crum's V-origin shifts into contact with the leftward crum's V-reach).
- **I-adjacency** must independently hold (the two crums must already have matching I-reach / I-origin, since the delete never alters I-coordinates).

**Concrete geometry:**

Before delete, let two crums exist with the same homedoc H:
- Crum A: `cdsp=(3,1)`, `cwid=(2,2)` → I=[3,5), V=[1,3), reach=(5,3)
- Crum C (intervening, homedoc≠H): `cdsp=(5,3)`, `cwid=(2,2)` → V=[3,5)
- Crum B: `cdsp=(5,5)`, `cwid=(2,2)` → I=[5,7), V=[5,7), homedoc=H, grasp=(5,5)

Note A.reach_I = 5 = B.grasp_I (already I-adjacent), but A.reach_V = 3 ≠ 5 = B.grasp_V (V-non-adjacent due to C).

**After `deletevspanpm` at V=[3,5):**
- C is entirely within the deleted V-range → `case 1` → removed
- B falls to the right of the deleted range → `case 2`: `cdsp.dsas[V] -= 2` → B is now `cdsp=(5,3)`, `cwid=(2,2)` → I=[5,7), V=[3,5)

Post-delete state:
- A: reach = **(5, 3)**
- B: grasp = **(5, 3)**  ← now both V-adjacent AND I-adjacent to A

**A and B remain two separate bottom crums.** `recombine` does not merge them.

**A new INSERT at V=3, I=5, homedoc=H with any width** now calls `insertcbcnd`, which loops over bottom-crum siblings and calls `isanextensionnd` on A:
- `tumblereq(H, A.homedoc)` → TRUE
- `prologuend(A, offset, &grasp, &reach)` → reach = (5, 3)
- `lockeq(reach.dsas, origin.dsas, 2)`: compares (5,3) vs (5,3) → **TRUE**

**Coalescing fires.** A's `cwid` is extended in place (`insertnd.c:251`). No new crum is created.

---

### 5. What Does NOT Happen

- **No homedoc bypass**: if the new insert has `homedoc ≠ H`, the first guard (`insertnd.c:305`) returns FALSE regardless of geometry.
- **No auto-merge of A and B after delete**: they remain separate until an INSERT explicitly arrives at (5,3) with homedoc=H.
- **No memory of the delete in the tree**: the POOM after delete accurately reflects surviving content. The coalescing check has no knowledge of what was deleted; it operates purely on current geometric coordinates.
- **No re-coalescing of B itself**: the `insertcbcnd` loop exits after finding the first match (`return(FALSE)` at `insertnd.c:257`). After coalescing with A, B is not re-evaluated for merging into the now-wider A.

---

### 6. Summary Table

| Condition | Effect on coalescing |
|---|---|
| V-delete removes intervening content between V-adjacent A and B | B's `cdsp.dsas[V]` shifts left; A's `cdsp.dsas[I]` unchanged |
| After delete, A.reach_I == B.grasp_I AND A.reach_V == B.grasp_V | Geometric precondition for coalescing is met |
| `recombine` called by `deletend` (`edit.c:75`) | Structural only — does NOT merge A and B |
| Subsequent INSERT at A's exact 2D reach, same homedoc | `isanextensionnd` → TRUE; A widens in place |
| I-coordinates not I-adjacent after delete | `lockeq` fails on `dsas[I]`; no coalescing even if V-adjacent |

**The coalescing CAN fire across a prior DELETE boundary**, but only when a new INSERT arrives at coordinates that satisfy the simultaneous I-AND-V reach-equals-origin test. The delete itself, via `recombine`, performs no semantic coalescing — it leaves formerly non-adjacent I-spans adjacent-but-separate in the tree, and only a subsequent appropriately-positioned insert will trigger the merge.

---

## Question 12 [gregory]

> When INSERT calls `insertspanf` to create the DOCISPAN entry, does it create exactly one entry covering the full contiguous I-span, or can a single INSERT produce multiple DOCISPAN entries if the POOM insertion splits an existing crum?

### Gregory's Answer

## KB Synthesis

A single INSERT always creates exactly one DOCISPAN entry. POOM crum splitting is irrelevant to DOCISPAN creation.

## Why

The call chain for INSERT is:

```
doinsert → inserttextingranf → docopy → insertpm (POOM)
                                      → insertspanf(..., DOCISPAN)
```

`insertspanf` receives the `ispanset` returned by `inserttextingranf`, not anything derived from POOM structure. These two paths are independent. [ST-INSERT, Finding 0036]

`inserttextingranf` for a single INSERT always produces one contiguous I-span. The allocation uses `tumblerincrement` to extend monotonically from the current maximum, so the freshly allocated range `[prev_max+1, prev_max+len]` is always a single contiguous block. [SS-ADDRESS-SPACE, Finding 0033; INV-MONOTONIC]

`insertspanf` iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. Since `inserttextingranf` returns one `typeispan`, exactly one `insertnd` call occurs — one DOCISPAN entry. [SS-DOCISPAN, Finding 0047]

## POOM splitting is irrelevant

`insertpm` handles the POOM tree (crum splitting, extension, rebalancing). These operations record the V→I mapping but have no effect on the `ispanset` that was already passed to `insertspanf`. The two subsystems receive the same input ispanset independently. Whatever structural tree operations occur — split, coalesce, extend — they do not feed back into the DOCISPAN write path.

This is confirmed by the frame condition [FC-CONTENT-SPANF-ISOLATION]: content operations modify the granfilade and DOCISPAN sub-index based on the I-span from allocation, not from POOM state.

## Summary

| Source of variation | Affects DOCISPAN count? |
|----|---|
| Number of bytes inserted | No (always 1 contiguous I-span from `inserttextingranf`) |
| POOM crum split | No (separate subsystem, independent of `insertspanf` input) |
| POOM crum extension | No (same reason) |
| CREATELINK between inserts | Yes — via a separate allocation that advances the I-address counter, breaking contiguity for *subsequent* inserts [INT-LINK-INSERT, Finding 0063] |

---

## Code Exploration

Now I have everything needed. Let me write the complete answer.

---

## Answer: INSERT, `insertspanf`, and DOCISPAN Entry Count

### The Call Path

**INSERT → `doinsert` → `docopy` → `insertspanf`**

`doinsert` [do1.c:87-123]:
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    ...
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

`docopy` [do1.c:45-64]:
```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // POOM insertion
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // spanfilade entry
&& asserttreeisok(docorgl)
);
```

The critical structural fact: the `ispanset` passed to `insertspanf` is determined entirely by `specset2ispanset` **before** `insertpm` is called. The POOM insertion and spanfilade insertion receive the **same, fixed** sporglset.

---

### How `insertspanf` Creates Entries

`insertspanf` [spanf1.c:15-54] loops over the sporglset and calls `insertnd` **once per item**:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // set lstream, lwidth, linfo from item type
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // [spanf1.c:51]
}
```

The number of DOCISPAN entries created equals the number of items in the sporglset. The loop itself adds no multiplicity — it creates exactly one `insertnd` call per item.

---

### What `insertnd` Does for the Spanfilade

The spanfilade is a `SPAN` enfilade (not POOM). `insertnd` [insertnd.c:62-66] for SPAN:
```c
case SPAN:
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    setwispupwards(fullcrumptr,1);
    break;
```

No `makegappm` is called — that path is POOM-only [insertnd.c:53-54]. `doinsertnd` → `insertmorend` → `insertcbcnd` [insertnd.c:242-275] does one of two things:

- **Extension case** [insertnd.c:250-258]: if `isanextensionnd` is true (new I-span is contiguous with an existing crum's right edge and has the same `homedoc`), the existing crum is widened in place — no new entry.
- **New crum case** [insertnd.c:260-274]: if no extension is possible, one new bottom crum is created via `createcrum` + `adopt`.

`splitcrumupwards` [insertnd.c:272] may restructure internal nodes if a parent is full, but it cannot create additional **bottom** crums — it only splits internal tree nodes. No new DOCISPAN entries result from it.

---

### Why POOM Splitting Cannot Cause Multiple DOCISPAN Entries

`insertpm` [orglinks.c:75-134] inserts into the POOM (the V↔I permutation matrix) using `insertnd` with `V` as the index, calling `makegappm` [insertnd.c:54] to split POOM crums at the insertion V-position:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
knives.nblades = 2;
...
makecutsnd (fullcrumptr, &knives);
```
[insertnd.c:144-148]

This splits POOM crums to open a V-space gap. **But it operates entirely on the granfilade's POOM tree** — a completely separate data structure from the spanfilade. The `ispanset` is a heap-allocated linked list fixed at the point `specset2ispanset` returned; `insertpm` reads it but never writes to it.

By the time `insertspanf` is called (after `insertpm` on do1.c:62), the sporglset already has its final item count. POOM crum splitting has zero influence on that count.

---

### For a Simple Text INSERT: Exactly One DOCISPAN Entry

`inserttextingranf` allocates a single contiguous block of I-space for the inserted text and returns a single I-span in `ispanset`. That becomes a one-item sporglset. `insertspanf` loops once. `insertnd` either widens an adjacent existing DOCISPAN crum or creates one new one.

**Result: A single INSERT always produces exactly one DOCISPAN entry** (or extends one existing entry if the allocated I-space is contiguous with an already-recorded span for that document). The POOM crum splitting that occurs in `insertpm` [insertnd.c:54] is structurally confined to the granfilade and cannot cause `insertspanf` to create additional DOCISPAN entries.

The only way a single INSERT operation could produce multiple DOCISPAN entries would be if `inserttextingranf` returned a multi-item `ispanset` — which would require non-contiguous I-space allocation. The granfilade allocates sequentially and returns one span [do1.c:118], so this does not occur in practice.

---

## Question 13 [gregory]

> The second blade in `findaddressofsecondcutforinsert` computes the boundary tumbler at the next subspace — is this always `2.0` regardless of document structure, or does it dynamically compute the boundary based on the actual next occupied subspace in the POOM?

### Gregory's Answer

## KB Synthesis

The second blade is computed by **pure tumbler arithmetic from the insertion V-address alone** — it does not examine the POOM at all.

[SS-TWO-BLADE-KNIFE] (Finding 0054) documents the algorithm in `findaddressofsecondcutforinsert()` at `insertnd.c:174-183`:

1. Increment the first digit of the insertion address: `N.x → (N+1).x`
2. Behead to isolate the fractional tail: `N.x → 0.x`
3. Subtract the fractional part: `(N+1).x - 0.x = (N+1).0`
4. Add 1 at the second digit: `(N+1).0 → (N+1).1`

The result is always `(N+1).1` where `N` is the leading digit of the insertion point. The source comment embedded in the finding — *"needs this to give it a place to find intersectionof for text is 2.1"* — confirms the design intent: for text subspace (N=1), the hardcoded answer is `2.1`.

[FC-SUBSPACE] and [INV-SUBSPACE-CONVENTION] both state the resulting invariant:

> `∀ N ∈ {1,2,3}, ∀ op = INSERT(N.x) : shift_region(op) ⊆ [N.1, (N+1).1)` holds for all insertions.

Concrete examples from [SS-TWO-BLADE-KNIFE]:
```
INSERT at V-position 1.3:  blade[1] = 2.1  (always, regardless of whether 2.x is occupied)
INSERT at V-position 2.5:  blade[1] = 3.1  (always)
```

The function takes only the insertion V-address as input. There is no call to `findorgl`, no POOM traversal, no inspection of what actually occupies adjacent subspaces. The boundary is geometrically fixed to `(N+1).1` by the first digit of the insertion point.

This is what makes subspace isolation structurally guaranteed for INSERT (as opposed to DELETE, where isolation is accidental via the `strongsub` exponent guard — see [INT-DELETE-SUBSPACE-ASYMMETRY]): the knife boundary is determined before any POOM is consulted, making it independent of document content.

---

## Code Exploration

Now I have all the evidence needed. Let me trace the algorithm fully and confirm with the link VSA setup code.

---

## Answer

The second blade in `findaddressofsecondcutforinsert` is **dynamically computed from the integer (subspace) part of `position`** — it is not hardcoded to `2.0`. Furthermore, it produces `(subspace+1).1`, not `(subspace+1).0`.

---

### The Function

```c
// insertnd.c:174-183
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{    /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;
       tumblerclear (&zero);
       tumblerincrement (position, -1, 1, secondcut);
       beheadtumbler (position, &intpart);
       tumblerincrement(secondcut,0,-tumblerintdiff(&intpart,&zero),secondcut);
       tumblerincrement (secondcut, 1, 1, secondcut);
}
```

---

### Step-by-Step Trace

V-space positions are two-story tumblers `s.n` where `s` is the subspace digit and `n` is the offset within that subspace. Text lives at `1.n`, link from-ends at `2.n`, link to-ends at `3.n` — confirmed by `setlinkvsas` [`do2.c:169-183`] and `findnextlinkvsa` [`do2.c:151-167`].

Given `position = 1.5` (text subspace 1, offset 5): mantissa = `[1, 5, 0, …]`, exp=0.

**Step 1** — `tumblerincrement(position, -1, 1, secondcut)` [`tumble.c:599-623`]:
- `idx` = index of last non-zero digit = 1 (mantissa[1]=5)
- copy position → secondcut; then `secondcut->mantissa[1 + (-1)] += 1`, i.e., `mantissa[0] += 1`
- secondcut = `[2, 5, 0, …]` = **2.5**

**Step 2** — `beheadtumbler(position, &intpart)` [`tumble.c:673-683`]:
- `++exp`, clear mantissa[0] since `exp==0` was; after `tumblerjustify`, left-shift by 1
- intpart = `[5, 0, …]` = **5** (the offset-only tail)

**Step 3** — `tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut)`:
- `tumblerintdiff(intpart, zero)` [`tumble.c:591-597`] returns `intpart.mantissa[0]` = 5
- `tumblerincrement([2,5,…], 0, -5, …)`: idx=1, `mantissa[1+0] += -5` → mantissa[1] = 0
- secondcut = `[2, 0, …]` = **2**

**Step 4** — `tumblerincrement(secondcut, 1, 1, secondcut)`:
- idx=0 (mantissa[0]=2); `mantissa[0+1] += 1` → mantissa[1] = 1
- secondcut = `[2, 1, 0, …]` = **2.1**

The same arithmetic for any `1.n` input cancels the offset `n` and produces **2.1** — matching the comment verbatim: `/*needs this to give it a place to find intersectionof for text is 2.1*/`.

For `position = 2.n` (link subspace), the same algebra yields **3.1**, and so on.

---

### The General Formula

For any two-story position `s.n`, the four steps implement:

1. `secondcut = (s+1).n` — bump the subspace digit up by 1, keeping the offset
2. `intpart = n` — extract just the offset
3. `secondcut = (s+1).0` — subtract the offset, zeroing it
4. `secondcut = (s+1).1` — add `.1` to get the first addressable position in the next subspace

Result: **`(s+1).1`** — always the first position of the next subspace, not its zero boundary.

---

### Why `.1` and Not `.0`?

The `.1` is not accidental. The convention throughout the codebase is that all subspaces start at `.1`, never `.0`. From `findvsatoappend` [`orglinks.c:42-43`]:

```c
tumblerincrement (vsaptr, 0, 1, vsaptr); /* no text in doc */
tumblerincrement (vsaptr, 1, 1, vsaptr);
```

This creates `1.1` as the first insertion address. And `setlinkvsas` [`do2.c:169-179`] creates `1.1`, `2.1`, `3.1` for the three link-endpoint subspaces. The cut needs to fall at a real, addressable position that `newfindintersectionnd` can find in the enfilade tree. A cut at `2.0` — a position that is never occupied — could fail to find a valid intersection node.

---

### No POOM Lookup — Pure Arithmetic

The function receives only `position` (the V-address of the insertion point). It does **not** walk the POOM, call `findpreviousisagr`, or inspect what actually occupies the next subspace. The derivation is entirely arithmetic: strip the offset, increment the subspace, re-attach `.1`. If the next subspace is empty in this particular document, the cut still lands at the right geometric position for the gap operation in `makegappm` [`insertnd.c:124-172`].

---

### Summary

| Question | Answer |
|---|---|
| Is the second blade always `2.0`? | No — it is `(subspace+1).1` |
| Is it hardcoded for text? | For text (`s=1`), it always produces `2.1`, but by arithmetic, not by literal constant |
| Does it check the actual next occupied subspace in the POOM? | No — it is pure tumbler arithmetic on `position`, no data structure lookup |
| What happens for link subspaces? | `position = 2.n` → `3.1`; `position = 3.n` → `4.1` |

The comment `"for text is 2.1"` is a concrete example of the general rule: the second blade is always the first address of the next subspace above the insertion position.

---

## Question 14 [gregory]

> When multiple characters are inserted one at a time at successive V-positions (simulating typing), does each single-character INSERT trigger a full `splitcrumupwards` cycle, or does the ONMYRIGHTBORDER case in `isanextensionnd` handle the entire sequence without any splits or tree height changes?

### Gregory's Answer

## KB Synthesis

## Sequential Single-Character Inserts at Successive Positions

**The short answer:** Only the **first** insert at a new interior position triggers a `splitcrumupwards` cycle. All subsequent inserts at successive V-positions are handled entirely by the ONMYRIGHTBORDER + `isanextensionnd` path — no splits, no tree height changes, zero net crum creation.

---

### Phase 1 — First Insert (e.g., "A" at interior position 1.3)

`whereoncrum(crum, 1.3)` returns `THRUME` (strictly inside the existing crum's interval). `makegappm()` proceeds:

1. Constructs a two-blade knife: `blade[0] = 1.3`, `blade[1] = 2.1` (next subspace boundary via `findaddressofsecondcutforinsert`) [SS-TWO-BLADE-KNIFE]
2. `slicecbcpm` cuts the existing crum at 1.3, producing two crums
3. A new crum is created for "A" at `[1.3, 1.4)` with I-address allocated from granfilade
4. The father's `numberofsons` increments → `toomanysons` may trigger → `splitcrumupwards` may run

**Net: Δcrums = +2** (the original splits into two halves, plus the new content crum). [ST-INSERT Finding 0062]

---

### Phase 2 — Second Insert ("B" at 1.4)

The new crum from Phase 1 covers `[1.3, 1.4)`, so its reach = 1.4.

`makegappm()` runs its early-exit guard first:
```c
if (... || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) return(0);
```

Since `1.4 == reach`, `tumblercmp` returns `EQUAL`, which is `!= LESS` → **`makegappm` returns 0 immediately**. No knife constructed, no crum split. [SS-WHEREONCRUM, PRE-INSERT Finding 0062]

Then `isanextensionnd()` checks two conditions:
1. `homedoc` matches (same document) ✓
2. `new_content.origin == existing_crum.reach` — the fresh I-address for "B" is allocated as `prev_max_iaddr + 1`, which is exactly where the previous crum's I-range ended ✓

Both hold → **the existing crum is extended in place**: `crum.width' = crum.width + 0.1`. No new crum node is allocated, no parent `numberofsons` change, `toomanysons` is never evaluated, `splitcrumupwards` is never called. [ST-INSERT Finding 0062]

**Net: Δcrums = 0**

---

### Phase 3…N — Each Subsequent Character

Identical to Phase 2. The crum's reach advances by one position each time (1.4 → 1.5 → 1.6 → …). Each insert arrives at `origin == reach`, hits the `makegappm` early exit, and is absorbed by `isanextensionnd` extension.

**Net: Δcrums = 0 per character, indefinitely.**

---

### The Bound

This is exactly what [ST-CRUM-BOUND] documents:

```
c ≤ 1 + 2C + 3R + 3P
```

where C = number of distinct cursor repositionings. Sequential typing at successive positions is **one cursor repositioning** (the first interior insert). All N characters after that contribute nothing. So typing 1000 characters in sequence at a single cursor location costs exactly **1 initial split (+2 crums)**, not 1000 splits.

[INV-MONOTONIC] confirms this works because I-addresses are allocated contiguously — each sequential character gets `prev + 1`, which is precisely what `isanextensionnd` requires to coalesce. The only thing that would break the chain is a `CREATELINK` between characters, which advances the I-address allocator past a non-text orgl and destroys contiguity [ST-CRUM-BOUND Finding 0063, INT-LINK-INSERT].

---

## Code Exploration

I now have complete information. Here is the full analysis:

---

## Answer: Consecutive Single-Character Insertions — No Splits, `isanextensionnd` Handles the Whole Sequence

The short answer: **`isanextensionnd` handles the entire consecutive-typing sequence without any splits, new crums, or tree height changes.** `splitcrumupwards` is never reached. Here is the full trace.

---

### 1. Entry Point: `doinsert` → `insertnd` (POOM Path)

Each keystroke calls `doinsert` [`do1.c:87`], which:

1. Calls `inserttextingranf` to allocate an I-address `lsa` in the granfilade and returns an `ispanset` with `stream=lsa, width=1`.
2. Calls `docopy` → `insertpm` → `insertnd` to stitch that I-span into the POOM at the requested V-address.

In `insertnd`, the POOM case is [`insertnd.c:53-61`]:
```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    setwispupwards(fullcrumptr,1);
    break;
```

---

### 2. `makegappm` Exits Immediately for Right-Edge Appends

`makegappm` [`insertnd.c:124`] opens a gap in the V-space for mid-document insertions. Its early-exit guard is [`insertnd.c:140-143`]:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

When typing appends at the end: `origin.V == reach.V` (the new character starts exactly where existing content ends). The condition `origin.V < reach.V` is `FALSE`, so `!FALSE = TRUE` → `return(0)`. **No cuts, no gap creation.**

---

### 3. First Character: `firstinsertionnd`

When the enfilade is empty, `doinsertnd` [`insertnd.c:191-194`] takes the `isemptyenfilade` branch:
```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
```

`firstinsertionnd` [`insertnd.c:199`] populates the existing (or freshly-created) bottom crum:
- `cdsp = (V=V₁, I=lsa₁)`
- `cwid = (V=1, I=1)`

Returns `FALSE` — no split.

---

### 4. Characters 2, 3, … N: `isanextensionnd` Fires Every Time

For subsequent characters, control reaches `insertmorend` → `insertcbcnd` [`insertnd.c:242`]:
```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr)
{
    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
        if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
            dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
            ivemodified (ptr);
            setwispupwards (father,1);
            if(!isfullcrum((typecorecrum*)father)){
                return(setwispupwards(findfather((typecorecrum*)father),1));
            }
            return(FALSE);           // ← no split, returns here
        }
    }
    // ... new crum creation + splitcrumupwards only reached if no extension found
```

The split path at [`insertnd.c:272`]:
```c
splitsomething = splitcrumupwards (father);
```
is **only reached when `isanextensionnd` returns FALSE for every son**. For consecutive typing, it never returns FALSE.

---

### 5. Why `isanextensionnd` Returns TRUE for Every Appended Character

The function [`insertnd.c:301-309`]:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must hold:

**Condition A — same `homedoc`:** All typed characters share the same document ISA, so this is always TRUE.

**Condition B — `reach == origin` in ALL dimensions:** `prologuend` computes [`retrie.c:334-339`]:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```
So: `grasp = offset + cdsp`, `reach = grasp + cwid`.

For POOM, `DSPSIZEPM = 2` [`wisp.h:26`], meaning `lockeq` compares **both** V and I dimensions:

- **V dimension:** After character `n` is stored (width 1 each), `cwid.V = n`, so `reach.V = V₁ + n`. Character `n+1` has `origin.V = V₁ + n`. ✓ Equal.

- **I dimension:** The granfilade allocates I-addresses consecutively. In `inserttextgr` [`granf2.c:83`], `findisatoinsertgr` → `findisatoinsertmolecule` [`granf2.c:158`] calls `findpreviousisagr` to find the last allocated address `A + (n-1)`, then for TEXTATOM computes [`granf2.c:169`]:
  ```c
  tumblerincrement (&lowerbound, 0, 1, isaptr);  // isaptr = lowerbound + 1
  ```
  So each successive character gets I-address `A, A+1, A+2, …`. After `n` chars, `cwid.I = n`, `reach.I = A + n`, and char `n+1` has `origin.I = A + n`. ✓ Equal.

Both dimensions match → `lockeq` returns TRUE → **`isanextensionnd` fires on every appended character.**

---

### 6. What Happens in the Extension Branch

When `isanextensionnd` returns TRUE [`insertnd.c:251-258`]:
```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
ivemodified (ptr);
setwispupwards (father,1);
...
return(FALSE);
```

- The single bottom crum is **widened** in both V and I: `cwid.V++`, `cwid.I++`
- `ivemodified` marks it dirty for flushing
- `setwispupwards` propagates the new width upward
- Returns `FALSE` (`bothertorecombine = FALSE`)

No new crums are created. No `splitcrumupwards`. No `adopt`. No height change.

---

### 7. `recombine` Is Also Skipped

Back in `insertnd` [`insertnd.c:70`]:
```c
if(/*TRUE||*/bothertorecombine||(fullcrumptr->height != oldheight)){
    recombine (fullcrumptr);
}
```

The commented-out `TRUE||` reveals that recombination was once unconditional. Now it only runs if a split happened (`bothertorecombine=TRUE`) or height changed. For extension insertions: `bothertorecombine = FALSE` and height is unchanged → **`recombine` is skipped entirely.**

---

### 8. `splitcrumupwards` Internals (Never Reached for Typing)

For completeness: `splitcrumupwards` [`split.c:16`] iterates upward while `toomanysons(father)`, splitting overfull crums and potentially calling `levelpush` to grow tree height. Since the extension path never adds a new son and never calls `splitcrumupwards`, this machinery is entirely inert during consecutive typing.

---

### Summary

| Insertion | `makegappm` | New crum | `splitcrumupwards` | Tree height | Effect |
|-----------|-------------|----------|---------------------|-------------|--------|
| Char 1 (empty doc) | Early exit | — | No | Unchanged | `firstinsertionnd` populates single bottom crum |
| Chars 2…N (append) | Early exit (origin ≥ reach) | No | No | Unchanged | `isanextensionnd` widens the single bottom crum |

For the entire typing sequence, the POOM enfilade maintains exactly **one bottom crum** that grows in width (both V and I) by 1 per keystroke. The B-tree structure is never reorganized. The `ONMYRIGHTBORDER` semantics — the origin falls exactly on the right edge of the existing crum (`reach == origin` in both dimensions) — is precisely the condition `lockeq` tests in `isanextensionnd` [`insertnd.c:308`], and it fires unconditionally for all consecutive appends sharing the same `homedoc`.

---

## Question 15 [gregory]

> INSERT at V-position `v` in an empty document creates the first POOM entry — does this initial insertion also trigger `makegappm` (finding nothing to shift), or is there a fast path that skips the gap-making machinery when the POOM has no existing entries?

### Gregory's Answer

## KB Synthesis

The KB gives a clear answer from two converging sources.

**Fast path exists: `makegappm`'s zero-width early exit**

From [ST-INSERT] / [SS-WHEREONCRUM] (Finding 0062), `makegappm` contains an explicit triple-condition early exit at `insertnd.c:137-143`:

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V]) ||
    tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS ||
    tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```

The **first condition** — `iszerotumbler(cwid.dsas[V])` — fires immediately for an empty document. From [SS-ENFILADE-TREE] (Finding 0058), `createenf(POOM)` produces a height-1 fullcrum with a single height-0 bottom node having **zero width**. So for any first insertion, `makegappm` returns 0 without constructing a knife, without calling `makecutsnd`, and without running `insertcutsectionnd`. No shifting machinery executes.

**What happens instead**

The actual first-entry path is `firstinsertionnd`, documented in [ST-INSERT] (Finding 0066): it sets the new child's `cdsp` to the absolute insertion V-position, then calls `setwispnd` on the parent to absorb that displacement into the root. From that finding:

> For first child, `firstinsertionnd` sets child `cdsp = insertion_position` (absolute), then `setwispnd` absorbs it: `root.cdsp = insertion_position`, `child.cdsp = 0` (relative).

**Summary**

| Condition | Mechanism | Result |
|-----------|-----------|--------|
| Empty POOM (cwid = 0) | `makegappm` zero-width guard | Returns 0 immediately — no knife, no shifts |
| First entry insertion | `firstinsertionnd` | Absolute position set, `setwispnd` updates root displacement |

The zero-width check in `makegappm` is the fast path. It is structurally necessary — for an empty crum with grasp=0, reach=0, any positive insertion address falls at `TOMYRIGHT` anyway (per [SS-WHEREONCRUM]), so the third condition would also fire. But the zero-width test catches it first, before tumbler comparisons are even attempted.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Answer: `makegappm` Is Called but Returns Immediately for an Empty POOM

There is **no fast path that bypasses the `makegappm` call** for the empty-document case. However, `makegappm` itself contains a guard condition that causes it to exit immediately when the POOM has zero width — which is exactly the state of a fresh document.

### Call chain

```
doinsert (do1.c:87)
  → inserttextingranf + docopy
    → insertpm (orglinks.c:75)
      → insertnd (orglinks.c:130)
        → makegappm (insertnd.c:54)  ← always called for POOM
        → doinsertnd (insertnd.c:57)
          → firstinsertionnd (insertnd.c:192)  ← empty-enfilade fast path
```

### Step 1 — `insertnd` unconditionally calls `makegappm` for POOM

`insertnd.c:51-61`:
```c
switch (fullcrumptr->cenftype) {
  case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   /* line 54 — no guard */
    checkspecandstringbefore();
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    ...
```

There is no `if (!isempty...)` wrapper around this call. `makegappm` is always entered for POOM.

### Step 2 — `makegappm` returns immediately for an empty POOM

`makegappm` (`insertnd.c:124`) begins with a three-condition early exit at lines 140–143:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

For a document that has never had content, `fullcrumptr->cwid.dsas[V]` is the zero tumbler. `iszerotumbler` fires on the very first clause, and the function returns `0` without executing any of the cut machinery (`makecutsnd`, `newfindintersectionnd`, the `for` loop over children, `setwidnd`, `setwispupwards`). The comment — *"this [is] for extensions to bc without calling cut"* — is the authors' label for this class of no-op early return.

### Step 3 — `doinsertnd` routes to `firstinsertionnd`, not `insertmorend`

Back in the `case POOM` block, `doinsertnd` is called (`insertnd.c:57`). Its first act (`insertnd.c:191–193`):

```c
if (isemptyenfilade (father)) {
    firstinsertionnd (father, origin, width, infoptr);
    return(FALSE);
}
```

`isemptyenfilade` for POOM (`genf.c:105–108`) checks that both `cwid` and `cdsp` tumblers are all-zero:

```c
case POOM :
    return (
       iszerolock(ptr->cwid.dsas, (unsigned)widsize(ptr->cenftype))
    && iszerolock(ptr->cdsp.dsas, (unsigned)dspsize(ptr->cenftype)));
```

An empty document satisfies both conditions, so `firstinsertionnd` is called (`insertnd.c:199`). It reuses or creates the single bottom crum, writes the origin/width/info directly into it, and returns. The full `insertmorend` → `insertcbcnd` → `splitcrumupwards` path is never entered.

### Summary

| Phase | Empty document | Non-empty document |
|---|---|---|
| `insertnd` calls `makegappm`? | **Yes, always** | Yes |
| `makegappm` does real work? | **No — exits at line 143** (`iszerotumbler` fires) | Yes — cuts, shifts, updates |
| `doinsertnd` path taken | `firstinsertionnd` | `insertmorend` |

The "fast path" is not a bypass of the `makegappm` call — it is the `iszerotumbler` guard inside `makegappm` (`insertnd.c:140`) combined with `isemptyenfilade` inside `doinsertnd` (`insertnd.c:191`). Both checks are O(1) tumbler comparisons. The gap-making machinery (cuts, sibling iteration, displacement adjustments) is entirely skipped for the first insertion.

---

## Question 16 [gregory]

> When INSERT adds text immediately adjacent to existing content (e.g., appending at the end of current text), does the granfilade always allocate the next contiguous I-address such that the POOM can coalesce into a single bottom crum, or are there conditions where the I-address is non-contiguous despite the V-position being adjacent?

### Gregory's Answer

## KB Synthesis

## I-Address Contiguity for Adjacent Inserts

The short answer: adjacent V-position inserts produce contiguous I-addresses **only when no content-allocating operation intervenes**. Several KB entries are relevant.

### The Allocation Mechanism

From [SS-ADDRESS-ALLOC] / [INV-MONOTONIC]: I-address allocation is stateless — `findisatoinsertmolecule` queries the granfilade for the current maximum I-address and increments by 1. There is no per-session counter or locality hint. The allocation is purely `next_iaddr(granf) = max_iaddr(granf) + 1`, regardless of where the insertion falls in V-space.

### What Enables Coalescing

From [ST-INSERT] (Finding 0062): `isanextensionnd()` coalesces a new insertion into an existing POOM crum when **both** hold:
1. Same `homedoc` (I-address origin document)
2. New content's I-address origin == existing crum's reach (I-space contiguity)

V-adjacency is necessary but insufficient — I-address contiguity is the operative condition.

### What Breaks I-Address Contiguity

From [INT-LINK-INSERT] (Finding 0063): **CREATELINK** is the primary disruptor. It calls `createorglingranf`, which allocates a link orgl in the granfilade. This advances `max_iaddr(granf)`. When the next INSERT calls `findpreviousisagr`, it finds the link orgl's I-address as the maximum and allocates text I-addresses above it — non-contiguous with any preceding text I-addresses. This is directly observable: `INSERT "ABC" → CREATELINK → INSERT "DEF"` yields **two** shared span pairs in `compare_versions`.

Any other **INSERT** (at any V-position in any document) also advances the global maximum, breaking contiguity for subsequently adjacent inserts.

### What Does NOT Break Contiguity

From [INV-MONOTONIC] (Finding 0077) and [FC-GRANF-ON-DELETE] (Finding 0061):

- **DELETE** and **REARRANGE**: granfilade unchanged; `findpreviousisagr` returns the same maximum. I-address contiguity is preserved.
- **CREATENEWVERSION**: allocates only a document address in a separate tumbler range, not a content I-address. `INSERT "ABC" → VERSION → INSERT "DEF"` yields **one** shared span pair — contiguous.

The contiguity-breaking predicate from [INV-MONOTONIC] (Finding 0077): `text_contiguous(insert_a, insert_b) ⟺ ¬∃ alloc_c : time(a) < time(c) < time(b) ∧ alloc_c ∈ content_allocations`, where `content_allocations = {INSERT, CREATELINK}`.

### Summary Table

| Intervening Operation | Granfilade Modified? | I-Addresses Contiguous? | POOM Coalesces? |
|---|---|---|---|
| None | No | Yes | Yes |
| DELETE / REARRANGE | No | Yes | Yes |
| CREATENEWVERSION | Doc address only | Yes | Yes |
| CREATELINK | Yes (link orgl) | **No** | No |
| Another INSERT | Yes (text) | **No** | No |

### The Homedoc Caveat

Even with contiguous I-addresses, if adjacent V-positions hold content from **different source documents** (e.g., text inserted natively vs. transcluded via COPY), `isanextensionnd` fails the `homedoc` check [ST-INSERT, Finding 0046]. The I-addresses may be contiguous in the permascroll, but the POOM crums will not coalesce because the content origin differs.

---

## Code Exploration

Now I have the complete picture. Let me compose the full answer.

---

## Answer: I-Address Contiguity and POOM Coalescence on Adjacent INSERT

### The Full Call Chain for INSERT

`fns.c:insert` [fns.c:84] → `doinsert` [do1.c:87] → (1) `inserttextingranf` to allocate I-address, (2) `docopy` → `insertpm` → `insertnd` → `insertcbcnd` to register V↔I mapping in the POOM.

---

### Step 1: I-Address Allocation in the Granfilade

`inserttextgr` [granf2.c:83-109] calls `findisatoinsertgr` [granf2.c:130] to determine the starting I-address for new text. For text atoms (`ATOM` subtype with `TEXTATOM=1`), this routes to `findisatoinsertmolecule` [granf2.c:158-181].

That function first establishes a search boundary:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // granf2.c:162
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // granf2.c:164
```

`upperbound` = `docISA.0.(TEXTATOM+1)` = `docISA.0.2` — this strictly excludes link atoms (`LINKATOM=2` lives at addresses ≥ `docISA.0.2.0.1`, which are all greater than `docISA.0.2`). The search is bounded to this document's text atom range only.

`findpreviousisagr` [granf2.c:256-278] walks the granfilade tree right-to-left, accumulating relative offsets. At the leaf node (height=0), it calls `findlastisaincbcgr` [granf2.c:280-284]:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)   /* offset is last isa if non-text or one char */
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
}
```

This sets `lowerbound` to the address of the **last character** of the last text crum.

Now in `findisatoinsertmolecule`, there are two cases:

**Case A** — `tumblerlength(hintisa) == tumblerlength(lowerbound)`: no text atoms exist yet (the search found the document's own GRANORGL, at the same address depth as `hintisa`):
```c
tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // granf2.c:166
tumblerincrement (isaptr, 1, 1, isaptr);                       // granf2.c:167
```
Allocates the first text atom at `docISA.0.1.0.1` (two levels below document ISA). This is a cold start — no predecessor to coalesce with anyway.

**Case B** — text atoms already exist, `atomtype == TEXTATOM`:
```c
tumblerincrement (&lowerbound, 0, 1, isaptr);  // granf2.c:169
```
`lowerbound` is the last character's address. Adding 1 at level 0 (same digit depth) gives `new_start = last_char_addr + 1`.

**This IS the address immediately after the last allocated character. I-addresses are strictly contiguous here.**

If the previous crum had I-start = S and length = L, it occupied [S, S+L-1]. `findlastisaincbcgr` returns S+L-1. Case B gives new start = S+L = the previous crum's I-reach. That is the definition of contiguity.

---

### Step 2: POOM Coalescence Test

After `inserttextingranf` returns `ispanset = {stream: lsa, width: total_chars}`, `docopy` → `insertpm` [orglinks.c:75-134] passes the V and I spans to `insertnd` [insertnd.c:15] → `insertcbcnd` [insertnd.c:242].

Before creating a new bottom crum, `insertcbcnd` [insertnd.c:249-258] scans existing bottom crums:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // extend in-place
        ...
        return(FALSE);  // coalesced — no new crum
    }
}
```

The coalescence predicate `isanextensionnd` [insertnd.c:301-309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must hold:
1. Same home document (`homedoc` match)
2. **Both V-reach and I-reach of the existing crum equal the V-origin and I-origin of the new insertion** — `lockeq` is a full 2D comparison of the `dsas[V]` and `dsas[I]` fields simultaneously

For appending at the V-end of a document, `appendpm` calls `findvsatoappend` [orglinks.c:29-49] to get exactly `reach.dsas[V]` of the last text crum:

```c
} else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr); /* no links in doc */
```

So V-adjacency holds. And since Case B gives `I_new_start = I_reach_of_last_crum`, I-adjacency also holds. **Coalescence occurs for a pure append.**

For `makegappm` [insertnd.c:124]: when appending, `origin.dsas[V] >= reach.dsas[V]` of the full POOM, so the early-return guard fires:
```c
if (...|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut */  // insertnd.c:143
```
No splitting needed for a pure append. ✓

---

### The Granfilade Also Has Its Own Compaction

Independently of POOM coalescence, `insertseq` [insert.c:17-70] does compaction at the granfilade level:

```c
if (           /* crum can be extended */
   info->infotype == GRANTEXT
&& ptr->cinfo.infotype == GRANTEXT
&& ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {   // insert.c:38
        ivemodified ((typecorecrum*)ptr);
        return(0);  // text absorbed into existing granfilade crum
    }
}
```

`fillupcbcseq` [insert.c:75] appends new characters directly into the existing granfilade leaf if there is capacity. This is separate from POOM coalescence — it compacts the permascroll storage itself.

---

### The Conditions Where I-Address Is Non-Contiguous Despite V-Adjacency

**Case: document versioning or content copy**

`docreatenewversion` [do1.c:260] creates a new document under a different ISA, then calls `docopyinternal` → `insertpm` to populate the new document's POOM with crums whose I-addresses point into the **original** document's ISA subtree (e.g., `origDocISA.0.1.0.*`).

When a subsequent INSERT appends to the new version:

- `doinsert` calls `inserttextingranf` with `hint.hintisa = newDocISA`
- `findisatoinsertmolecule` searches `findpreviousisagr` up to `newDocISA.0.2`
- No text atoms exist under `newDocISA.0.1.*` (only the GRANORGL at `newDocISA` itself)
- `tumblerlength(hintisa) == tumblerlength(lowerbound)` → **Case A fires**
- Fresh I-address allocated: `newDocISA.0.1.0.1.0.1`

The POOM's last crum has I-reach = some address in `origDocISA.0.1.*`. The new I-origin = `newDocISA.0.1.0.1.0.1`. These are in **entirely different branches of the address hierarchy**.

`isanextensionnd` tests `lockeq(reach.dsas, originptr->dsas, ...)`:
- `reach.dsas[I]` ≠ `originptr->dsas[I]`
- **Coalescence fails.**

The POOM acquires a new bottom crum even though the V-position is adjacent. The new text's I-address is non-contiguous with the copied content's I-addresses — they live in separate document ISA subtrees.

**The same pattern applies to `docopy`** [do1.c:45] when inserting content transcluded from another document. The POOM crum's I-span points to the source document's permascroll range; new original text in the target document gets fresh I-addresses from the target's ISA subtree.

---

### Summary

| Condition | I-contiguous? | V-adjacent? | POOM coalesces? |
|-----------|--------------|-------------|-----------------|
| Append to original document | Yes — `findisatoinsertmolecule` Case B: `lowerbound + 1` | Yes — `findvsatoappend` returns exact V-reach | Yes — both arms of `isanextensionnd` succeed |
| Mid-document insert (original) | Yes — still Case B, allocates next sequential I-addr | No — V-origin ≠ V-reach of any crum | No — V-arm of `isanextensionnd` fails |
| First insert into fresh document | N/A — Case A, cold start | N/A | N/A — nothing to coalesce with |
| Append to versioned/copied document | No — Case A, new ISA subtree | Yes | No — I-arm of `isanextensionnd` fails |

**The definitive non-contiguous case**: After `docreatenewversion` or `docopy`, the target document's POOM holds I-spans from a foreign ISA subtree. Any original text insertion allocates from the target document's own ISA subtree via Case A of `findisatoinsertmolecule`. Even though V-positions are adjacent at the append point, the I-addresses are non-contiguous across ISA subtree boundaries — `isanextensionnd` [insertnd.c:308] fails the `lockeq` test, and the POOM acquires a new bottom crum rather than extending the existing one.

---

## Question 17 [gregory]

> After INSERT creates a new granfilade leaf with `MAXBCINLOAF=1`, what determines whether this triggers a `splitcrumupwards` and `levelpush` in the granfilade tree — is it purely the occupancy exceeding 1 in the parent loaf, and how does this interact with the disabled `levelpull`?

### Gregory's Answer

## KB Synthesis

## Granfilade Split Mechanics After INSERT

### What triggers `splitcrumupwards`

After INSERT allocates a new granfilade leaf via `insertseq`, it adopts the new height-0 bottom crum as the **right sibling** of the existing bottom crum under the parent height-1 node [SS-DUAL-ENFILADE, Finding 0041]. Immediately after `adopt`, the code calls `splitcrumupwards(father)`.

The trigger condition is purely occupancy: `toomanysons(father)` returns TRUE when `father->numberofsons > MAXBCINLOAF` — that is, `> 1` [SS-GRAN-BOTTOM-SINGLETON, SS-ENFILADE-BRANCHING]. So any height-1 node holding 2 bottom crums immediately satisfies `toomanysons`. Since `MAXBCINLOAF = 1`, this triggers on **every second insert** that lands under the same height-1 node.

### What determines `levelpush` vs. `splitcrum`

`splitcrumupwards` checks `isfullcrum(ptr)` — whether the node is the apex [SS-SPLIT, Finding 0070]:

- **If the height-1 node IS the fullcrum (root):** `levelpush` is called first, incrementing the fullcrum's height from 1→2 and pushing its existing children down one level. Then `splitcrum` splits the now-demoted former root into two height-1 children under the new height-2 fullcrum.
- **If the height-1 node is NOT the fullcrum:** `splitcrum` directly creates a new sibling height-1 node, distributing children between original and sibling. The parent gains one child. This may cascade upward — `splitcrumupwards` loops while `toomanysons` is true.

[SS-ENFILADE-TREE, Finding 0060] documents the exact consequence: inserting the 3rd bottom crum when the tree is at height-2 with two height-1 nodes (each with 1 child) triggers a split at a non-root height-1 node, adding a third child to the fullcrum. Since `MAXUCINLOAF = 6` applies to upper crums, the fullcrum won't itself split until it accumulates 7 children — so height growth is relatively rare.

### The `levelpull` asymmetry

`levelpull` is disabled — it immediately `return(0)` without executing the collapse logic [SS-ENFILADE-TREE, Finding 0058]. This has two concrete consequences:

1. **Tree height is monotonically non-decreasing** [INV-ENFILADE-MINIMALITY]. Every `levelpush` is permanent. A granfilade that grew to height-3 during content insertion will remain height-3 even after delete-everything.

2. **The two "empty document" states are non-equivalent** [EC-EMPTY-DOC, Finding 0058]: a never-filled document (height-1, one zero-width bottom node) differs structurally from a post-delete-all document (height-H, empty intermediate nodes, zero bottom nodes). The latter causes Bug 0019 — INSERT crashes because `firstinsertionnd` expects a bottom crum to exist.

### Summary

The trigger is purely occupancy: `numberofsons > 1` at any height-1 granfilade node, which fires on every second insert into that node. Whether this causes `levelpush` (height growth) depends solely on whether that height-1 node is the current fullcrum. Because `levelpull` is disabled, height growth from `levelpush` is permanent — the granfilade can only grow taller, never shorter, making its height a monotonically non-decreasing value over the document's lifetime [INV-ENFILADE-MINIMALITY].

---

## Code Exploration

I now have all the code needed for a complete, cited answer.

---

## What Determines `splitcrumupwards` and `levelpush` in the GRAN Granfilade Tree

### The Call Chain

Every granfilade insert routes through `insertseq()` in `insert.c`. The two entry points are:
- `inserttextgr` [granf2.c:82] calls `insertseq()` [granf2.c:99]
- `createorglgr` [granf2.c:110] calls `insertseq()` [granf2.c:125]

Inside `insertseq` [insert.c:17], there is a **fast path** that avoids creating a new leaf entirely:

```c
if (info->infotype == GRANTEXT
 && ptr->cinfo.infotype == GRANTEXT
 && ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq(ptr, &nextaddress, info)) {   // pack text into existing leaf
        ivemodified((typecorecrum*)ptr);
        return(0);   // ← NO splitcrumupwards on this path
    }
}
```
[insert.c:34–41]

When the existing bottom crum has room (`textlength < GRANTEXTLENGTH`) and the text fits, `fillupcbcseq` packs it in and returns without calling `splitcrumupwards` at all.

---

### When a New Leaf Is Created

If the fast path fails (non-text content like `GRANORGL`, full crum, or text that didn't fit), `insertseq` creates and adopts a new leaf:

```c
new = createcrum(0, (INT)ptr->cenftype);
reserve(new);
adopt(new, RIGHTBRO, (typecorecrum*)ptr);   // ← new sibling added to father
ivemodified(new);
splitsomething = splitcrumupwards(findfather(new));   // ← FIRST CALL [line 48]
...
splitsomething |= splitcrumupwards(findfather(ptr)); // ← SECOND CALL [line 64]
```
[insert.c:43–64]

`splitcrumupwards` is called **twice** — once on the parent of the new leaf, once on the parent of the split point — before `recombine()` is conditionally called [insert.c:67–69].

---

### What `toomanysons` Actually Tests

`splitcrumupwards` [split.c:16] loops on the `toomanysons` predicate [genf.c:239]:

```c
bool toomanysons(typecuc *ptr)
{
    ...
    return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum(...)?MAX2DBCINLOAF:MAXBCINLOAF)));
}
```

The constants [enf.h:26–28]:
```c
#define MAXUCINLOAF     6
#define MAXBCINLOAF     1     /* so text will fit */
#define MAX2DBCINLOAF   4
```

For a GRAN tree (`is2dcrum` returns FALSE for `GRAN` [genf.c:19]):

| Height of node | Threshold | Overflows when |
|---|---|---|
| `height == 1` (direct parent of leaves) | `MAXBCINLOAF = 1` | `numberofsons > 1`, i.e., ≥ 2 leaves |
| `height > 1` (internal nodes, apex) | `MAXUCINLOAF = 6` | `numberofsons > 6`, i.e., ≥ 7 children |

**Yes: occupancy exceeding 1 is the precise test at height 1.** After `adopt(new, RIGHTBRO, ptr)` adds the new leaf, the height-1 parent goes from 1 to 2 sons — immediately triggering `toomanysons`. So every successful new-leaf insertion (that isn't the fill-in-existing-leaf fast path) triggers a height-1 split.

---

### What `splitcrumupwards` Does on Each Overfull Node

```c
bool splitcrumupwards(typecuc *father)
{
    for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
        if (isfullcrum((typecorecrum*)father)) {
            levelpush(father);
            splitcrum((typecuc*)findleftson(father));
            return(TRUE);
        }
        splitcrum(father);   // ← non-apex path
        splitsomething = TRUE;
    }
    return(splitsomething);
}
```
[split.c:26–43]

For GRAN, `splitcrum` dispatches to `splitcrumseq` [split.c:47–48], which creates a right sibling for `father` and migrates `numberofsons/2` children to it [split.c:81–88]. With `MAXBCINLOAF=1`, a 2-child height-1 node splits into two 1-child height-1 nodes, incrementing the parent's `numberofsons` by 1.

The loop **walks up** the tree. At each level it:
1. Calls `splitcrum(father)` if not apex → parent gains one more child
2. Checks parent → if `numberofsons > MAXUCINLOAF=6`, splits parent too
3. Continues until either `toomanysons` is false or it reaches the apex

---

### When `levelpush` Fires

`levelpush` fires **only** when the loop reaches the fullcrum (`isfullcrum` is TRUE) and `toomanysons` is still TRUE there. At the apex, the threshold is still `MAXUCINLOAF=6` (since apex height is always > 1 after the first push). `levelpush` [genf.c:263]:

```c
new = createcrum(fullcrumptr->height, fullcrumptr->cenftype);
new->isleftmost = TRUE;
transferloaf(fullcrumptr, new);       // move all children to new intermediate node
fullcrumptr->height++;                // apex grows by one level
adopt((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);  // new becomes sole child
new->sonorigin = temploafptr;
setwispupwards(new, 1);
```
[genf.c:273–292]

Then `splitcrum(findleftson(father))` immediately splits the now-overfull intermediate node [split.c:29].

**So `levelpush` is NOT triggered by `MAXBCINLOAF=1` directly.** `MAXBCINLOAF=1` determines that height-1 nodes split after every single new-leaf insertion, causing height-2 (and higher) nodes to accumulate children rapidly. `levelpush` fires when the fullcrum's `numberofsons` exceeds `MAXUCINLOAF=6` — which is determined by how many times height-level splits have propagated to the apex.

In a fresh GRAN tree at height 2 (apex directly above height-1 nodes), the progression is:
- Insertions 1–7 each cause a height-1 split → apex gains a height-1 child each time
- When the apex reaches 7 children: `toomanysons` fires at apex → `levelpush` → apex height becomes 3

After `levelpush`, the apex has one intermediate child (height 2) with ≤6 grandchildren, so further insertions must propagate all the way up again before another `levelpush` fires.

---

### The Disabled `levelpull` and Its Effect

`levelpull` [genf.c:318] is completely gutted:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson(fullcrumptr);
    dspadd(&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, fullcrumptr->cenftype);
    disown(ptr);
    fullcrumptr->height--;
    transferloaf(ptr, fullcrumptr);
    setwispupwards(fullcrumptr, 1);
    freecrum(ptr);
*/
}
```
[genf.c:318–342]

The only live code is `return(0)`. The commented-out body would have collapsed the apex one level when it had exactly 1 child — the inverse of `levelpush`.

`recombineseq` calls `levelpull(father)` when `father->isapex` [recombine.c:66–67]:
```c
if (father->isapex)
    levelpull(father);
```

Since `levelpull` is a no-op, `recombineseq` never shrinks the tree height. The consequences:

1. **The apex height only ever increases** via `levelpush`; it never decreases regardless of deletions
2. After deletes that leave the tree sparse, the apex height remains at whatever maximum it reached during insertion — future inserts re-use that height rather than needing another `levelpush`
3. **`recombineseq` itself has an early return** [recombine.c:41]: `if (father->height < 3 || !father->modified) return(0)` — recombine is only attempted for trees of height ≥ 3, so shallow trees after deletes get no consolidation at all from that path
4. The structural invariant is asymmetric: the tree is a ratchet that grows in height during bulk inserts but never compresses, so a session that inserts many documents and then deletes most of them will retain an oversized tree skeleton

---

### Summary

| Question | Answer | Source |
|---|---|---|
| What triggers `splitcrumupwards`? | Creating a new leaf: `adopt(new, RIGHTBRO, ptr)` → parent goes from 1 to 2 bottom crums → `toomanysons` at height-1 returns TRUE (`numberofsons > MAXBCINLOAF=1`) | insert.c:46–48, genf.c:239, enf.h:27 |
| Is it purely occupancy > 1? | Yes, for height-1 nodes. Every new leaf insert immediately fires the condition. Text-pack fast path (`fillupcbcseq`) is the only escape | insert.c:34–41, genf.c:239–244 |
| What triggers `levelpush`? | `splitcrumupwards` loop reaching the fullcrum when `toomanysons` is still TRUE there; threshold is `MAXUCINLOAF=6` at the apex regardless of `MAXBCINLOAF` | split.c:26–31, genf.c:263, enf.h:26 |
| How does disabled `levelpull` interact? | `recombineseq` calls `levelpull` when `isapex`, but `levelpull` is a no-op (`return(0)`, body commented out). Tree height never decreases. This creates a ratchet: `levelpush` grows the apex, nothing shrinks it | genf.c:318–342, recombine.c:66–67 |

---

## Question 18 [gregory]

> When a COPY operation inserts transcluded content into a document (reusing existing I-addresses rather than allocating new ones), does the target POOM's `insertpm` follow the exact same code path as text INSERT — including `makegappm` shifting and `isanextensionnd` coalescing — or is there a separate insertion path for copied content?

### Gregory's Answer

## KB Synthesis

Yes, COPY follows the exact same POOM insertion code path as text INSERT. The KB is explicit on both points.

## Same code path: `insertpm` → `insertnd` → `makegappm`

[ST-INSERT] Finding 0052 states directly:

> INSERT, COPY, and CREATELINK all share the same POOM insertion mechanism: `insertpm` → `insertnd` → `makegappm`.

The `docopy()` call chain is confirmed in [ST-INSERT] Finding 0036 (`do1.c:45-65`): `docopy` → `insertpm` → `insertnd` → `makegappm`. The shifting behavior — classifying crums via `insertcutsectionnd` and applying `tumbleradd` to entries in the shift region `[blade[0], blade[1])` — is identical for COPY and INSERT.

## `isanextensionnd` coalescing applies, but with a `homedoc` constraint

[ST-VCOPY] Finding 0046 confirms that `isanextensionnd` runs during COPY:

> The function `isanextensionnd()` checks two conditions: (1) the new mapping has the same `homedoc` as an existing crum, and (2) the new mapping starts exactly where the existing crum ends (contiguous in both V and I dimensions). If both hold, the existing crum's width is extended in place.

The critical difference from text INSERT: `homedoc` must match. Since COPY reuses I-addresses that originated in another document, the `homedoc` field encodes the I-address origin document. Consecutive COPYs from **different** source documents will never coalesce even if they land at contiguous V-positions, because `isanextensionnd` fails on the homedoc check. COPYs from the **same** source document will coalesce if V- and I-contiguity both hold.

## Summary

| Property | Text INSERT | COPY |
|----------|-------------|------|
| `insertpm` → `insertnd` → `makegappm` | ✓ | ✓ |
| `makegappm` shifting of subsequent crums | ✓ | ✓ |
| `isanextensionnd` coalescing | ✓ (same homedoc = same doc) | ✓ (only if homedoc matches) |
| Allocates new I-addresses | ✓ | ✗ (reuses existing) |

The POOM layer is completely agnostic to whether I-addresses are fresh or reused — it operates on `(V-position, I-address)` pairs and applies the same structural logic either way. The distinction between INSERT and COPY is entirely at the layer above: INSERT calls `inserttextingranf` to mint new I-addresses, while COPY receives them from `specset2ispanset` on the source document. [INV-IADDR-PROVENANCE]

---

## Code Exploration

## COPY vs INSERT: POOM Insertion Code Path Analysis

**Short answer: COPY and INSERT converge to the same `insertpm` code path.** The only divergence is upstream I-address sourcing. Everything from `insertpm` onward — including `makegappm` shifting and `isanextensionnd` coalescing — is identical.

---

### Entry Points (fns.c)

**INSERT** handler (`fns.c:84`):
```
insert() → doinsert() → inserttextingranf() [allocates new I-addrs] → docopy()
```

**COPY** handler (`fns.c:35`):
```
copy() → docopy() [directly, with source I-addrs from specset]
```

`doinsert` in `do1.c` calls `inserttextingranf` to mint new I-addresses, then calls `docopy` with the result. The COPY handler calls `docopy` directly with the source document's existing I-addresses. **Both converge into `docopy`.**

---

### docopy — Shared Spine (do1.c:45–65)

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  ...
  return (
    specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // do1.c:60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    ...
  );
}
```

`docopy` does not inspect whether the I-spans are newly allocated or transclusion-reused. It calls `insertpm` identically in both cases.

---

### insertpm — Iterates I-spans (orglinks.c:75–134)

For each I-span in the sporglset, `insertpm` calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

`crumorigin` encodes both the V-position (`vsaptr`) and the I-address (`lstream`). There is no branch on "is this transcluded content?" — both INSERT and COPY hit this line identically.

---

### insertnd — Gap-making and Dispatch (insertnd.c:15–76)

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // insertnd.c:54
    ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);  // insertnd.c:57
    break;
```

`makegappm` is called unconditionally for POOM nodes, regardless of whether content is text or transclusion.

---

### makegappm — V-address Shifting (insertnd.c:124–172)

`makegappm` finds elements after the insertion point and shifts their V-addresses:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // insertnd.c:162
    ivemodified (ptr);
    break;
```

`findaddressofsecondcutforinsert` (`insertnd.c:174`) computes the boundary for which elements need shifting. Both INSERT and COPY trigger this path for any non-extension insertion.

---

### insertcbcnd — isanextensionnd Coalescing (insertnd.c:242–275)

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {  // insertnd.c:250
        dspadd (&ptr->cwid, width, &ptr->cwid, ...);                // insertnd.c:251
        ivemodified (ptr);
        ...
        return(FALSE);  // coalesced — no new crum created
    }
}
// else: createcrum(), adopt()
```

`isanextensionnd` (`insertnd.c:301–309`) checks two conditions:
1. `infoptr->homedoc` matches the existing crum's home document
2. The existing crum's reach equals the new insertion's origin (contiguity)

For a COPY of content from document X into document Y, the `homedoc` of the incoming I-spans is X. If the POOM already contains a crum from X reaching to exactly the right I-address, coalescing fires and the existing crum is widened rather than a new one created. This is the **same coalescing logic** used when inserting adjacent text via INSERT — the only difference is what `homedoc` the I-addresses carry.

---

### Full Execution Stack (both operations)

```
insert()/copy()
  └─ docopy()                          do1.c:45
       └─ insertpm()                   orglinks.c:75
            └─ insertnd()              insertnd.c:15
                 ├─ makegappm()        insertnd.c:54   ← V-address shifting
                 └─ doinsertnd()       insertnd.c:57
                      └─ insertmorend()
                           └─ insertcbcnd()            insertnd.c:242
                                ├─ isanextensionnd()   insertnd.c:250  ← coalescing
                                └─ createcrum()/adopt()               ← new crum
                 └─ recombine()        insertnd.c:76   ← tree rebalancing
```

---

### Conclusion

COPY does **not** have a separate POOM insertion path. From `insertpm` downward, transcluded content follows the exact same code — `makegappm` shifting (`insertnd.c:54,162`), `isanextensionnd` coalescing (`insertnd.c:250–309`), and `recombine` rebalancing (`insertnd.c:76`) — as text INSERT.

The sole architectural difference is upstream: INSERT calls `inserttextingranf` to allocate fresh I-addresses in the granfilade before entering `docopy`; COPY enters `docopy` directly with pre-existing source I-addresses. Once inside `docopy`, both are structurally indistinguishable.
