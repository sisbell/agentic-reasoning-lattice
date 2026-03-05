# Consultation Answers — Address Permanence

**Inquiry:** What guarantees must the system provide about address stability? Once content is assigned an address, what operations may and may not affect that assignment?
**Date:** 2026-02-23 02:29
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> Once content is assigned an address in the system, may any operation — editing, deletion, or versioning — ever change that assignment?

### Nelson's Answer

# No. Address assignment is permanent and irrevocable.

This is not a secondary property of the system — it is the foundational invariant from which permanence, link survivability, attribution, and version comparison all derive.

## The direct statement

Nelson states the guarantee explicitly in his description of tumblers:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The word "permanent" is not casual. It means the assignment survives all future operations — not just for the lifetime of a session or a version, but for the lifetime of the docuverse.

## Why the system is designed this way

Xanadu separates two address spaces precisely to protect address permanence:

**I-Space (Invariant Space)** — where content permanently lives. An I-address is assigned once, at creation, and never changes. Content at that address never changes either.

**V-Space (Virtual Space)** — the document's current arrangement. V-addresses shift freely during editing. They are ephemeral by design.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

This quote refers to V-addresses — they change constantly. But the I-address (the byte's permanent identity) is precisely what does *not* change.

## Operation by operation

**INSERT** — Creates new content with fresh I-addresses. V-addresses after the insertion point shift: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66]. But no existing I-address is affected.

**DELETE** — Removes content from V-space only. The I-space content remains at its address:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The deleted bytes are described as "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. They are invisible in the current view but still exist at their I-address.

**REARRANGE** — A pure V-space operation. Content moves to different V-positions but its I-addresses are untouched: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

**COPY (transclusion)** — Creates a V-space reference to existing I-space content. No new I-addresses are created; no existing ones change. The bytes "have an ordinal position in the byte stream just as if they were native to the document" [LM 4/11] — they appear at new V-positions but their I-identity is unchanged.

**CREATENEWVERSION** — Creates a new V-space arrangement over the same I-space content. No I-addresses change. The new document's address "will indicate its ancestry" [LM 4/66], but the content it arranges retains its original addresses.

## The storage model makes this explicit

Nelson describes the underlying storage as append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only store, nothing is overwritten. New content is appended; old content stays where it is. Address reassignment is structurally impossible — there is no mechanism that could perform it.

## What depends on this invariant

Address permanence is not an isolated property. It is the foundation for:

- **Link survivability**: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/42-4/43] — links work because they point to I-addresses, which never change.

- **Origin traceability**: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40] — the I-address encodes which document created the byte.

- **Version comparison**: Correspondence between versions is computed from shared I-addresses. If addresses could change, correspondence would be meaningless.

- **Transclusion integrity**: When your document includes content from mine, the connection works because both documents reference the same I-address. Changing that address would sever the connection.

- **Royalty tracking**: The system knows whom to pay because it knows where content originated — from the I-address.

## Summary

The answer is unequivocal. No editing operation (INSERT, DELETE, REARRANGE), no versioning operation (CREATENEWVERSION, COPY), and no administrative action may change an address assignment. V-space arrangements change freely — that is their purpose. I-space addresses are permanent — that is *their* purpose. The entire architecture exists to maintain this separation.

---

## Question 2 [nelson]

> If a user inserts new content into the middle of an existing document, must the addresses of all previously stored content remain exactly as they were?

### Nelson's Answer

# Address Stability on INSERT

The answer depends on *which* addresses you mean. Xanadu has two address spaces, and they behave oppositely on insertion.

## I-Space Addresses: Yes, Absolutely Permanent

Every byte ever stored has a permanent I-space address that never changes, regardless of any editing operation. This is a core guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Content at an I-space address is immutable. INSERT creates *new* bytes at *fresh* I-space addresses. The previously stored content is untouched.

## V-Space Addresses: No, They Explicitly Shift

V-space addresses are the positions in a document's current virtual byte stream — "where this byte appears right now." INSERT explicitly changes them:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Nelson acknowledges this is by design and not a problem:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

## Why This Works: The Two-Space Separation

The entire point of having two address spaces is to decouple permanence from arrangement:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Links and citations point to **I-space** addresses. Editing changes **V-space** arrangements. So:

| Address type | Changes on INSERT? | Used for |
|---|---|---|
| **I-space** | Never | Links, citations, transclusion, permanence |
| **V-space** | Yes — shifts downstream positions | Current document view, user navigation |

## Summary

Previously stored content keeps its I-space addresses exactly. V-space addresses of content *after* the insertion point shift by the length of the inserted text. This is not a defect — it is the fundamental architectural reason for separating I-space from V-space. Permanence lives in I-space; flexibility lives in V-space.

---

## Question 3 [nelson]

> May the system ever assign a previously used address to different content, or must every address be permanently bound to exactly one piece of content?

### Nelson's Answer

# Address Reuse Is Forbidden

No. The system must never assign a previously used address to different content. Every address is permanently bound to exactly one piece of content. This is not a minor implementation detail — it is the foundational invariant on which nearly every Xanadu guarantee depends.

## Nelson's Explicit Statements

On permanent addressing:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

On append-only storage:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

On I-space immutability:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Content at an I-space address is permanent and immutable. The address identifies that content forever.

## How the System Creates Addresses Without Reuse

The tumbler system is designed precisely to avoid reuse. New addresses are created by **forking** — subdividing existing addresses — never by recycling old ones:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

The address space is infinite (each tumbler "digit" has no upper limit), so exhaustion is impossible. There is never a need to reclaim old addresses.

## DELETE Does Not Free Addresses

This is where the distinction matters most sharply. When content is "deleted" from a document, the I-space address remains occupied:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE removes content from V-space (the current arrangement). The I-space address — and the content bound to it — persists forever.

## Why Reuse Would Destroy the System

Every major Xanadu guarantee depends on permanent address-content binding:

| Guarantee | How reuse would break it |
|-----------|--------------------------|
| **Permanence** | A reference to address X would silently point to different content |
| **Attribution** | The I-address encodes origin; reuse would attribute new content to the wrong author |
| **Link survivability** | Links attach to I-addresses; reuse would make links point to unrelated content |
| **Transclusion** | A window to address X would show the wrong bytes |
| **Correspondence** | Version comparison relies on shared I-addresses; reuse would create false correspondences |
| **Royalties** | Per-byte payment flows to the owner of the I-address; reuse would misdirect royalties |
| **Historical backtrack** | Reconstructing past versions requires that old addresses still hold their original content |

Nelson's entire architecture rests on the premise that the I-space address is the *identity* of content. If the same address could mean different things at different times, the system collapses: links would silently lie, attribution would be meaningless, and the web of literature would be corrupted.

## Even Ghost Elements Reserve Their Positions

Addresses where nothing is stored (ghost elements) still occupy their position on the tumbler line and cannot be reassigned:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

Even an empty address is reserved. Links can point to it. Reassigning it would break those links.

## Summary

The permanent binding of address to content is axiomatic. The entire system — append-only storage, forking address allocation, V-space/I-space separation, link survivability, transclusion, attribution, royalties, and historical backtrack — is engineered around the guarantee that once an address is assigned, it means one thing, forever. Nelson designed the tumbler system specifically so that this property holds without central coordination, without running out of space, and without ever needing to reclaim old addresses.

---

## Question 4 [nelson]

> When a new version of a document is created, do the shared passages retain their original addresses, or does versioning produce new addresses for the same content?

### Nelson's Answer

## Shared passages retain their original I-space addresses

When you create a new version, **no new addresses are produced for existing content**. The new version is a new V-space arrangement — a new mapping — that points to the same I-space bytes as the original. Content lives permanently at its I-space address; versions are just different ways of arranging references to that content.

### The architectural basis

Nelson's two-address-space design makes this inevitable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space addresses are permanent and immutable. V-space addresses are ephemeral views. A version IS a V-space arrangement, not a new allocation of I-space:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The CREATENEWVERSION operation confirms this:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

It creates a new document (new V-space, new document tumbler) **with the contents** of the original — meaning the new V-stream maps to the same I-space bytes. No duplication occurs.

### Why this must be so

Three of my fundamental guarantees depend on shared I-addresses across versions:

1. **Correspondence.** The system identifies which parts of two versions match by checking whether their V-positions map to the same I-address. If versioning produced new addresses, correspondence would be destroyed:

   > "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

2. **Link survivability.** Links point to I-space addresses. If a link targets bytes in version 1, and version 2 shares those same I-addresses, the link reaches into both versions automatically:

   > "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

   If versioning produced new I-addresses, this refractive following would be impossible — there would be no shared identity between versions.

3. **Non-duplication.** The entire storage model rejects copying:

   > "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents." [LM 2/36]

### The analogy

Think of the library stacks (I-space) and reading lists (V-space):

```
I-Space (permanent)              V-Space (arrangements)
┌─────────────────────┐          ┌──────────────────────┐
│ Shelf A: "hello"    │          │ Document v1:         │
│ Shelf B: " world"   │    ──►   │   [ref A, ref B]     │  → "hello world"
│ Shelf C: "!"        │          │                      │
│                     │          │ Document v2:         │
│ (never changes)     │    ──►   │   [ref A, ref C]     │  → "hello!"
└─────────────────────┘          └──────────────────────┘
```

Version 2 still points to Shelf A for "hello" — same address, same bytes. Only the arrangement changed (Shelf B replaced by Shelf C in the V-stream). The byte "hello" was not re-stored; it was re-referenced.

### What IS new in a version

Only two things get fresh addresses:

- **The document/version tumbler itself** — the new version gets a new document address whose digits "indicate its ancestry" [LM 4/66]
- **Any genuinely new content** — if you edit the new version by inserting text, those new bytes get fresh I-space addresses (as with any INSERT)

But the passages carried over from the parent version keep their original I-space addresses. That shared identity is what makes the system work — it is the structural basis for correspondence, link refractive following, transclusion tracking, and royalty attribution.

---

## Question 5 [nelson]

> If content is deleted from a document, does its address cease to exist, or must the address remain valid and the content remain retrievable through other means?

### Nelson's Answer

# Deletion Does Not Destroy: The Address Persists, The Content Remains

The answer is unambiguous across multiple passages in Literary Machines. **The address remains valid forever. The content remains retrievable. "Deletion" is removal from the current view, not destruction of the underlying content.**

---

## The Two Address Spaces Are Key

Xanadu maintains two distinct address spaces, and deletion affects only one of them:

- **I-Space (Invariant Space):** Where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.
- **V-Space (Virtual Space):** The document's current arrangement. A view that references I-space content. Can be rearranged across versions.

Deletion removes content from V-space — the current arrangement — but leaves I-space untouched.

---

## Nelson's Explicit Statement on Deleted Bytes

Nelson's diagram on page 4/9 shows "DELETED BYTES" as a valid system state with this annotation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Note the precise language: **"not currently addressable"** — not "destroyed," not "gone," not "address invalidated." The bytes exist; they are merely not reachable through the current V-space arrangement.

And further:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

---

## The Append-Only Storage Model

Nelson explicitly designed the storage system to reject destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is appended, never overwritten. The I-space address assigned at creation is permanent. There is no mechanism for removing content from I-space.

---

## Historical Backtrack Guarantees Retrieval

The entire version system depends on deleted content remaining retrievable:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If deletion destroyed content, historical backtrack would be impossible. Nelson treats this as a fundamental guarantee, not an optional feature.

---

## The Permanence of Addresses

Nelson is explicit that addresses, once assigned, never become invalid:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This applies to all addresses, including those of "deleted" content. The I-space address of a byte that has been removed from V-space remains as valid as any other address in the docuverse.

---

## What Deletion Affects and Does Not Affect

| Aspect | Affected by DELETE? |
|--------|---------------------|
| V-space arrangement (current view) | **YES** — content removed from current arrangement |
| I-space content (permanent storage) | **NO** — bytes remain forever |
| I-space address validity | **NO** — address remains valid |
| Previous versions | **NO** — still contain the content |
| Transclusions in other documents | **NO** — other documents still show it |
| Links pointing to that content | **NO** — still resolve via I-space |
| Home document traceability | **NO** — I-address still encodes origin |

---

## Links Survive Precisely Because Content Survives

The link survivability guarantee depends on this:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links point to I-space addresses. Since deletion only affects V-space, links to "deleted" content continue to resolve. The content is still there in I-space; it simply isn't part of the document's current arrangement.

---

## The Non-Destruction Guarantee

Nelson states this as a design principle, not merely a feature:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And the storage philosophy that underlies it:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

Editing — including deletion — re-twists the braid. It does not cut strands out of existence.

---

## Summary

In Xanadu, deletion is **rearrangement**, not **destruction**. The I-space address remains valid. The content remains retrievable — through historical backtrack, through other versions, through transclusions in other documents, and through any links that point to it. The address never ceases to exist. This is not an incidental property but the foundational design principle of the entire system.

---

## Question 6 [nelson]

> When the same content appears in multiple documents through transclusion, must it be identified by one single address everywhere, or may different documents use different addresses for the same content?

### Nelson's Answer

## Transcluded content must share one I-space address everywhere

The answer is unambiguous: transcluded content is identified by **one single I-space address** across all documents that include it. This is not an implementation detail — it is the architectural foundation on which correspondence, attribution, royalties, and discovery all depend.

### The core mechanism

Nelson's two-space architecture separates **identity** (I-space) from **arrangement** (V-space). Each document has its own V-space — a virtual byte stream where content appears at positions local to that document. But the underlying I-space address is permanent and singular:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their **home locations**." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called **inclusions** or **virtual copies**." [LM 4/11]

The term "virtual copies" is precise: the content is not duplicated. Multiple V-space positions in different documents map to the **same** I-space address. The content exists once; it is referenced many times.

### Why identity must be shared

Nelson's system depends on shared I-addresses for at least four capabilities:

**1. Correspondence.** Version comparison works because shared I-space origin defines which parts match:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

If transcluded content received a new address in each document, the system could not determine correspondence — it would see unrelated bytes that happen to have the same value.

**2. Discovery (FINDDOCSCONTAINING).** This operation finds all documents containing specified material:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

This works by matching I-space addresses. If each document assigned its own address to transcluded content, this operation would be impossible without full-text comparison.

**3. Attribution.** Origin traceability is structural:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The I-address encodes which document created the bytes (the Document field of the tumbler). If transclusion created new addresses, attribution would be severed.

**4. Royalties.** Automatic payment requires knowing who created the content:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

"Determined automatically" means by examining the I-addresses — native bytes belong to this document's owner, transcluded bytes belong to their home document's owner.

### The critical distinction: identity vs. value

Content identity in Xanadu is based on **provenance**, not **value**. Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address. This is how the system distinguishes "wrote the same words independently" from "quoted from the original."

The COPY operation — which is Xanadu's transclusion mechanism — makes this explicit:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This creates a V-space mapping to the **existing** I-space content. No new I-space content is created.

### What differs across documents: V-space addresses only

Each document that transcludes the same content will have **different V-space positions** for it. If Alice's document has "hello world" at V-positions 1-11, and Bob transcludes it, it might appear at V-positions 47-57 in Bob's document. The V-addresses differ; the I-addresses are identical.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are ephemeral and local. I-addresses are permanent and universal.

### Summary

| Address type | Same across documents? | Purpose |
|---|---|---|
| **I-space** | Yes — always identical | Permanent identity, attribution, royalty |
| **V-space** | No — differs per document | Local arrangement, user-facing position |

The single-I-address-everywhere property is what makes transclusion fundamentally different from copying. It is not a design choice that could go either way — it is the mechanism by which Nelson's guarantees of attribution, correspondence, discovery, and automatic royalty are achieved.

---

## Question 7 [nelson]

> Must links continue to function correctly after editing operations precisely because the addresses they reference are guaranteed never to change?

### Nelson's Answer

# Yes — But the Precision Matters

The answer is yes, though the mechanism is more specific than "addresses never change." It depends on *which* addresses links reference, and *which* addresses editing changes. These are different address spaces, and their separation is the architectural foundation.

## Two Address Spaces, Two Stability Properties

Xanadu has two address spaces with opposite stability characteristics:

**I-space addresses are permanent:**
> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**V-space addresses are ephemeral:**
> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Links attach to I-space (permanent content identity). Editing changes V-space (current arrangement). Because links and edits operate on different address spaces, they do not interfere with each other.

## Nelson's Explicit Statement

Nelson states the connection directly:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And more fully:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

## The Chain of Reasoning

The full argument has three links:

1. **I-space addresses are permanent** — content at an I-space address never changes, and the address is never reassigned. This follows from the append-only storage model: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

2. **Links reference I-space addresses** — a link is "a strap between bytes," where "bytes" means content at permanent I-space locations, not positions in the current V-space arrangement.

3. **Editing changes only V-space** — INSERT, DELETE, REARRANGE, and COPY all modify the V-space mapping (which I-space bytes appear where in the document's current view), but never alter I-space content or addresses.

Therefore: since links point to something that editing cannot change, links survive editing.

## The Tumbler Guarantee Supports This

The broader tumbler permanence guarantee reinforces the I-space half:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This ensures that I-space addresses are not merely stable within a session but permanent across the lifetime of the docuverse.

## DELETE Does Not Break the Chain

Even deletion does not threaten this architecture, because DELETE operates on V-space only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Deleted" content persists in I-space. Links to it still resolve. The bytes are merely removed from the current V-space view.

## The Boundary Condition

Nelson does acknowledge one limit to survivability:

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

This "if anything is left" condition refers to V-space reachability — whether any bytes at the endset remain present in some accessible document view. If content is deleted from every version and every transclusion, the link's endset has no V-space presence (though the I-space content technically persists for historical backtrack).

## Summary

Links survive editing operations precisely because:

- They reference **I-space addresses** (permanent, immutable)
- Editing modifies **V-space addresses** (ephemeral, mutable)
- These are **different address spaces** by design

The guarantee that I-space addresses never change is necessary. But the full explanation requires the architectural separation: links point to the permanent layer, edits touch only the ephemeral layer. Nelson designed it this way deliberately — the I-space/V-space split exists *in order to* make links survivable while keeping editing free.

---

## Question 8 [nelson]

> Must every act of storing new content produce a fresh address that has never been used before and will never be used again?

### Nelson's Answer

# Yes — Fresh Content Requires Fresh Addresses

Every act of storing genuinely new content in Xanadu must produce an address that has never been used before and will never be reused. This is not a single explicit rule but the convergence of several interlocking guarantees Nelson specifies.

## 1. Addresses Are Permanent and Immutable

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once an address is assigned, it is occupied forever. This immediately implies that new content cannot be placed at an existing address — the address is already taken.

## 2. Content at an I-Address Never Changes

I-space addresses are "absolute and immutable" — content at an I-space address never changes after creation. If content is immutable at its address, and addresses are permanent, then storing different content requires a different address. There is no alternative.

## 3. Storage Is Append-Only

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The append-only model means the address space grows monotonically forward. New content is appended; nothing is overwritten. This structurally prevents address reuse.

## 4. Address Creation Is Monotonic Forking

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

New addresses are created by sequential forking: 2.1, then 2.2, then 2.3. The process only moves forward. Nelson's example makes the monotonicity explicit — you fork successive items, never returning to reuse a previously allocated position.

## 5. "Deleted" Content Still Occupies Its Address

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Even deletion does not free an address for reuse. The bytes remain in I-space; only the V-space mapping is removed. The address continues to be occupied by its original content.

## The Crucial Distinction: New Content vs. New Arrangement

Not every operation that touches storage produces fresh I-space addresses. The distinction is between creating **new content** and creating **new arrangements of existing content**:

| Operation | Fresh I-addresses? | What happens |
|-----------|-------------------|--------------|
| **INSERT** | Yes | New bytes enter I-space at fresh addresses |
| **APPEND** | Yes | New bytes appended to I-space |
| **COPY** | No | V-space mapping to existing I-addresses (transclusion) |
| **CREATENEWVERSION** | No (for content) | New document address, but text content shares existing I-addresses |
| **REARRANGE** | No | Pure V-space operation |
| **DELETE** | No | V-space mapping removed; I-space unchanged |

Nelson makes this explicit for COPY:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Transclusion reuses I-addresses by design — that is exactly what makes attribution structural and royalty tracking automatic. The same bytes, at their permanent home addresses, are referenced from multiple V-space arrangements.

## Why This Matters

The freshness requirement is not arbitrary. It is load-bearing for three of Nelson's fundamental guarantees:

1. **Attribution**: Every byte traces to its origin through its I-address. If addresses were reused, origin traceability would break — you could not distinguish "wrote the same words independently" from "quoted from the original."

2. **Permanence**: Citations and links point to I-addresses. If an address could be recycled for different content, every existing reference to the old content would silently become a reference to something else — a silent corruption of the docuverse.

3. **Correspondence**: Version comparison works because shared I-addresses reveal which parts of two versions came from the same origin. Address reuse would create false correspondences.

## Summary

Yes. Every act of storing new content must produce a fresh address. This follows necessarily from the conjunction of permanent addresses, immutable content at those addresses, append-only storage, and monotonic forking. The address, once baptized, belongs to that content forever. The system grows; it never overwrites.

---

## Question 9 [nelson]

> If a user rearranges passages within a document — moving a paragraph from one position to another — must the content's permanent address remain unchanged despite its new position?

### Nelson's Answer

## Yes — absolutely. The content's permanent address is unchanged by rearrangement.

This is one of the most fundamental architectural commitments in Xanadu: the separation of **I-space** (where content permanently lives) from **V-space** (the document's current arrangement of that content).

### The Two Address Spaces

When you create content, it receives a permanent **I-space address** — a tumbler encoding its server, account, document, and element position. This address is invariant:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The document's **V-space** is the current arrangement — the reading order a user sees. V-addresses are ephemeral positions (1, 2, 3...) that shift with every edit. Rearranging a paragraph changes V-space; it does not touch I-space.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### REARRANGE Is a Pure V-Space Operation

The REARRANGE command transposes regions of the virtual byte stream:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

This changes which I-space content maps to which V-space positions. The I-space addresses of every byte involved remain exactly as they were at creation.

### Why This Matters: Link Survivability

The entire link system depends on this guarantee. Links attach to I-space addresses, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

And explicitly including rearrangement:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

If rearrangement changed permanent addresses, links would break every time a user moved a paragraph — defeating the entire purpose.

### The Analogy

Think of it as a library (I-space) and a reading list (V-space):

- The library shelf location of a book never changes
- Your reading list can reorder those books however you like
- A citation to "shelf A, book 7" always finds the same book regardless of which reading list it appears on

Or as Nelson puts it:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Xanadu's entire design exists to reject that model. Content is stored once, permanently, at a fixed address. Documents are views — rearrangeable mappings over that permanent content. Rearranging the view cannot alter the thing being viewed.

### Summary

| What changes during REARRANGE | What stays fixed |
|-------------------------------|-----------------|
| V-space positions (reading order) | I-space addresses (permanent identity) |
| Which V-address maps to which content | The content itself |
| The user's visible arrangement | Links to that content |
| The document's current shape | Attribution and origin traceability |

The permanent address is the content's *identity*. Rearrangement changes *arrangement*. These are, by design, completely independent.

---

## Question 10 [nelson]

> Must the system be able to answer, for any valid address, what content was originally stored there, regardless of how many edits or versions have occurred since?

### Nelson's Answer

# Yes — Unconditionally for I-Space Addresses

This is not merely a feature but the foundational architectural commitment of the system. For any valid I-space address where content was stored, the system must always return that exact content, no matter what has happened since.

## The Core Guarantee

I-space addresses are permanent and immutable. Content at an I-space address never changes after creation:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The storage model is append-only by design:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The permascroll (Nelson's "hyperfile") never overwrites, never removes. Every byte ever created has an eternal address. This is stated as a rejection of the conventional model:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

## Edits Do Not Affect It

Editing operates on V-space (the document's current arrangement), not I-space (where content permanently lives). The distinction is absolute:

- **INSERT** adds new content to I-space and updates the V-space mapping
- **DELETE** removes content from V-space only; I-space is unchanged
- **REARRANGE** is a pure V-space operation
- **CREATENEWVERSION** creates a new V-space arrangement over the same I-space content

Nelson makes this explicit on the DELETE case:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Not currently addressable" means not reachable through V-space in the current version. The I-space address remains valid and the content remains retrievable.

## Why This Must Be So

Three guarantees depend on I-space permanence:

**1. Link survivability.** Links attach to I-space addresses. If content at those addresses could disappear, links would break — violating the fundamental promise:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

**2. Origin traceability.** Attribution is structural — the I-address encodes which document created the content:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

If I-space content could be lost, attribution would be lost with it.

**3. Historical backtrack.** The ability to reconstruct any previous state requires that all content from all states remain available:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

## The Necessary Qualification: V-Space Is Different

For V-space addresses, the answer is conditional: you must specify *which version*. A V-address like "position 5 in document D" is ephemeral — it shifts with every INSERT and DELETE. But for any *version* of the document, the system can reconstruct the V-space arrangement and resolve any V-address within it. This is the "part-pounce" guarantee:

> "This system is built around the assumption that you are reading from a screen, not from paper. When you 'go to' a certain part of a document, the whole document is not ready to show; yet the system gives you that part instantly, materializing it for you from the many fragments of its actual storage." [LM 2/16]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes; the I-address does not. The system resolves V-addresses by mapping through the version's POOM to I-space, where content lives permanently.

## Ghost Elements Are Not a Counterexample

Some valid tumbler addresses have nothing stored at them — these are "ghost elements":

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

The guarantee applies to addresses where content *was* stored, not to all conceivable addresses. A ghost element was never "originally stored" — it exists only as a potential position. The question "what was stored here?" has the answer "nothing, and nothing was ever stored here."

## Summary

For any I-space address where content was created: **yes, unconditionally and permanently.** This is not a feature to be weighed against cost — it is the architectural foundation upon which permanence, attribution, link survivability, version history, and royalty accounting all depend. Without it, the system is not Xanadu.

---

## Question 11 [gregory]

> After INSERT stores text at a given I-address in the granfilade, is there any operation or sequence of operations that can modify the bytes stored at that I-address, or is the granfilade strictly append-only with no in-place mutation?

### Gregory's Answer

## KB Synthesis

# Answer: Granfilade is Strictly Append-Only

The granfilade is **strictly append-only** with **no in-place mutation** of content. Once bytes are stored at an I-address, no operation in the system can modify those bytes.

## Evidence from the Knowledge Base

### Core Immutability Invariant

[INV-IADDR-IMMUTABILITY] states definitively:

> "I-addresses, once allocated in the granfilade, are permanent and immutable. The granfilade is append-only — `inserttextingranf` always allocates fresh addresses at the end. There is no mechanism to reuse, reassign, or deallocate I-addresses."

And further:

> "No operation in the system reassigns or destroys an I-address. This is what makes cross-document identity (transclusion) and version comparison possible — both depend on I-addresses being stable reference points."

### DELETE Does Not Touch the Granfilade

[FC-GRANF-ON-DELETE] provides the explicit frame condition:

> "DELETE and REARRANGE are frame-condition-preserving with respect to the granfilade. These operations modify only the spanfilade (V-to-I mappings) and leave the granfilade (I-space content storage) completely unchanged."

The formal property is: `∀ op ∈ {DELETE, REARRANGE} : granf_after(op) = granf_before(op)`

[ST-DELETE] confirms:

> "DELETE destroys the local V-to-I mapping but does NOT destroy the I-addresses themselves. The content bytes persist in the granfilade, the spanfilade still indexes them, and any other document sharing those I-addresses retains its mapping."

### No Address Reuse

[INV-NO-IADDR-REUSE] closes any potential gap:

> "Deleted I-addresses are never reused. Since the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum, 'gaps' in V-space created by DELETE do not create 'gaps' in I-space. The I-address space grows strictly monotonically and permanently. There is no free-list, no gap-tracking, and no garbage collection of I-addresses."

### What INSERT Actually Does

[ST-INSERT] clarifies that INSERT only *adds* to the granfilade:

> "During text insertion (`inserttextgr`), I-addresses are allocated contiguously: the start address is found via `findisatoinsertgr`, then advanced by text length... The resulting I-span width equals the character count for text content."

The allocation is always forward, never reusing or modifying existing addresses.

### Cross-Document Frame Condition

[FC-DELETE-CROSS-DOC] confirms the isolation:

> "DELETE in one document has zero effect on any other document's POOM mappings. If document T transcluded content from document D (sharing I-addresses via COPY), and D subsequently deletes that content, T's POOM still maps to the shared I-addresses. T's content is unaffected — the transclusion survives the source document's deletion."

This only works because the granfilade content at those I-addresses remains unchanged.

## Complete List of Operations and Their Granfilade Effects

| Operation | Granfilade Effect |
|-----------|-------------------|
| **INSERT** | Appends new content at fresh I-addresses |
| **DELETE** | No effect (only removes V→I mappings) |
| **REARRANGE** | No effect (only reorders V-positions) |
| **VCOPY** | No effect (shares existing I-addresses) |
| **CREATENEWVERSION** | Adds one document address entry, no content modification |
| **CREATELINK** | Adds one link orgl entry, no content modification |

## Conclusion

The granfilade operates under a **write-once** model. The bytes stored at any I-address during INSERT remain permanently unchanged at that address. All mutation operations (DELETE, REARRANGE) operate exclusively on the POOM layer, which maps V-addresses to I-addresses. The granfilade itself is an immutable, monotonically growing store.

This design is what enables the content identity system: documents can safely share I-addresses knowing the content will never change, and versions/transclusions maintain referential integrity indefinitely.

## Code Exploration

Based on my comprehensive examination of the udanax-green C source code, I can definitively answer your question:

## The Granfilade is Strictly Append-Only — No In-Place Mutation

After INSERT stores text at an I-address in the granfilade, **there is no operation or sequence of operations that can modify those stored bytes**. The granfilade is immutable once written.

### Evidence from Source Code

#### 1. INSERT Operation Creates New Storage Only

The `inserttextgr` function [`granf2.c:83-109`] allocates fresh I-addresses and stores text:

```c
inserttextgr(...) {
    findisatoinsertgr(..., &lsa);  // Find NEW I-address
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...); // Copy bytes
    insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);  // Store at I-address
}
```

The `insertseq` function [`insert.c:17-70`] creates a new crum (bottom-level storage node):

```c
insertseq(...) {
    new = createcrum(0, (INT)ptr->cenftype);  // Allocate NEW crum
    moveinfo(info, &((typecbc *)new)->cinfo);  // Copy text into NEW crum
}
```

The only case where an existing crum is touched is `fillupcbcseq` [`insert.c:75-103`], which appends to a crum's buffer **if there's remaining space**. But this is still insertion at the END of existing bytes, not modification:

```c
fillupcbcseq(...) {
    crumlength = ptr->cinfo.granstuff.textstuff.textlength;
    remainingroom = GRANTEXTLENGTH - crumlength;
    movmem(&info->..., (char*)(&(ptr->cinfo.granstuff.textstuff))+crumlength, textlength);
    // Appends AFTER existing bytes at offset crumlength
}
```

#### 2. No Write Operations to Stored Text

I searched for all operations on `textstring`:

```bash
grep 'textstring\[.*\]=' backend/*
```

Result: **Zero write operations** found after initial storage. All `movmem` calls involving `textstring` are:
- Initial storage during INSERT [`granf2.c:98`]
- Disk I/O operations [`corediskout.c:242`, `corediskin.c:260`]
- Retrieval (copying FROM storage TO output) [`context.c:308`]

#### 3. DELETE Deallocates, Never Modifies

The `deleteseq` function [`edit.c:16-28`] removes crums by freeing memory:

```c
deleteseq(...) {
    ptr = (typecbc *) context->corecrum;
    freecrum((typecorecrum*)&context->corecrum);  // DEALLOCATE, don't modify
}
```

The `freecrum` function [`credel.c:434-453`] calls `efree((char*)ptr)` to return memory to the allocator. It never touches the text bytes.

#### 4. DELETE_VSPAN Operates on POOM, Not Granfilade

Document deletion via `deletevspanpm` [`orglinks.c:145-152`] operates on the POOM (Permutation Matrix enfilade), which stores V→I mappings:

```c
deletevspanpm(...) {
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    // Operates on dimension V (virtual addresses), not the granfilade
}
```

This removes **references** to I-addresses from the document structure, but the bytes at those I-addresses remain unchanged in the granfilade.

#### 5. Complete FEBE Operation Inventory

Examining all FEBE operations in [`fns.c`]:

- **insert** — appends NEW text at NEW I-addresses
- **copy** — creates NEW V→I references (no granfilade write)
- **deletevspan** — removes V→I references from POOM (no granfilade write)
- **rearrange** — reorders V→I mappings (no granfilade write)
- **createlink** — appends NEW link at NEW I-address
- **createnewdocument** — creates NEW POOM structure
- **createnewversion** — copies V→I references to NEW POOM
- **retrieve operations** — READ-ONLY access

**No UPDATE, MODIFY, or OVERWRITE operations exist.**

### Architectural Implications

This immutability is fundamental to Xanadu's design:

1. **Transclusion works** because I-addresses are stable — multiple documents can safely reference the same I-addresses
2. **Version control is implicit** — all versions share immutable I-addressed content
3. **Content-addressed storage** — bytes at I-address `X` never change, enabling hash-based verification
4. **Garbage collection only** — unreferenced I-addresses can be freed when no POOM references them, but while alive they're immutable

### Conclusion

The granfilade is **strictly append-only**. Once `inserttextgr` stores bytes at an I-address, those bytes are immutable for the lifetime of that storage. No operation modifies, overwrites, or updates the content. The only ways to "change" stored bytes are:

1. **Delete the crum** (freeing memory when unreferenced)
2. **Write NEW bytes** at a NEW I-address

This is a foundational invariant of the udanax-green architecture.

---

## Question 12 [gregory]

> When DELETE removes a V-span and the corresponding I-addresses become unreferenced by any POOM, can those same I-addresses ever be reassigned to new content by a subsequent INSERT or CREATELINK allocation?

### Gregory's Answer

## KB Synthesis

# Answer: I-addresses Cannot Be Reused

**No.** I-addresses that become unreferenced after DELETE can never be reassigned to new content by subsequent INSERT or CREATELINK operations.

## Mechanism

The allocation algorithm queries the granfilade tree to find the highest existing I-address, then allocates by incrementing from that maximum [ST-INSERT, INV-MONOTONIC]. Since DELETE does not remove I-addresses from the granfilade, "deleted" I-addresses remain in the tree and continue to influence allocation [FC-GRANF-ON-DELETE].

## Frame Conditions

DELETE operates exclusively on the POOM (V-to-I mappings), leaving the granfilade completely unchanged [ST-DELETE, FC-GRANF-ON-DELETE]:

```
∀ op ∈ {DELETE, REARRANGE} : granf_after(op) = granf_before(op)
```

The granfilade is append-only. `inserttextingranf` always allocates fresh addresses at the end; there is no mechanism to reclaim or reuse previously allocated addresses [INV-IADDR-IMMUTABILITY].

## Invariant

[INV-NO-IADDR-REUSE] explicitly states:

> Deleted I-addresses are never reused. Since the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum, "gaps" in V-space created by DELETE do not create "gaps" in I-space.

Formally: `∀ i ∈ I-space : once_allocated(i) ⟹ always_allocated(i)`

## Concrete Example

From [INV-NO-IADDR-REUSE]:

```
Document has I.1, I.2, I.3
Delete the character at I.2 from V-space
  → Granfilade still contains I.1, I.2, I.3 (all three persist)
  
Next allocation:
  findpreviousisagr returns I.3
  → allocates I.4
  
I.2 is never reused, even though no V-position maps to it
```

## CREATELINK Uses Same Mechanism

CREATELINK allocates via the same granfilade query-and-increment [INV-MONOTONIC, ST-INSERT]. Both text and link orgls compete for the same monotonic I-address sequence — allocation is `next_iaddr(granf) = max_iaddr(granf) + 1` regardless of entity type.

## Consequence

The no-reuse guarantee is essential for transclusion integrity. If document B transcludes content from document A via shared I-addresses, deleting that content from A's V-space cannot cause those I-addresses to be reallocated to different content in a later INSERT. B's transclusion remains anchored to the original I-addresses indefinitely [INV-TRANSITIVE-IDENTITY, INT-TRANSCLUSION].

## Code Exploration

Perfect! I found Finding 0061 which already thoroughly documents this behavior. Let me provide you with a complete answer based on the source code analysis and existing documentation.

## Answer: I-Addresses Are NEVER Reused

**No, I-addresses that become unreferenced cannot be reassigned.** The allocation mechanism is strictly monotonic and has no awareness of which I-addresses are "referenced" vs "unreferenced."

### Code Evidence

#### Allocation Path

When INSERT or CREATELINK allocates new I-addresses, the path is:

1. **`granf2.c:findisatoinsertgr` [130-156]** - Main allocation entry point
2. **`granf2.c:findisatoinsertmolecule` [158-181]** - For text/link content (ATOM types)
3. **`granf2.c:findpreviousisagr` [255-278]** - Finds highest existing I-address

The critical allocation logic in `findisatoinsertmolecule`:

```c
// granf2.c:162-169
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);  // ← Increment from highest
```

**Key observation:** Line 164 calls `findpreviousisagr`, which traverses the granfilade tree to find the **highest existing I-address**. Line 169 then **increments** that address by 1 to allocate the next I-address.

#### No Reference Tracking

The allocation algorithm:
- **Queries only the granfilade tree structure** - it sees which I-addresses exist, not which are "referenced"
- **Has no awareness of the POOM** - it doesn't check which I-addresses are mapped from V-space
- **Maintains no free-list** - there's no data structure tracking freed/unreferenced I-addresses
- **Is stateless** - each allocation independently queries the tree; no session counter

#### Delete Path Does NOT Free I-Addresses

When DELETE removes a V-span:

```c
// edit.c:30-75 - deletend (POOM deletion)
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
        case 1:
            disown ((typecorecrum*)ptr);      // Release ownership
            subtreefree ((typecorecrum*)ptr); // Free memory
            break;
```

**What DELETE does:**
- Removes entries from the **spanfilade** (V→I mappings) - `edit.c:deletend` [30-75]
- Frees the in-memory tree nodes
- Updates the POOM structure

**What DELETE does NOT do:**
- Mark I-addresses as "unreferenced" or "available for reuse"
- Remove content from the **granfilade** (I-space content storage)
- Maintain any "freelist" of reusable addresses

The granfilade content remains permanently. As Finding 0061 states: *"bytes never die, addresses never change."*

### Proof from Existing Tests

Finding 0061 contains empirical evidence from the `interleaved_insert_delete` test:

| Operation | V-span width | Analysis |
|-----------|--------------|----------|
| INSERT "AAA" | 0.3 | Allocates I.1, I.2, I.3 |
| DELETE char at 1.2 | 0.2 | Removes V→I.2 mapping (I.2 becomes unreferenced) |
| INSERT "BBB" | **0.5** | Allocates I.4, I.5, I.6 (NOT reusing I.2!) |

If unreferenced I-addresses were reused, the width would be 0.2 + 0.1 = 0.3. Instead, it's 0.2 + 0.3 = 0.5, proving that I.2 remains in the granfilade and I.4-I.6 are freshly allocated.

### Why This Design?

This monotonic allocation without garbage collection has specific advantages:

1. **Permanent content addressing** - I-addresses never change, enabling stable transclusion
2. **Simple allocation logic** - No complex free-list management or reference counting
3. **Multi-document safety** - Content referenced by ANY document (even via transclusion) remains accessible

The trade-off is **unbounded granfilade growth** - deleted content accumulates as "garbage" I-addresses that continue to influence allocation but are never reclaimed.

### Complete Answer

**Can unreferenced I-addresses be reassigned?**

**No.** The allocation mechanism (`findpreviousisagr` + increment) has no concept of "unreferenced." It only knows:
1. What I-addresses currently exist in the granfilade tree
2. The next sequential I-address is the highest existing + 1

Even if an I-address becomes unreferenced by all POOMs:
- It remains in the granfilade tree structure
- It continues to influence the "highest I-address" calculation
- Future allocations skip over it and continue incrementing

This is by design: Xanadu's "bytes never die" philosophy means content at I-addresses is permanent, even if no current V-span references it.

### Code Citations

- `backend/granf2.c:130-156` - `findisatoinsertgr` (allocation entry point)
- `backend/granf2.c:158-181` - `findisatoinsertmolecule` (query + increment strategy)
- `backend/granf2.c:255-278` - `findpreviousisagr` (finds highest existing I-address)
- `backend/edit.c:30-75` - `deletend` (deletes from POOM, not granfilade)
- `findings/0061-iaddress-allocation-monotonic.md` - Comprehensive finding with test evidence

---

## Question 13 [gregory]

> Does REARRANGE (both 3-cut pivot and 4-cut swap) preserve the I-address component of every affected POOM entry exactly, changing only V-displacements while leaving I-displacements and I-widths untouched?

### Gregory's Answer

## KB Synthesis

Yes, REARRANGE (both pivot and swap) preserves the I-address component of every affected POOM entry exactly, modifying only V-displacements and leaving I-displacements and I-widths untouched.

## Direct Evidence

[ST-REARRANGE] Finding 0056 provides the most explicit confirmation:

> "Rearrange preserves I-addresses exactly. The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched. No new I-addresses are allocated, no content is duplicated in the permascroll, and the same enfilade nodes (crums) are retained."

The critical code line is:
```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```

where `index` is the V-dimension parameter, meaning only `cdsp.dsas[V]` (V-displacement) is modified, never `cdsp.dsas[I]` (I-displacement).

## Supporting Invariants

[INV-REARRANGE-IDENTITY] across Findings 0016, 0018, and 0056 consistently states:

- Finding 0016: "After a pivot or swap, the moved content retains the same I-addresses it had before."
- Finding 0018: "The set of I-addresses in a document is invariant across rearrangement. `I-addresses(D_before_rearrange) = I-addresses(D_after_rearrange)`"
- Finding 0056: "Formally: `∀ c ∈ content(doc): i_addr(c, doc_after) = i_addr(c, doc_before)`"

## POOM Structure Context

[SS-POOM-BOTTOM-CRUM] Finding 0076 documents that each bottom crum contains:
```
BottomCrum = {
  origin: { dsas[I]: Tumbler,  dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler,  dsas[V]: Tumbler }
}
```

REARRANGE modifies only `origin.dsas[V]` (V-displacement), leaving `origin.dsas[I]` (I-displacement) and `width.dsas[I]` (I-width) unchanged.

## Downstream Consequences

[INV-REARRANGE-LINK-SURVIVAL] Finding 0016 confirms this preservation is observable:

> "Links bound to rearranged content remain discoverable after pivot or swap. Because links are bound to I-addresses (not V-addresses), moving content to new V-positions does not break link bindings."

Links continue to work because their I-address-based indexing remains valid—which requires that rearranged content preserve its I-addresses exactly.

## Mechanism

REARRANGE operates by computing V-dimension offsets from cut points (`makeoffsetsfor3or4cuts`), then applying these offsets to each affected entry's V-displacement via `tumbleradd`. The algorithm never accesses the I-dimension fields. From [ST-REARRANGE] Finding 0056:

> "The operation modifies V-addresses exclusively—it calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` which updates the displacement's V-address component. No I-addresses are touched, no content is copied, no new permascroll entries are created."

**Answer: Yes, REARRANGE preserves all I-address components (both I-displacements and I-widths) exactly. Only V-displacements are modified.**

## Code Exploration

Based on my analysis of the C source code, I can now provide a definitive answer to your question.

## Answer: YES - REARRANGE Preserves I-Addresses Exactly

REARRANGE (both 3-cut pivot and 4-cut swap) **preserves the I-address component of every affected POOM entry exactly**, changing only V-displacements while leaving I-displacements and I-widths completely untouched.

---

## Evidence from Source Code

### 1. POOM Data Structure

Each POOM crum contains two fields [**enf.h:47-48**, **enf.h:71-72**]:

```c
struct structcorecrumhedr {
    ...
    typewid cwid;    // width in both dimensions
    typedsp cdsp;    // displacement in both dimensions
    ...
};
```

These are defined as [**wisp.h:50-54**]:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];  // MAXLOXIZE = 2
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

With the dimension indexes [**wisp.h:18-20**]:

```c
/* wid and dsp indexes for pm */
#define I  0
#define V  1
```

So each POOM crum has **four components**:
- `cwid.dsas[I]` — I-width
- `cwid.dsas[V]` — V-width  
- `cdsp.dsas[I]` — I-displacement
- `cdsp.dsas[V]` — V-displacement

### 2. REARRANGE Execution Path

The call chain is:

1. `fns.c:159` → `rearrange(taskptr)` - FEBE protocol handler
2. `do1.c:34` → `dorearrange(...)` calls `rearrangepm(...)`
3. `orglinks.c:137` → `rearrangepm(...)` calls:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);  // ← Note: V dimension
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

The critical parameter is `V` — the dimension being rearranged.

### 3. The Core Modification in rearrangend

In `rearrangend` [**edit.c:78-160**], there is **exactly one location** where crum data is modified:

```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
{
    ...
    knives.dimension = index;  // index == V from rearrangepm
    knives.nblades = cutseqptr->numberofcuts;
    
    // Build displacement offsets for the rearrange
    makeoffsetsfor3or4cuts (&knives, diff);
    
    // Classify and modify each crum between the cuts
    for (ptr = (typecuc*)findleftson(father); ptr; 
         ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
        
        i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
        
        switch (i) {
          case -1:
            gerror ("rearrangend can't classify crum\n");
          case 0:  case 4: /* these never move */
            break;
          case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
            // ↓↓↓ THE ONLY MODIFICATION ↓↓↓
            tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
            ivemodified((typecorecrum*)ptr);       
            break;
          ...
        }
    }
    ...
}
```

[**edit.c:125**]

### 4. What Gets Modified

Since `index == V`, line 125 expands to:

```c
tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V]);
```

This adds an offset `diff[i]` to **only the V-displacement**.

### 5. What Is NOT Modified

The following fields are **never touched** by `rearrangend`:

- ✓ `ptr->cdsp.dsas[I]` — **I-displacement remains unchanged**
- ✓ `ptr->cwid.dsas[I]` — **I-width remains unchanged**  
- ✓ `ptr->cwid.dsas[V]` — **V-width remains unchanged**

The only references to `cwid` in edit.c are for error dumping [**edit.c:216**, **edit.c:225**], never modification.

---

## Semantic Implication

This confirms the fundamental Xanadu property: **content identity (I-address) is invariant under rearrangement**. REARRANGE is purely a V-space operation that changes where content appears in the document view (V-position), while preserving what that content is (I-address).

The content's I-address specifies its position in the eternal permascroll. REARRANGE moves the V-space "window" through which we view that content, but the content itself remains anchored at its original I-address in the permanent address space.

---

## Confirmation via Behavioral Testing

To empirically verify this, the existing test scenario `scenario_pivot_preserves_identity` in `febe/scenarios/rearrange.py:254` retrieves vspansets before and after pivot. The golden test would show that the I-components of the vspanset entries remain constant while V-components change.

---

## Question 14 [gregory]

> When COPY transcludes content from document A to document B, does document B's POOM receive exactly the same I-addresses as document A's POOM for the copied span, or does any intermediate conversion alter or re-allocate the I-address values?

### Gregory's Answer

## KB Synthesis

# Answer: COPY Preserves Exact I-Addresses

When COPY transcludes content from document A to document B, **document B's POOM receives exactly the same I-addresses** as document A's POOM for the copied span. No intermediate conversion alters or re-allocates the I-address values. This is the fundamental mechanism that enables content identity tracking across documents.

## The Mechanism

The transclusion data flow is `[INT-SPORGL-TRANSCLUSION]`:

1. Source V-addresses → converted to I-addresses via document A's POOM
2. I-addresses → packaged into **sporgls** (which carry both I-addresses and provenance)
3. Sporgls → inserted into document B's POOM via `insertpm`
4. Result: Document B's POOM maps new V-addresses to the **same I-addresses** from document A

As stated in `[INT-SPORGL-TRANSCLUSION]`: *"Because the sporgl preserves the original I-address (not a new one), the destination document ends up referencing the same content identities as the source."*

## Evidence from State Transitions

**VCOPY postcondition** `[ST-VCOPY]`:
- Finding 0002: "vcopy shares existing identities, not copies content"  
- Finding 0018: "Vcopy (transclusion) preserves I-addresses from the source"
- Finding 0046: "COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones"

**Contrast with INSERT** `[ST-INSERT]`:
- INSERT always allocates fresh I-addresses from the granfilade
- Finding 0030: INSERT creates new I-addresses; existing I-addresses are never modified

**Provenance invariant** `[INV-IADDR-PROVENANCE]`:
- "Every I-address has exactly one native document — the document where INSERT first allocated it"
- "COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones"

## Transitive Identity Preservation

The exact I-address preservation enables transitive identity `[INV-TRANSITIVE-IDENTITY]`:

```
Document C: "ABCDEFGHIJ" (I-addresses α₁..α₁₀)
Document B: vcopy(all of C) → I-addresses α₁..α₁₀
Document A: vcopy("DEFGH" from B) → I-addresses α₄..α₈

compare_versions(A, C) → "DEFGH" shared (same I-addresses α₄..α₈)
```

If COPY had performed any I-address conversion or re-allocation, this transitive identity would break.

## DELETE vs COPY Asymmetry

The I-address immutability principle `[INV-DELETE-NOT-INVERSE]` confirms this:

- DELETE followed by INSERT produces **different I-addresses** (INSERT always allocates fresh)
- DELETE followed by COPY from a version **restores original I-addresses** (COPY references existing)

As stated: *"VCOPY shares existing I-addresses rather than allocating new ones... the only identity-preserving restoration is VCOPY from a document that still references the original I-addresses"*

## Summary

Document B receives **bit-for-bit identical I-addresses** from document A. The only thing that changes is the V-address mapping:
- Document A: `V_A(position_A) → I-address_α`  
- Document B: `V_B(position_B) → I-address_α`  ← **same α**

This exact I-address preservation is what makes transclusion, version comparison, and link discovery work across document boundaries.

## Code Exploration

Based on my code analysis, I can now provide a definitive answer. Let me trace through the complete data flow:

## Answer: I-addresses are preserved exactly during COPY

When COPY transcludes content from document A to document B, **document B's POOM receives exactly the same I-addresses as document A's POOM**. No intermediate conversion alters or re-allocates the I-address values.

### Evidence from Source Code

**1. V→I Conversion extracts original I-addresses** [do2.c:14-44, orglinks.c:397-453, context.c:176-212]

The conversion chain:
- `docopy` calls `specset2ispanset` [do1.c:54]
- `specset2ispanset` calls `vspanset2ispanset` [do2.c:36]
- `vspanset2ispanset` calls `permute` → `span2spanset` → `retrieverestricted` [orglinks.c:401, 415, 435]
- `retrieverestricted` retrieves contexts from document A's POOM [retrie.c:55-84]
- `context2span` **extracts I-addresses directly from POOM contexts** [context.c:206-207]:

```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);  // Line 206
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width); // Line 207
```

These lines copy the I-coordinates from the POOM context into the ispanset without modification.

**2. Insertion preserves extracted I-addresses** [orglinks.c:74-133]

The `insertpm` function:
- Unpacks the ispanset via `unpacksporgl` [orglinks.c:101]
- `unpacksporgl` **moves I-addresses directly** from ispan to output [sporgl.c:181-182]:

```c
movetumbler (&((typeispan *)sporglptr)->stream, streamptr);  // Line 181
movetumbler (&((typeispan *)sporglptr)->width, widthptr);    // Line 182
```

- Back in `insertpm`, these values are **inserted without modification** [orglinks.c:105, 109]:

```c
movetumbler (&lstream, &crumorigin.dsas[I]);  // Line 105 - I-stream
movetumbler (&lwidth, &crumwidth.dsas[I]);    // Line 109 - I-width
movetumbler (vsaptr, &crumorigin.dsas[V]);    // Line 113 - NEW V-address
```

- Finally, `insertnd` inserts this crum into document B's POOM [orglinks.c:129]

**3. No allocation occurs**

Searching the entire code path:
- `movetumbler` is a copy operation (moves tumbler values)
- No calls to allocation functions for I-addresses
- No arithmetic modifications to I-address values
- The I-coordinates flow through as-is: POOM_A → context → ispan → POOM_B

### Semantic Interpretation

This behavior is **correct for transclusion semantics**. Both documents point to the same content in the granfilade, so they must have identical I-addresses. The POOM maps V-space (document positions) to I-space (content addresses):

- Document A: V-position 1.0 → I-address 3.1.5.100
- Document B: V-position 2.0 → **same** I-address 3.1.5.100

The content itself exists once in the granfilade at I-address 3.1.5.100. Both POOMs reference this single instance.

### Conclusion

**No intermediate conversion alters or re-allocates I-address values.** The I-addresses extracted from document A's POOM are inserted verbatim into document B's POOM. Only the V-addresses differ (as specified by the COPY operation's destination position).

---

## Question 15 [gregory]

> After CREATELINK allocates a link orgl I-address that advances the per-document allocation counter past the text range, can a subsequent text INSERT ever receive an I-address that falls within or before the link orgl's I-address range, or is the gap permanent?

### Gregory's Answer

## KB Synthesis

Looking at the relevant KB entries, **the gap is permanent**. Here's why:

## The Allocation Mechanism

From [INV-MONOTONIC] (Finding 0063):
> "The allocation function is `next_iaddr(granf) = max_iaddr(granf) + 1` regardless of entity type — text characters and link orgls compete for the same monotonic sequence."

And from [SS-ADDRESS-SPACE] (Finding 0061):
> "I-address allocation does not use a session-local counter. Each INSERT queries the granfilade tree via `findpreviousisagr` to find the highest existing I-address below an upper bound, then increments by 1."

The key insight from [INT-LINK-INSERT] (Finding 0063):
> "When the next INSERT calls `findpreviousisagr` to determine the allocation point, it finds the link orgl's I-address as the highest and allocates above it — creating a gap in the text I-address sequence."

## Why the Gap Cannot Be Filled

Three permanent properties prevent backfilling:

1. **No Reuse** — From [INV-NO-IADDR-REUSE] (Finding 0061):
   > "Deleted I-addresses are never reused. Since the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum, 'gaps' in V-space created by DELETE do not create 'gaps' in I-space."

2. **Append-Only Granfilade** — From [FC-GRANF-ON-DELETE] (Finding 0061):
   > "DELETE and REARRANGE are frame-condition-preserving with respect to the granfilade... Content inserted into the granfilade persists permanently at its I-address regardless of subsequent V-space operations."

3. **Strictly Monotonic** — From [INV-MONOTONIC] (Finding 0061):
   > "I-address allocation is strictly monotonically increasing and completely unaffected by DELETE or REARRANGE operations... No operation in the system can cause an I-address to be freed or reused."

## Observable Evidence

From [INT-LINK-INSERT] (Finding 0063), the gap is empirically observable:
> "The gap is observable through `compare_versions`: a document with INSERT 'ABC' + INSERT 'DEF' (no link) yields 1 shared span pair, while INSERT 'ABC' + CREATELINK + INSERT 'DEF' yields 2 shared span pairs. The two text regions have non-contiguous I-address ranges because the link orgl's I-address sits between them."

Concrete example from Finding 0063:
```
INSERT "ABC"     → I-addresses 1.1, 1.2, 1.3
CREATELINK       → link orgl at ~2.0 (advances granf maximum)
INSERT "DEF"     → I-addresses 2.1, 2.2, 2.3
                   (NOT 1.4, 1.5, 1.6 — the gap is permanent)
```

## Conclusion

The gap between text I-addresses before and after CREATELINK is **permanent and unfillable**. The link orgl I-address remains in the granfilade forever, and `findpreviousisagr` will always find it when computing the next allocation point. There is no mechanism to allocate "backwards" into gaps — allocation is a pure forward-only operation that always increments from the observed maximum.

## Code Exploration

Let me now compile my final answer based on the code analysis I've completed.

---

## Answer: The Gap is Permanent

After CREATELINK allocates a link orgl I-address that advances the per-document allocation counter past the text range, a subsequent text INSERT **cannot** receive an I-address that falls within or before the link orgl's I-address range. **The gap is permanent** because text and links occupy **separate I-address subspaces**.

### Code Evidence

#### I-Address Subspace Separation

Text and link atoms use different I-address ranges defined by `atomtype`:

**From `backend/xanadu.h`:**
```c
#define TEXTATOM  1
#define LINKATOM  2
```

**From `backend/granf2.c:158-181` (`findisatoinsertmolecule`):**

The allocation algorithm computes different upperbounds for text vs links:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

- **Text (TEXTATOM=1)**: `upperbound = docisa.0.2` (1+1=2)
- **Link (LINKATOM=2)**: `upperbound = docisa.0.3` (2+1=3)

Then `findpreviousisagr` searches for the highest existing I-address **below** the upperbound:

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

#### Why Text Cannot Fill Link Gaps

For **TEXTATOM** allocation (lines 168-169):
```c
else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
}
```

For **LINKATOM** allocation (lines 170-175):
```c
else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // docisa.0.2
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);         // docisa.0.2.1
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

**The critical insight:**
1. Text allocates in the `docisa.0.1.*` subspace
2. Links allocate in the `docisa.0.2.*` subspace (line 171)
3. When allocating text, `upperbound = docisa.0.2` **excludes** all link addresses
4. `findpreviousisagr(fullcrumptr, docisa.0.2, &lowerbound)` will **never** return a link I-address because all links are ≥ `docisa.0.2`

### Concrete Example

For document `1.1.0.1`:

1. **First INSERT** → Text allocated at `1.1.0.1.0.1.1`
2. **CREATELINK** → Link orgl allocated at `1.1.0.1.0.2.1`
3. **Second INSERT** → Text searches below `1.1.0.1.0.2`, finds `1.1.0.1.0.1.1`, allocates at `1.1.0.1.0.1.2`

The link at `1.1.0.1.0.2.1` is **invisible** to text allocation because the text upperbound (`1.1.0.1.0.2`) excludes it.

### Verification Path

From `backend/granf2.c:255-278` (`findpreviousisagr`), the function recursively walks the granfilade tree to find the highest I-address strictly less than the upperbound. Since links start at `docisa.0.2.*` and text searches below `docisa.0.2`, the two subspaces never overlap.

**Conclusion:** Text and links maintain permanent separation in I-space. The allocation counter conceptually has two independent streams—one for text (`docisa.0.1.*`) and one for links (`docisa.0.2.*`)—and they never fill each other's gaps.

---

## Question 16 [gregory]

> When INSERT shifts V-positions of existing POOM entries rightward via makegappm, does the shift apply uniformly to all entries at or beyond the insertion point within the same subspace, or can any entry be skipped or receive a different shift magnitude?

### Gregory's Answer

## KB Synthesis

# INSERT Shift Uniformity

The shift applies **uniformly** to all POOM entries within the shift region, with a clear partition into shifted and non-shifted zones. No entry receives a different shift magnitude based on its properties — the shift is determined solely by region membership.

## The Three-Region Partition

From **[ST-INSERT]** (Finding 0054), `insertcutsectionnd()` classifies each POOM crum into exactly three cases based on position relative to the two-blade knife:

- **Case 0** (before `blade[0]`): No shift
- **Case 1** (`blade[0] ≤ v < blade[1]`): Shift right by insertion width
- **Case 2** (at or beyond `blade[1]`): No shift

The knife structure from **[SS-TWO-BLADE-KNIFE]** (Finding 0054):
- `blade[0]` = insertion V-position
- `blade[1]` = `(N+1).1` where N is the subspace digit

## Uniform Shift Magnitude

All Case 1 entries receive **identical** shift magnitude. The code at `edit.c:162` (referenced in **[ST-INSERT]**, Finding 0052) applies:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])
```

The `width` parameter is the insertion width — a **single value** applied uniformly to every Case 1 entry. There is no per-entry variation, no conditional adjustment, and no type-dependent shift magnitude.

From **[FC-SUBSPACE]** (Finding 0054), the formal postcondition states:
```
∀ entry ∈ poom(doc) : blade[0] ≤ entry.vpos < blade[1] ⟹ 
  entry.vpos' = entry.vpos + insert_width
```

## What CAN Be Skipped

Entries in Case 0 and Case 2 are **deliberately skipped** — they receive zero shift:

- **Case 0 (prefix)**: Entries before the insertion point are unaffected
- **Case 2 (cross-subspace)**: Entries at or beyond the next subspace boundary are protected by the second blade

This skipping is intentional and enforces subspace isolation (**[FC-SUBSPACE]**, Finding 0054): INSERT at `1.x` cannot affect entries at `2.x`.

## No Other Variation

The shift operation has no dependency on:
- Entry type (text vs link orgls receive identical treatment within their subspace)
- Entry I-address (shift is V-space only)
- Entry width (the shift adds to displacement, not to width)
- Position within the shift region (all Case 1 entries treated identically)
- Crum boundary conditions (boundaries may prevent splitting via **[EC-BOUNDARY-INSERT-CLASSIFICATION]**, Finding 0062, but not shift variation)

## Summary

**Uniform**: All entries within `[blade[0], blade[1])` receive shift magnitude = insertion width.

**Skipped**: Entries outside this region (Cases 0 and 2) receive zero shift.

**No exceptions**: No entry within the shift region receives a different magnitude. The shift is determined by region membership alone, not by entry properties.

## Code Exploration

I have completed my investigation. Here is my full answer:

---

# Answer: Uniform Shift Within Subspace

## The Direct Answer

**Within the same subspace**, the shift applies **uniformly to ALL entries** at or beyond the insertion point. **No entries are skipped**, and **all receive identical shift magnitude** equal to the insertion width.

However, **entries in different subspaces are NOT shifted**. This subspace isolation is enforced by the second cut blade mechanism.

## Code Evidence

### The Shift Operation [insertnd.c:151-169]

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i=insertcutsectionnd(ptr,&fgrasp,&knives);
    switch (i) {
      case 0:
      case 2:
        break;  // No shift
      case 1:
        tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);  // Line 162
        ivemodified (ptr);
        break;
    }
}
```

**Key observation:** ALL case 1 entries receive the identical shift `&width->dsas[V]`. There is no variation.

### The Classification Logic [edit.c:207-233]

`insertcutsectionnd` classifies each entry using two blades:
- `blade[0]` = insertion point (e.g., 1.3)
- `blade[1]` = next subspace boundary (e.g., 2.1, calculated by `findaddressofsecondcutforinsert`)

```c
// Check blade[1] first
cmp = whereoncrum(ptr, offset, &knives->blades[1], V);
if (cmp <= ONMYLEFTBORDER) {
    return (2);  // Entry at/beyond blade[1] → NO SHIFT
}

// Check blade[0]
cmp = whereoncrum(ptr, offset, &knives->blades[0], V);
if (cmp <= ONMYLEFTBORDER) {
    return (1);  // Entry at/beyond blade[0], before blade[1] → SHIFT
}

return (0);  // Entry before blade[0] → NO SHIFT
```

**Result:**
- All entries in range `[insertion_point, next_subspace)` return case 1 → shifted uniformly
- All entries in other subspaces return case 2 → not shifted

### The Subspace Boundary [insertnd.c:174-183]

When inserting at 1.3, `findaddressofsecondcutforinsert(1.3)` returns **2.1** (confirmed by golden test comment at `golden/subspace/insert_text_check_both_link_positions.json:61`).

This ensures:
- All entries in subspace 1.x (text) at positions ≥ 1.3 → case 1 → **shifted**
- All entries in subspace 2.x (links) → case 2 → **NOT shifted**

## Empirical Proof

### Test 1: Uniform Shift Within Subspace

Golden test: `golden/subspace/displacement_tumbler_value.json`

**Setup:** "ABCDE" at positions 1.1-1.5
**Action:** INSERT "XYZ" at 1.3 (width = 0.3)
**Results:**
- Position 1.6 = 'C' (originally at 1.3, shifted by +0.3)
- Position 1.7 = 'D' (originally at 1.4, shifted by +0.3)

**Every character** at positions ≥ 1.3 was shifted by exactly 0.3. No skipping.

### Test 2: Subspace Isolation

Golden test: `golden/subspace/insert_text_check_both_link_positions.json`

**Setup:** Text in 1.x, link at 2.1
**Action:** INSERT at 1.3
**Results:**
- Text in 1.x shifted uniformly
- Link at 2.1 **NOT shifted** (still at 2.1, not 2.3)

Cross-subspace entries are isolated from shifts.

## whereoncrum Return Values [retrie.c:345-392]

| Value | Name | Meaning |
|-------|------|---------|
| -2 | TOMYLEFT | Blade left of entry |
| -1 | ONMYLEFTBORDER | Blade at entry's left border |
| 0 | THRUME | Blade cuts through entry |
| 1 | ONMYRIGHTBORDER | Blade at entry's right border |
| 2 | TOMYRIGHT | Blade right of entry |

When `cmp <= ONMYLEFTBORDER`, the entry is **at or beyond** the blade position.

## Conclusion

The shift is **completely uniform** within a subspace:
1. ✓ **Same magnitude:** All shifted entries receive exactly `width->dsas[V]`
2. ✓ **No skipping:** All entries with position ≥ insertion point are case 1
3. ✓ **Subspace isolation:** Blade[1] at next subspace prevents cross-subspace shifts

The second blade mechanism is the key insight: it creates a classification boundary that ensures all entries in the insertion subspace get shifted, while all entries in other subspaces do not.

---

## Question 17 [gregory]

> Does CREATENEWVERSION produce a new document whose POOM entries contain exactly the same I-addresses as the source document's text subspace, with no re-allocation, re-mapping, or transformation of those I-address values?

### Gregory's Answer

## KB Synthesis

Yes, CREATENEWVERSION produces a new document whose POOM entries contain exactly the same I-addresses as the source document's text subspace, with **no re-allocation, re-mapping, or transformation** of those I-address values.

## Evidence from the Knowledge Base

### No Content Allocation Occurs

[FC-GRANF-ON-VERSION] explicitly states: "CREATENEWVERSION does not modify the content portion of the granfilade. Like DELETE and REARRANGE, it is content-allocation-neutral." The postcondition is: `granf_content_after = granf_content_before` (no new content entries).

[ST-VERSION] provides the mechanism: "It does NOT allocate any new content I-addresses — no call to `findisatoinsertgr` for content. The copied SPANs reuse the source document's existing I-addresses."

### I-Address Preservation is Explicit

[ST-VERSION-CREATE] (Finding 0032) describes the implementation: "copy all content preserving I-addresses via `docopyinternal`". The operation performs: "(1) allocate a new orgl [document address] via `createorglingranf`, (2) retrieve the source document's full vspanset, (3) copy all content preserving I-addresses."

[INV-IADDR-PROVENANCE] establishes the general principle: "COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones." Since VERSION uses `docopyinternal` (a COPY operation), it inherits this property.

### Text Subspace Only

[ST-VERSION-CREATE] (Finding 0043) confirms the scope: "CREATENEWVERSION(d) copies only the text subspace (`1.x` V-positions) from the source document's POOM into the new version. The link subspace (`0.x` / internally `2.x`) is not copied."

### Observable Consequences

[ST-VERSION-CREATE] (Finding 0018) notes: "Version creation preserves content identity — the new version shares I-addresses with its parent for all inherited content. `compare_versions` between original and version returns the shared content."

[INT-VERSION-TRANSCLUSION] (Finding 0032) extends this: "The version shares the same I-addresses as the original, including any that originated from third-party documents" — preserving even transitively shared content identity.

## Conclusion

The version's POOM is constructed by creating V→I mappings that reference the **identical I-addresses** present in the source document's text subspace. The only new allocation is the version's document address itself. All content I-addresses are preserved exactly as they were in the source.

## Code Exploration

## Answer

**YES.** CREATENEWVERSION produces a new document whose POOM entries contain **exactly the same I-addresses** as the source document's text subspace, with **no re-allocation, re-mapping, or transformation** of those I-address values.

---

## Evidence from Code

### 1. CREATENEWVERSION Implementation

The operation copies I-addresses directly from the source document:

**[do1.c:260-299]** `docreatenewversion`:
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
  typehint hint;
  typevspan vspan;
  typevspec vspec;
  
  // 1. Allocate new document address
  makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
  createorglingranf(taskptr, granf, &hint, newisaptr);
  
  // 2. Retrieve source document's V-span
  doretrievedocvspanfoo (taskptr, isaptr, &vspan);
  
  // 3. Build vspec pointing to OLD document
  vspec.next = NULL;
  vspec.itemid = VSPECID;
  movetumbler(isaptr, &vspec.docisa);    // ← OLD document ISA
  vspec.vspanset = &vspan;
  
  // 4. Copy into new document
  addtoopen(newisaptr, user, TRUE, WRITEBERT);
  docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // ← Copies I-addresses
  logbertmodified(newisaptr, user);
  doclose(taskptr, newisaptr, user);
  
  return (TRUE);
}
```

**Key: Line 287** sets `vspec.docisa = isaptr` (the OLD document), so when we look up I-addresses, we use the OLD document's POOM.

### 2. V→I Conversion Using Source POOM

**[do1.c:66-82]** `docopyinternal`:
```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  
  // Convert V-spans to I-spans using the vspec.docisa (OLD document)
  if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
  
  // Get NEW document's POOM
  if (!findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;
  
  // Insert OLD document's I-addresses into NEW document's POOM
  if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
  
  // Record in spanfilade
  if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
  
  return TRUE;
}
```

**[do2.c:14-46]** `specset2ispanset`:
```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
  typeorgl docorgl;
  
  for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    if (((typeitemheader *)specset)->itemid == VSPECID) {
      // Look up I-addresses in the vspec's document (line 35: uses vspec.docisa)
      if (!(
        findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)
        && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
          return (FALSE);
      }
    }
  }
  return (TRUE);
}
```

**Line 35**: Uses `&((typevspec *)specset)->docisa` to find the orgl. This is the **OLD document's ISA** (set at do1.c:287), so we retrieve I-addresses from the **OLD document's POOM**.

**[orglinks.c:397-402]** `vspanset2ispanset`:
```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
  
  return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

This performs V→I lookup using the OLD document's orgl, retrieving the **existing I-addresses**.

### 3. I-Addresses Are Copied Unchanged

**[orglinks.c:75-134]** `insertpm`:
```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
  tumbler lstream, lwidth;
  type2dbottomcruminfo linfo;
  typewid crumorigin, crumwidth;
  
  for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    
    // Copy I-address from source UNCHANGED
    movetumbler (&lstream, &crumorigin.dsas[I]);   // ← Line 105
    movetumbler (&lwidth, &crumwidth.dsas[I]);     // ← Line 109
    
    // Set V-address in new document
    movetumbler (vsaptr, &crumorigin.dsas[V]);
    
    // Calculate V-width...
    shift = tumblerlength (vsaptr) - 1;
    inc = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
    
    // Insert into new document's POOM
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
  }
  return (TRUE);
}
```

**Lines 105 & 109**: The I-addresses (`lstream` and `lwidth`) are copied **directly** via `movetumbler`, with **no transformation or allocation**. The `movetumbler` function performs a simple memory copy of the tumbler structure.

### 4. No New Content Allocation

**Critically**, `docopyinternal` does **NOT** call `findisatoinsertgr` (the content allocation function). Compare with `doinsert`:

**[do1.c:87-123]** `doinsert`:
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
  typespanset ispanset;
  
  return (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // ← Allocates NEW I-addresses
       && docopy (taskptr, docisaptr, vsaptr, ispanset)                 // ← Then inserts them
  );
}
```

`doinsert` calls `inserttextingranf`, which allocates **new I-addresses** via `findisatoinsertgr`. In contrast, `docreatenewversion` → `docopyinternal` **skips this step entirely**, using only existing I-addresses from the source document.

---

## Test Evidence

From **Finding 0077: CREATENEWVERSION Does Not Advance Content Allocation**:

**Experiment**: INSERT "ABC" → CREATENEWVERSION → INSERT "XYZ"

**Result**:
```
After INSERT ABC: vspec = <VSpec in 1.1.0.1.0.1, at 1.1 for 0.3>
Created version: 1.1.0.1.0.1.2
After INSERT XYZ: vspec = <VSpec in 1.1.0.1.0.1, at 1.1 for 0.6>

Number of shared I-span pairs: 1
✓ CREATENEWVERSION did NOT advance content allocation counter
  XYZ I-addresses are contiguous with ABC
  Combined I-span: 1.1.0.1.0.1.3.0.1.1 + 0.6
```

The `compare_versions` result shows **1 shared span** covering all 6 characters. If CREATENEWVERSION had consumed I-addresses, we would see **2 separate spans** with a gap between them.

This proves that CREATENEWVERSION **did not allocate any I-addresses** — it only copied existing ones.

---

## Summary

CREATENEWVERSION creates a new document whose POOM contains:

1. **Same I-addresses** as the source document (via V→I lookup in source POOM)
2. **New V-addresses** starting at the specified position (typically 1.1)
3. **No new content allocation** — no calls to `findisatoinsertgr`

The new document's POOM entries map:
- **V-space**: New positions (1.1, 1.2, 1.3, ...)
- **I-space**: **Exact same I-addresses** as source (unchanged, copied via `movetumbler`)

This is the foundation of **content identity preservation** through versioning — both documents share the same underlying content in the granfilade via identical I-addresses.

---

## Question 18 [gregory]

> Once insertspanf creates a DOCISPAN entry in the spanfilade recording that document D contains I-address range R, is there any operation that removes or modifies that entry, or does it persist unconditionally even after DELETE removes that content from D's POOM?

### Gregory's Answer

## KB Synthesis

# DOCISPAN Persistence After DELETE

**Answer: DOCISPAN entries persist unconditionally. No operation removes or modifies them after creation.**

## Evidence from Knowledge Base

### Write-Only Spanfilade Architecture

[INV-SPANF-WRITE-ONLY] establishes the fundamental property:

> "The spanfilade is a write-only (append-only) index. Entries are added by `insertspanf` during COPY and INSERT operations, but **no deletion function exists anywhere** in the spanf codebase. Inspection of `spanf1.c` and `spanf2.c` reveals `insertspanf`, `findlinksfromtothreesp`, `retrieveendsetsfromspanf`, `finddocscontainingsp`, and `findnumoflinksfromtothreesp` — all insertion and query functions. **No `deletespanf`, `removespanf`, or any removal mechanism exists.**"

The invariant: `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)` — the spanfilade is **monotonically non-decreasing**.

### DELETE Operation Behavior

[ST-DELETE] confirms DELETE has no spanf effect:

> "DELETE (`dodeletevspan`) removes the V-to-I mapping from the document's POOM via `deletevspanpm` → `deletend`, but does **NOT remove the corresponding spanfilade entry** created by the original COPY/INSERT. The spanfilade continues to assert that the document contains I-addresses that the document's POOM no longer maps. Specifically, `deletevspanpm` calls only `deletend` on the document's orgl in granf and `logbertmodified` — **there is no call to any spanf function**."

Code evidence from Finding 0057:
```c
// COPY path (both layers updated):
backend/do1.c:45-65 — insertpm (granf) + insertspanf (spanf)

// DELETE path (only granf updated):
backend/do1.c:162-171 — deletevspanpm (granf only)
```

### Resulting Divergence

[INT-DELETE-SPANF-DIVERGENCE] describes the consequence:

> "DELETE causes the POOM (granf) and spanfilade (spanf) to diverge. Before DELETE, both layers agree: the POOM says the document maps V-addresses to certain I-addresses, and the spanfilade says the document contains those I-addresses. After DELETE, the POOM no longer contains the mapping, but the spanfilade still claims the document contains those I-addresses. This divergence is **permanent** — no mechanism exists to reconcile the two layers."

The formal invariant becomes asymmetric:
- **Forward direction holds**: `∀ D, i : (∃ v : poom.D(v) = i) ⟹ i ∈ spanf_index(D)` (every live reference is indexed)
- **Reverse does NOT hold**: `find_documents(i)` may include documents where `¬∃ v : poom.D(v) = i` (stale entries)

### Observable Consequences

[EC-STALE-SPANF-REFERENCE] demonstrates the practical impact:

> "After DELETE removes transcluded content, FIND_DOCUMENTS still returns the document as containing those I-addresses. The document appears in the result because the spanfilade entry persists, but attempting to convert the I-addresses to V-addresses in that document yields empty — the POOM has no mapping. This creates a 'ghost reference' in the spanfilade."

**Concrete example:**
```
Setup:
  Document D has content at I-addresses α₁..α₅
  INSERT creates DOCISPAN: spanf[α₁..α₅] → {D}

After DELETE from D:
  POOM(D): ∅ (V-to-I mapping removed)
  spanf[α₁..α₅]: {D} (UNCHANGED — stale reference persists)
  
  find_documents(α₁..α₅) → {D}  (D still returned)
  I-to-V(α₁, D) → ∅             (no V-position in D)
```

## Architectural Note

[FC-CONTENT-SPANF-ISOLATION] clarifies that while INSERT writes to spanf DOCISPAN, this is a **one-way operation**:

> "INSERT writes to both granf (new content) and spanf (DOCISPAN index)." But no operation performs the inverse.

The spanfilade functions as a **historical journal** of all content placements that have ever occurred, not a current-state index. This is by design — the permanent layer accumulates references monotonically [INV-IADDRESS-PERMANENT].

**Summary**: Once `insertspanf` creates a DOCISPAN entry, it persists forever. DELETE, REARRANGE, and all other operations leave the spanfilade unchanged.

## Code Exploration

## Answer

**No. Once `insertspanf` creates a DOCISPAN entry, there is no operation that removes or modifies it. These entries persist unconditionally, even after DELETE removes that content from the document's POOM.**

---

## Evidence from Source Code

### 1. How DOCISPAN Entries Are Created

From `backend/do1.c:45-65` (the `docopy` function):

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  bool specset2ispanset(), findorgl(), acceptablevsa(), insertpm(), insertspanf();

  return (
     specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
  && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && acceptablevsa (vsaptr, docorgl)
  && asserttreeisok(docorgl)

  /* the meat of docopy: */
  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)

  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
  && asserttreeisok(docorgl)
  /*      &&  ht stuff */ );
}
```

**Line 62** calls `insertspanf`, which creates the DOCISPAN entry recording that document D contains I-address range R.

From `backend/spanf1.c:15-54` (the `insertspanf` implementation):

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
{
  typedsp crumorigin;
  typewid crumwidth;
  tumbler lstream, lwidth;
  type2dbottomcruminfo linfo;

  prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
  tumblerclear (&crumwidth.dsas[ORGLRANGE]);
  clear (&linfo, sizeof(linfo));
  for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
      movetumbler (&((typeispan *)sporglset)->stream, &lstream);
      movetumbler (&((typeispan *)sporglset)->width, &lwidth);
      movetumbler (isaptr,&linfo.homedoc);
      // ... [lines 30-43 handle SPORGLID and TEXTID]
      movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
      movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
      insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    }
  }
  return (TRUE);
}
```

**Line 51** calls `insertnd` to add the 2D entry to the spanfilade enfilade, mapping `(I-address range, document ISA)` → metadata. This entry records "document D contains I-addresses R."

### 2. What DELETE Does

From `backend/do1.c:158-167` (the `dodeletevspan` function):

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  /*&& TRUE*/ /* ht stuff */ );
}
```

DELETE calls `deletevspanpm` — **no spanf operation**.

From `backend/orglinks.c:145-152` (the `deletevspanpm` implementation):

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

**Key observation**: 
- **Line 149**: Calls `deletend` on the document's POOM (in granf) to remove the V→I mapping
- **Line 150**: Logs the modification
- **No call to remove the spanfilade entry**

### 3. No Deletion Function Exists for Spanf

Inspection of all spanf source files reveals:

**Functions that exist in `backend/spanf1.c` and `backend/spanf2.c`:**
- `insertspanf` — adds DOCISPAN entries [spanf1.c:15]
- `insertendsetsinspanf` — adds link endset entries [do2.c:116]
- `findlinksfromtothreesp` — queries for links [spanf1.c:56]
- `finddocscontainingsp` — finds documents containing I-addresses [spanf1.c:151]
- `retrieveendsetsfromspanf` — retrieves link endsets [spanf1.c:190]

**Functions that DO NOT exist:**
- ❌ `deletespanf` — no such function
- ❌ `removespanf` — no such function  
- ❌ Any cleanup or removal mechanism

Verification via grep:
```bash
$ grep -r "deletespanf\|removespanf" backend/
# No matches in C source files
```

### 4. Architectural Confirmation

The spanfilade is **write-only** from the perspective of individual entries:

| Operation | Granf Update | Spanf Update |
|-----------|--------------|--------------|
| **INSERT** (doinsert) | insertpm → insertnd (add V→I) | insertspanf → insertnd (add I→doc) |
| **COPY** (docopy) | insertpm → insertnd (add V→I) | insertspanf → insertnd (add I→doc) |
| **DELETE** (dodeletevspan) | deletevspanpm → deletend (remove V→I) | ❌ **No cleanup** |
| **REARRANGE** (dorearrange) | rearrangepm → rearrangend (shift V-positions) | ❌ **No modification** |

From `backend/edit.c:31-76`, the `deletend` function operates on SPAN and POOM enfilades but is never called on the spanf global:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
  // ... [cuts and removes entries from the enfilade]
  // This modifies the document's POOM (fullcrumptr = docorgl)
  // Never called with fullcrumptr = spanf
}
```

### 5. Consequence: Stale References Persist

**Example execution trace:**

1. **Document A copies content from Document B**:
   - `docopy` → `insertpm` (adds V→I mapping to A's POOM in granf)
   - `docopy` → `insertspanf` (adds entry to spanf: "A contains I-addresses X")

2. **Document A deletes that content**:
   - `dodeletevspan` → `deletevspanpm` → `deletend` (removes V→I from A's POOM)
   - **No spanf modification** — the entry "A contains I-addresses X" remains

3. **User queries for documents containing I-addresses X**:
   - `finddocscontainingsp` queries spanf → returns both B and A
   - Attempting I→V conversion for A fails (POOM has no mapping)
   - Finding 0048 documents this filtering behavior

---

## Conclusion

**DOCISPAN entries in the spanfilade are permanent once created.** They record historical fact ("document D once contained I-addresses R") rather than current state ("document D currently contains I-addresses R"). 

This design makes the spanfilade a **historical journal** rather than a **current index**. The lack of cleanup is consistent with the broader architecture:
- Finding 0057 documents this behavior in detail
- Finding 0024 shows link deletion has the same pattern
- Finding 0048 shows how stale entries are filtered during I→V conversion

The backend provides no mechanism to remove or modify spanfilade entries. **The answer is definitively no.**

---

## Question 19 [gregory]

> If a link is created with endsets referencing specific I-address spans, and those spans are later deleted from every document's POOM, do the link's stored endset I-addresses in the granfilade remain unchanged such that re-transcluding the same I-addresses makes the link discoverable again?

### Gregory's Answer

## KB Synthesis

**YES** — the link's endset I-addresses remain unchanged in the granfilade, and re-transcluding those same I-addresses makes the link discoverable again.

## Mechanism

When content is deleted:

1. **Link orgl persists unchanged** [SS-THREE-LAYER-MODEL], [INV-IADDR-IMMUTABILITY]
   - The link structure in I-space contains endset I-addresses
   - DELETE cannot modify I-space entries [FC-DELETE-CROSS-DOC]
   - Link endsets are stored as I-addresses in the permanent layer [SS-LINK-ENDPOINT]

2. **Spanf index retains link mappings** [INV-SPANF-WRITE-ONLY], [INT-SPORGL-LINK-INDEX]
   - Link-to-I-address mappings in spanf are never removed
   - DELETE only affects POOM, not spanf [INT-DELETE-SPANF-DIVERGENCE]

3. **Link becomes "ghost"** [EC-GHOST-LINK]
   - FOLLOWLINK succeeds but returns empty (I-addresses have no V-positions)
   - find_links returns nothing (no I-address intersection with any document)
   - The link exists but is unresolvable

When you re-transclude via COPY:

4. **COPY restores I-address identity** [ST-VCOPY], [ST-COPY]
   - COPY shares the original I-addresses (doesn't allocate new ones)
   - New POOM mappings created: V-positions → original I-addresses

5. **Link becomes discoverable again** [INT-LINK-TRANSCLUSION], [ST-FIND-LINKS]
   - find_links searches spanf by I-address intersection
   - Restored POOM mappings provide V-positions for the link's I-addresses
   - Link discovery works through shared content identity

## Critical Distinction

**Re-transclude (COPY)** ✓
```
DELETE → COPY same I-addresses → link discoverable
```

**Delete + Insert** ✗
```
DELETE → INSERT new text → NEW I-addresses allocated [INV-DELETE-NOT-INVERSE]
Link remains orphaned (references old I-addresses that no longer exist in any POOM)
```

[INV-DELETE-NOT-INVERSE] establishes that DELETE+INSERT is not identity-preserving. Only COPY ([ST-COPY]) shares existing I-addresses, which is what reconstitutes the link.

This is the reconstitution mechanism mentioned in [EC-GHOST-LINK]: "reconstitution is always possible since I-addresses are permanent (P0)."

## Code Exploration

Based on my analysis of the source code, I can now answer your question definitively:

---

# Answer: Yes, Link Endsets Persist via I-Addresses

**The link's stored endset I-addresses in the granfilade remain unchanged when content is deleted, and re-transcluding the same I-addresses makes the link discoverable again.**

## Evidence from Source Code

### 1. Link Creation Stores I-Addresses

**[do1.c:195-221]** `docreatelink`:
- Line 214: Converts V-specs to sporglsets via `specset2sporglset`
- Line 218: Inserts endsets into link's orgl via `insertendsetsinorgl`  
- Line 219: Inserts endsets into spanfilade via `insertendsetsinspanf`

**[sporgl.c:35-65]** `vspanset2sporglset`:
- Line 48: Converts V-spans to I-spans via `vspanset2ispanset`
- Lines 50-58: Creates sporgls containing:
  - Line 53: `sporgladdress` = document ISA
  - Line 54: `sporglorigin` = **I-address stream**
  - Line 55: `sporglwidth` = **I-address width**

**Key insight:** Endsets are converted from V-addresses to I-addresses during link creation and stored as I-addresses in both the link's orgl and the spanfilade.

### 2. Deletion Only Affects POOM, Not Granfilade

**[orglinks.c:145-150]** `deletevspanpm`:
- Line 149: Calls `deletend` on document's orgl with V-dimension
- This removes the V→I mapping from the POOM tree only

**[edit.c:31-76]** `deletend`:
- Operates on a single enfilade tree (the POOM)
- Does NOT touch the granfilade where I-addresses are allocated
- Does NOT touch the spanfilade where link endsets are indexed

**When content is deleted:**
1. The V→I mapping is removed from the document's POOM
2. The I-addresses remain allocated in the granfilade
3. The link's endsets in the spanfilade still reference those I-addresses

### 3. Link Discovery Uses I-Addresses

**[spanf1.c:56-103]** `findlinksfromtothreesp`:
- Line 71-75: Converts search V-specs to sporglsets (I-addresses)
- Line 77: Searches spanfilade for links via `sporglset2linkset`

**[sporgl.c:239-269]** `sporglset2linksetinrange`:
- Line 259: Calls `retrieverestricted` on spanfilade with I-addresses
- Searches for links whose endsets contain the specified I-addresses
- Returns matching link ISAs

**Link lookup works by:**
1. Converting your V-spec to I-addresses
2. Searching the spanfilade for links whose endsets contain those I-addresses
3. The spanfilade lookup uses I-addresses directly, not V-addresses

### 4. Re-Transclusion Restores V→I Mapping

**[do1.c:45-65]** `docopy`:
- Line 60: Calls `insertpm` to insert I-spans into POOM at new V-address
- Line 62: Updates spanfilade with new mapping

When you re-transclude the same I-addresses:
1. `insertpm` creates a new V→I mapping in the POOM
2. The I-addresses are the same as before
3. Link search converts your new V-address to the same I-addresses
4. The spanfilade still has the link endsets referencing those I-addresses
5. **The link is discoverable again**

## Semantic Implications

This behavior reveals a fundamental design principle:

**Links connect I-addresses (content identity), not V-addresses (content location).**

- **Granfilade**: Stores the permanent I-address allocations (content atoms)
- **POOM**: Stores the current V→I mappings (where content appears in a document)
- **Spanfilade**: Indexes links by I-addresses (content identity), not V-addresses

When you delete content from a POOM, you're only removing the "view" of the content at that V-location. The content's identity (I-address) persists in the granfilade. Links reference that identity, so they persist regardless of whether any document currently views that content.

---

I can write a golden test to verify this empirically if you'd like. The test would:
1. Create a link referencing specific I-addresses
2. Delete the content from all documents
3. Re-transclude the same I-addresses to a new V-location
4. Verify the link is discoverable again

Would you like me to create and run this test?

---

## Question 20 [gregory]

> When DELETE shifts surviving POOM entries leftward via strongsub and the exponent guard fires for cross-subspace entries, is the entry returned completely unchanged — same V-displacement, same V-width, same I-displacement, same I-width — or does any component get modified even when the V-displacement is preserved?

### Gregory's Answer

## KB Synthesis

Looking at the DELETE operation's interaction with cross-subspace entries when the strongsub exponent guard fires, the answer is: **YES, the entry is completely unchanged** — all four components (V-displacement, V-width, I-displacement, I-width) remain identical.

## Case 2 Subtraction (Initial Processing)

In `deletend()` at `edit.c:63`, Case 2 handles entries after the deletion range:

```c
tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
```

This operation touches **ONLY the V-displacement field** (`cdsp.dsas[V]`). The other three fields are never accessed in Case 2:
- `cdsp.dsas[I]` (I-displacement) — not touched
- `cwid.dsas[V]` (V-width) — not touched  
- `cwid.dsas[I]` (I-width) — not touched

When the exponent guard fires (width.exp < entry.vpos.exp), `strongsub` at `tumble.c:544` executes:

```c
movetumbler(aptr, cptr);  // Copy minuend unchanged to result
return(0);
```

The V-displacement remains unchanged: `2.1 - 0.3 = 2.1` when `0.3.exp (-1) < 2.1.exp (0)` [SS-TUMBLER, ST-DELETE].

## Setwispupwards Adjustment (Post-Processing)

After processing all crums, `deletend()` calls `setwispupwards(father, taskptr)` which invokes `setwispnd` to maintain relative addressing in 2D enfilades [SS-ENFILADE-TREE].

The `setwispnd` algorithm (wisp.c:171-228):
1. Find `mindsp` = minimum displacement across all children
2. Add `mindsp` to parent's `cdsp`
3. Subtract `mindsp` from each child's `cdsp`

For our scenario with mixed-exponent children:
- Text entries: `1.1, 1.2` (exp=-1)
- Link entry: `2.1` (exp=0)

Comparison uses [INV-TUMBLER-TOTAL-ORDER]: since exp=-1 < exp=0, we have `1.1 < 2.1`, so `mindsp = 1.1`.

The adjustment attempts: `child.cdsp = tumblersub(2.1, 1.1)`

But this is also a cross-exponent subtraction! The strongsub exponent guard fires **again**:
- Check: `1.1.exp (-1) < 2.1.exp (0)` → TRUE
- Returns `2.1` unchanged

**Result: The link entry's V-displacement remains `2.1` even after setwispnd adjustment.**

## Conclusion

The exponent guard in strongsub provides **double protection** [FC-SUBSPACE]:
1. During Case 2 processing — prevents the deletion width from shifting cross-subspace entries
2. During setwispnd adjustment — prevents relative-addressing recalculation from affecting cross-subspace entries

Since DELETE Case 2 **never touches** the other three fields (V-width, I-displacement, I-width), and the only field it attempts to modify (V-displacement) is protected by the exponent guard, the cross-subspace entry emerges from DELETE with **all four components unchanged** [ST-DELETE, SS-ENFILADE-TREE].

## Code Exploration

## Answer

**Yes, the entry is returned completely unchanged** — same V-displacement, same V-width, same I-displacement, same I-width. When the exponent guard fires, no component of the POOM entry is modified.

## Code Path Analysis

### 1. DELETE Shift Operation [backend/edit.c:63]

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

**Critical observation:** Only `cdsp.dsas[index]` (the displacement in dimension `index`) is modified. The code never touches:
- `cwid.dsas[V]` (V-width)
- `cdsp.dsas[I]` (I-displacement)  
- `cwid.dsas[I]` (I-width)

### 2. The Exponent Guard [backend/tumble.c:544-547]

The `tumblersub` call chains through `tumbleradd` to `strongsub`, which implements the exponent guard:

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    tumbler answer;
    register INT i, j;
    
    tumblerclear(&answer);
    if (tumblereq (aptr, bptr)) {
        movetumbler (&answer, cptr);
        return(0);
    }
    if (bptr->exp < aptr->exp) {          // EXPONENT GUARD
        movetumbler(aptr,cptr);           // Return aptr UNCHANGED
        return(0);
    }
    // ... rest of subtraction logic only executes if guard doesn't fire
```

When `bptr->exp < aptr->exp`, the function returns `aptr` completely unchanged at lines 545-546.

### 3. Complete Preservation

When the exponent guard fires:

1. **V-displacement** → Preserved by strongsub returning `aptr` unchanged
2. **V-width** → Never touched by `edit.c:63` (only modifies displacement)
3. **I-displacement** → Never touched by `edit.c:63` (only modifies V dimension)
4. **I-width** → Never touched by `edit.c:63` (only modifies V dimension)

## Example: Cross-Subspace Immunity

Entry at V-displacement = **1.5** (link subspace):
- exp = 0, mantissa = [1, 5]

DELETE removes width = **0.01** (text subspace):
- exp = -2, mantissa = [1]

Since `0.01.exp (-2) < 1.5.exp (0)`, the guard fires → **entire entry unchanged**.

## Semantic Meaning

The exponent guard creates a precision boundary: when the deleted region is multiple orders of magnitude smaller than the entry's position, the entry is completely unaffected. This makes cross-subspace entries (like links at V ≥ 1.0) immune to small text deletions (V < 1.0).

**Citations:**
- [backend/edit.c:63] - DELETE shift only modifies displacement
- [backend/tumble.c:544-547] - Exponent guard returns unchanged value
- [backend/tumble.c:406-440] - tumblersub chains to strongsub
- [backend/tumble.c:365-404] - tumbleradd calls strongsub when signs differ
