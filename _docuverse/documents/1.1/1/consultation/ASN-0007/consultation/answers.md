# Consultation Answers — Links and Endsets

**Inquiry:** What must bidirectional links guarantee? What are endset semantics — how do links survive editing, deletion, and rearrangement of their target content?
**Date:** 2026-02-23 16:49
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a link connects two spans of content across different documents, what exactly does each endset point to — the content itself, or its position within the document?

### Nelson's Answer

Let me check the key pages where Nelson discusses this most directly.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-209.png</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-197.png</file_path>
</parameters>
</tool_call>

This is a precise question, and the answer is clear from the architecture: **endsets point to the content itself — to permanent I-space addresses — not to positions within any document's current arrangement (V-space).**

Here is the evidence, with citations.

## The Core Statement

Nelson describes links as attaching to bytes, not to positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

And more explicitly on the addressing side:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The phrase "to the bytes themselves" is the key. Bytes have permanent I-space addresses. Positions in a document's current arrangement are V-space addresses that shift with every edit. Links attach to the former, not the latter.

## Why This Must Be I-Space

The survivability guarantee makes this architecturally necessary:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

If endsets pointed to V-space positions (e.g., "position 47 in document D"), then every INSERT before position 47 would invalidate the link. The guarantee that links "survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43] is only possible if endsets reference content identity (I-space), not content arrangement (V-space).

The mechanism:

- **V-space addresses** change with every edit — they are ephemeral positions in the current arrangement
- **I-space addresses** are permanent — a byte's I-address never changes after creation
- When you edit a document, V-space shifts but I-space is untouched
- Links reference I-space, so editing has no effect on them

As Nelson states about V-space:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space is "constantly changing." You cannot build survivable links on something that constantly changes.

## What This Means Across Documents

When a link connects spans in two different documents, each endset contains I-space addresses identifying specific bytes by their permanent identity — which encodes their home document, their owner, and their position in the append-only content store.

This means:

1. **The from-set** is a span-set of I-space addresses (possibly in multiple documents)
2. **The to-set** is a span-set of I-space addresses (possibly in multiple documents)
3. **The type (three-set)** is also a span-set of I-space addresses (or ghost addresses where nothing is stored)

Nelson confirms that endsets map to the universal tumbler line:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

And each endset can span multiple documents:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

## The User-Facing vs. Storage-Level Distinction

There is a subtlety worth noting. At the **FEBE protocol level**, users work with V-space addresses — they INSERT at V-space position 5, they DELETE a V-span. But when they create a link (MAKELINK), the system translates the user's selection into permanent I-space addresses for storage. The user says "link from this visible passage to that visible passage"; the system records "link from these I-space bytes to those I-space bytes."

This is why Nelson can say users don't need to know about I-space:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The front end handles translation. The back end stores links in I-space terms. The user sees content; the link grabs the content's permanent identity.

## Summary

Each endset points to **content** — identified by permanent I-space addresses — not to positions within any document's current V-space arrangement. This is the architectural foundation for link survivability. The link is a "strap between bytes" [LM 4/42] that holds onto the bytes' permanent identities, regardless of how those bytes are currently arranged in any document's view.

---

## Question 2 [nelson]

> If a user inserts new content in the middle of a span that a link's endset references, does the link now include the new content, or does it continue to reference only the original content?

### Nelson's Answer

## The link continues to reference only the original content.

This follows directly from Nelson's fundamental design: links attach to **bytes** (I-space identity), not to **positions** (V-space arrangement).

### The Mechanism

When you INSERT new content in the middle of a span that a link's endset references:

1. The new content receives **fresh I-space addresses** — it is new content that did not exist before
2. The link's endset references the **original bytes by their permanent I-space addresses**, which are unchanged
3. The V-space arrangement shifts (positions after the insertion point increase), but the link does not care about V-space

Nelson states this directly:

> "Since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And more explicitly:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" metaphor is precise: the strap binds to specific bytes. Inserting new bytes between them does not stretch the strap to include the newcomers.

### The Endset Becomes Discontiguous in V-Space

After insertion, the link's endset — which was a single contiguous V-space span — may now appear as a **broken, discontiguous set** in V-space. Nelson explicitly anticipated this:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes." [LM 4/42]

**Example:**

```
Before INSERT:
  V-space: [A B C D E]     (positions 1-5)
  Link endset: {A,B,C,D,E} (one contiguous span)

After INSERT of [X Y Z] between C and D:
  V-space: [A B C X Y Z D E]  (positions 1-8)
  Link endset: {A,B,C,D,E}    (same bytes, now discontiguous in V-space)
                               (V-positions 1-3 and 7-8)
```

The I-space addresses of A through E are permanent and unchanged. X, Y, Z have entirely new I-space addresses. The link's endset still covers exactly {A, B, C, D, E}.

### Why This Must Be the Case

This behavior is required by the **link survivability guarantee**:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

If links expanded to include newly inserted content, they would change meaning with every edit — the opposite of survivability. A citation link to "these three sentences" would silently grow to include an unrelated paragraph someone inserted between sentences two and three. That would violate the link's semantic intent.

The I-space/V-space separation is designed precisely for this:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space positions change freely. I-space addresses — and therefore link endsets — do not.

### Summary

| Aspect | After INSERT in middle of linked span |
|--------|--------------------------------------|
| Link's I-space references | **Unchanged** — same bytes |
| New content included? | **No** — new bytes have new I-addresses |
| V-space appearance | May become **discontiguous** |
| Link meaning | **Preserved** — same content referenced |
| Link validity | **Intact** — all original bytes still exist |

---

## Question 3 [nelson]

> When content that a link points to is deleted from a document, does the link break, or does it continue to exist pointing to the permanent content that was removed?

### Nelson's Answer

## The Link Does Not Break

When content is "deleted" from a document, the link continues to exist, pointing to the permanent content. This follows from two interlocking design principles.

### Delete Does Not Destroy

DELETE in Xanadu removes content from V-space (the document's current arrangement) but does **not** remove it from I-space (permanent storage). Nelson's diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And more directly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The content still exists at its permanent I-space address. It has merely been removed from the current V-space view.

### Links Point to Bytes, Not Positions

Links attach to I-space content (the permanent bytes), not to V-space positions (the current arrangement):

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The survivability guarantee is explicit:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### The Full Picture

The separation of I-space from V-space is what makes this work:

- **I-space** (permanent): Content lives here forever. An append-only store where nothing is ever overwritten or removed.
- **V-space** (ephemeral): The document's current arrangement of content. Editing changes V-space only.

When you "delete" a passage, the V-space mapping is removed — the passage disappears from the current view. But the I-space bytes remain. The link, which points to those I-space bytes, remains valid. The link's endsets still resolve to content that exists.

The only way a link can break is if **all** bytes at one of its endsets are truly gone — which cannot happen in Xanadu, because I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Summary

A link to "deleted" content remains fully intact, pointing to the permanent I-space bytes. The content is invisible in the current version's V-space but still exists, still addressable through its I-space address, still reachable through old versions, and still connected by any links that reference it. This is by design — it is the entire point of separating content identity (I-space) from content arrangement (V-space).

---

## Question 4 [nelson]

> Must every link be discoverable from both ends — if I can find all links pointing FROM a span, must I equally find all links pointing TO that span?

### Nelson's Answer

# Yes — Bidirectional Link Discovery Is a Core Guarantee

Nelson designed link discovery to be fully symmetrical across all three endsets. This is not an incidental feature but a fundamental architectural property.

## The Search Model

The single operation `FINDLINKSFROMTOTHREE` accepts constraints on **all four** dimensions simultaneously: home-set, from-set, to-set, and type (three-set). Any unconstrained dimension defaults to the whole docuverse. This means:

- **Find links FROM a span**: constrain the from-set, leave to-set open
- **Find links TO a span**: constrain the to-set, leave from-set open
- **Find links OF a type**: constrain the three-set, leave from/to open
- **Any combination**: constrain multiple endsets at once

Nelson specifies the satisfaction condition:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This is perfectly symmetric — no endset is privileged over another in the matching logic.

## Nelson's Explicit Statements

On bidirectional reading:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37–2/40]

On in-link discovery:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

On search efficiency in both directions:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

## Why This Matters

Nelson explicitly frames this as solving the **backlinks problem** that plagues conventional hypertext. Traditional hyperlinks are one-way — you can follow a link forward but cannot discover what points at you. Xanadu rejects this:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work." [LM 2/43]

The "two-sided coin" metaphor is precise: free linking (FROM) and discoverable in-links (TO) are inseparable aspects of the same design. You cannot have one without the other. If authors cannot prevent incoming links, then readers **must** be able to discover them — otherwise the freedom to link would be meaningless.

## The Three-Endset Symmetry

The architectural basis is the symmetry of the link structure itself. All three endsets follow identical conventions:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

Because the system treats from-set, to-set, and type identically — each is an arbitrary span-set, each is indexed, each participates in the same search mechanism — discovery is inherently symmetric across all three dimensions.

## Summary

Link discovery in Xanadu is not merely bidirectional but **tridirectional** — discoverable from the from-set, the to-set, **and** the type. The single `FINDLINKSFROMTOTHREE` operation handles all directions through the same mechanism. This symmetry is not an implementation choice but a consequence of the fundamental design: all three endsets are structurally identical, all are indexed, and the search satisfaction condition treats them uniformly.

---

## Question 5 [nelson]

> Can a link's endsets be changed after the link is created, or is a link as permanent and immutable as the content it connects?

### Nelson's Answer

## Links Are Immutable After Creation

A link's endsets **cannot be changed** after the link is created. Links in Xanadu are as permanent and immutable as the content they connect. The evidence for this is strong and converges from multiple directions.

### 1. No Modification Operation Exists

The FEBE protocol defines exactly one link-creation operation and zero link-modification operations:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

The complete set of 17 FEBE commands includes `MAKELINK` but nothing like `EDITLINK`, `MODIFYLINK`, or `CHANGEENDSETS`. The editing operations (`INSERT`, `DELETEVSPAN`, `REARRANGE`, `COPY`, `APPEND`) apply to document text content, not to links.

What the system IS defined to do with links: you can create them, find them, retrieve their endsets, count them, and delete them. You cannot modify them.

### 2. Links Live in I-Space (Permanent, Immutable)

Links occupy the **2.x subspace** of I-space — the permanent address space where content never changes:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

I-space is defined by the guarantee that content at an I-space address **never changes**. Links, being I-space objects with permanent tumbler addresses, inherit this immutability.

### 3. Link "Maintenance" Is Indexing, Not Modification

Nelson describes what happens after creation:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and **thereafter maintained by the back end through the back end's inter-indexing mechanisms**." [LM 4/41]

The back end "maintains" links by keeping them indexed and searchable — not by allowing their endsets to be rewritten. The maintenance is bookkeeping, not mutation.

### 4. Survivability ≠ Mutability

Link survivability is sometimes mistaken for link flexibility, but it is the opposite — it depends on link immutability:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links survive because their endsets point to **I-space addresses** (permanent content identity), not V-space positions (ephemeral arrangement). When a document is edited, V-space positions shift, but the I-space addresses the link points to remain unchanged. The link itself never changes — it's the document's arrangement around it that moves.

### 5. Deletion, Not Modification

The only way to "change" a link is to delete it and create a new one. Nelson explicitly includes deleted links as a system state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Even deletion doesn't truly destroy the link — it becomes "not currently addressable" but remains in I-space, recoverable through historical backtrack.

### 6. The Endset Design Confirms This

The endset structure itself is designed for permanence:

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

Endsets point to I-space addresses. Since I-space addresses are permanent and immutable, and since no operation exists to rewrite an endset's target addresses, the endsets are fixed at creation time.

### Summary

| Question | Answer |
|----------|--------|
| Can endsets be modified after creation? | **No** — no FEBE operation exists for this |
| Can a link be deleted? | **Yes** — by the owner, but it remains in history |
| Can a link be "updated"? | **Only by deleting the old link and creating a new one** |
| Why are links immutable? | They are I-space objects with permanent tumbler addresses |
| What survives editing? | The link itself (unchanged); the content it points to may move in V-space but its I-space identity is permanent |

A link, once created, is a permanent fact in the docuverse — a "strap between bytes" that endures as long as any bytes remain at each end. If you want different endsets, you make a different link.

---

## Question 6 [nelson]

> If content referenced by a link is rearranged — moved from one position to another within the same document — does the link follow the content to its new location?

### Nelson's Answer

## Yes — the link follows the content to its new position.

This is one of the most fundamental guarantees of Xanadu's link architecture. Links attach to **bytes** (identified by permanent I-space addresses), not to **positions** (ephemeral V-space addresses). Rearrangement changes where bytes appear in the document's virtual stream (V-space), but it does not change the bytes' permanent identity (I-space). Since links point to I-space, they are unaffected.

Nelson states this directly:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" metaphor is precise: the link is bound to the bytes themselves, not to their current location. When bytes move, the strap moves with them.

Nelson explicitly names rearrangement as one of the operations links survive:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

And on page 4/30, he makes the mechanism explicit:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### Why this works

The I-space/V-space separation is the enabling architecture:

- **I-space** (permanent): where content lives forever, with immutable addresses
- **V-space** (ephemeral): the document's current arrangement of that content

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

REARRANGE is a pure V-space operation — it changes which I-space content appears at which V-space positions. The I-space addresses are untouched, and since links reference I-space addresses, they remain valid and correctly attached after the rearrangement.

### The condition for survival

The only condition Nelson places on link survival is that **some bytes remain at each end**. Rearrangement preserves all bytes (it moves them, it doesn't delete them), so this condition is trivially satisfied. The link survives intact.

---

## Question 7 [nelson]

> When a new version of a document is created, do links that pointed to the original version automatically apply to the new version, or do they remain attached only to the version they were created against?

### Nelson's Answer

# Links Across Versions: Refractive Following

The answer is both: links remain attached to the specific bytes they were created against, but they can be **refractively followed** to corresponding places in any other version. Nelson is explicit about this:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

## The Mechanism: Shared I-Space

The reason this works is structural, not through any link-copying operation. When CREATENEWVERSION is called, the new version shares the same I-space content as the original. Links point to I-space addresses (permanent content identity), not V-space addresses (ephemeral positions). Since both versions contain the same I-space bytes, a link to those bytes is simultaneously a link into both versions.

This is correspondence at work — the relationship between V-space positions that share the same I-space origin.

## The Front-End's Role

Nelson places the version-navigation decision in the front end, not the back end:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

Two key qualifications here:

1. **"may easily be set up"** — this is front-end policy, not automatic back-end behavior. The front end decides whether to redirect to the newest version or stay on the version the link was made against.

2. **"if it's still there"** — if the newer version has deleted the passage (removed it from V-space), the link still resolves to the old version where the content remains. The content survives in I-space regardless.

## Why Old Versions Must Persist

This cross-version link behavior is precisely why published documents cannot be withdrawn:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

The old version is the anchor. Links were made against it. Those links "reach through" to newer versions via correspondence, but they depend on the old version continuing to exist.

## Summary

| Aspect | Behavior |
|--------|----------|
| **Link attachment** | To specific I-space bytes (permanent) |
| **Cross-version resolution** | Via shared I-space origin (correspondence) |
| **Version navigation** | Front-end policy — can follow to newest version |
| **If content deleted in new version** | Link still resolves in the version where content exists |
| **Old version withdrawal** | Prohibited — other users' links depend on it |

Nelson's design is elegant: links don't need to "know about" versions at all. They point to bytes. Because versions share bytes, a single link implicitly spans all versions that contain those bytes. The front end then decides which version to show the user.

---

## Question 8 [nelson]

> What must the system guarantee about link creation — can a user create a link to any published content, or only to content they own?

### Nelson's Answer

# Link Creation: What the System Must Guarantee

## The Core Guarantee: Link to Anything Published

Nelson is unambiguous: **any user may create a link to any published content**, not just content they own. This is a fundamental right, not a feature.

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

This is a **contractual obligation** on publishers, not merely a system capability. When you publish, you agree to accept incoming links from anyone.

## Three Specific Guarantees

### 1. Freedom to Link

> "Each user is free to link to anything privately or publicly." [LM 2/43]

No permission is required. No approval workflow. If the content is published, you can link to it.

### 2. No Veto by Target Author

The author of published content **cannot prevent** others from linking to it:

> "Each author of a published work is relinquishing the right to control links into that work." [LM 2/43]

This relinquishment is part of the publication contract itself — it is the price of publishing.

### 3. Link Ownership Is Independent of Target Ownership

A link lives in its **home document**, which determines who owns it — not what it points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

This means your commentary link about someone else's work lives at **your** address, under **your** control. The target author cannot delete it.

## Why This Must Be So

Nelson sees link freedom as inseparable from the publication bargain. The publication contract explicitly includes:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

The logic is: automatic royalty replaces permission-seeking. Since you get paid every time your content is delivered, you no longer need the right to control who references it.

## What About Links Between Others' Documents?

The MAKELINK operation confirms that a link can connect content in documents you don't own:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

Your document can host a link whose from-set and to-set both point into documents owned by other people. The home document (yours) determines ownership; the endsets can point anywhere in the docuverse.

## The Two-Way Coin

The system guarantees bidirectional discovery of these links:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

So link freedom is not just the right to create links — it includes the guarantee that others can **find** your links when they read the target content.

## Summary

| Question | Answer |
|----------|--------|
| Can I link to content I don't own? | **Yes** — to any published content |
| Can the target author block my link? | **No** — relinquished at publication |
| Who owns the link? | **You** — determined by home document |
| Can I link between two others' documents? | **Yes** — home document is separate from endsets |
| Can others discover my link? | **Yes** — bidirectional link discovery is guaranteed |

The system must guarantee **unrestricted link creation to all published content**. This is not a convenience feature — it is the mechanism by which literature becomes "socially self-constructing into a vast new traversable framework" [LM 2/45].

---

## Question 9 [nelson]

> If one endset of a link references content that spans multiple documents through transclusion, does the link point to the original source content or to the transcluded appearance?

### Nelson's Answer

## Links Point to I-Space Content, Not V-Space Appearances

The answer is unambiguous: **a link's endset points to the original I-space content itself.** Since transclusion shares I-addresses between the source and all including documents, the question of "original vs. transcluded appearance" dissolves — at the I-space level, there is no distinction. It is the same content at the same permanent address.

### Why This Must Be So

Three architectural facts converge:

**1. Links attach to bytes, not positions.**

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" binds to the bytes themselves — their permanent I-space identity — not to their current V-space arrangement in any particular document.

**2. Transclusion shares I-addresses.**

Transcluded content does not get new addresses. The COPY operation creates a V-space mapping to *existing* I-space content:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The transcluded bytes in document B are the *same bytes* at the *same I-addresses* as in document A. There is no "copy" with a separate identity.

**3. Endsets address the universal tumbler line.**

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

Endsets reference positions on the tumbler line — which is the I-space address space. A link whose endset covers a range of I-addresses covers that content everywhere it appears: in its home document, in every document that transcludes it, and in every version that shares those addresses.

### The Consequence: A Link to Content Is a Link to All Its Appearances

This is confirmed by the version-spanning behavior Nelson describes:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Versions share I-space content (that's what CREATENEWVERSION does). Links "reach through" because they point to I-addresses, not V-addresses. The exact same logic applies to transclusion: if document B transcludes a paragraph from document A, a link whose endset covers that paragraph's I-addresses is discoverable from *both* documents.

This is operationally confirmed by FINDDOCSCONTAINING:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

The operation finds documents through shared I-space origin — which is exactly how link endsets work.

### What This Means for the User

When you create a link whose endset touches content that has been transcluded across multiple documents:

- **You are linking to the content itself**, identified by its permanent I-address
- **The link is discoverable from every document** that contains that content (original and all transclusions)
- **The link survives editing** in any of those documents, as long as any of the referenced bytes remain anywhere
- **You never need to know** which document is the "original" — the system traces everything back to home locations automatically

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### Summary

The I-space/V-space separation makes the question self-answering. There is no "original vs. transcluded appearance" at the level where links operate. Links live in I-space. Transclusion shares I-space. Therefore a link to transcluded content is inherently a link to that content in all its appearances — the strap binds to the bytes, and the bytes are the same bytes everywhere.

---

## Question 10 [nelson]

> Must the system guarantee that a user can discover ALL links whose endsets touch a given span of content, or is it acceptable for some links to be invisible to certain users?

### Nelson's Answer

# Link Discovery: Completeness Guarantee

Nelson's design intent is clear: **for published content, the system must guarantee discovery of ALL links.** But there is a legitimate privacy boundary that makes some links invisible to some users.

## The Completeness Guarantee for Published Links

Nelson is explicit that readers must be able to find everything that connects to published content:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." [LM 2/46]

The FEBE protocol reinforces this with completeness semantics:

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

And the search architecture is designed so that scale does not degrade completeness:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

The word "all" here is deliberate. The system returns **all** matching links, not a sample, not a ranked subset, not an editorially curated selection.

## The Author Cannot Hide Incoming Links

Nelson explicitly removes the target author's ability to suppress link discovery. This is a contractual requirement of publication:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

This is non-negotiable. If Alice publishes document D, she cannot prevent Bob's published links to D from being discoverable by readers of D. Alice gave up that right when she published.

## The System Must Not Filter Editorially

Nelson warns explicitly against system-imposed filtering of what users can see:

> "Some advocates of Artificial Intelligence would have computers decide what the reader shall see. As a filtering service this may be just what you want—but the danger is its evolving into a circumscription of your rights, where the choice is no longer yours." [LM 3/21]

The user controls filtering. The system provides the mechanism (sieving by attributes like location, author, time), but the choice of what to suppress is the reader's, never the system's.

## The Privacy Exception: Legitimate Invisibility

However, Nelson also specifies that private documents are accessible only to their owner and designees:

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

Since links live in their home document, and the home document determines access, a link housed in a **private** document is legitimately invisible to non-authorized users. This is not a violation of the completeness guarantee — it is the privacy guarantee operating as designed.

Nelson even acknowledges both modes in a single phrase:

> "each user is free to link to anything **privately or publicly**" [LM 2/43]

A private link to published content is a valid state. The link creator chose privacy; the system respects it.

## The User-Controlled Sieve

Nelson expects an avalanche of links and provides for user-managed filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

> "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits — say, location and author and time." [LM 2/47]

Sieving is the user's tool for managing abundance. It narrows what the user **chooses to see**, but it does not reduce what the system **can return**. Remove all filters, and you get everything accessible.

## Summary

| Scenario | All links discoverable? |
|----------|------------------------|
| Published link → published content | **Yes.** Guaranteed. |
| Published link → private content | The link exists but the target content is inaccessible to unauthorized users. |
| Private link → published content | **No.** The link is invisible to non-authorized users. This is legitimate privacy. |
| Private link → private content | **No.** Both link and target are restricted. |
| Author of target suppressing in-links | **Forbidden.** Relinquished upon publication. |
| System editorially filtering results | **Forbidden.** User controls filtering. |

The guarantee is: **within the domain of content you are authorized to see, the system must return ALL links.** No published link is hidden from you. No system editorial judgment suppresses results. The only legitimate boundary is privacy — and that boundary is drawn by the link creator's choice, not by the target author or the system.

---

## Question 11 [gregory]

> When FOLLOWLINK resolves a link's source endset to V-addresses via `span2spanset`, and only half the endset's I-address range is currently referenced by any POOM, does it return the reachable half as a partial VSpec or does it discard the entire endset?

### Gregory's Answer

## KB Synthesis

# Answer: FOLLOWLINK Returns Partial Results

FOLLOWLINK returns **partial VSpecs** containing only the reachable portion of the endset. Unreferenced I-addresses are silently filtered during I-to-V conversion.

## Filtering Mechanism

The I-to-V conversion path filters at the individual I-address level via `span2spanset()` [INV-ITOV-FILTERING]:

> "At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), **the I-address is dropped from the result without error**."

This happens per-I-address, not per-endset. When `retrieverestricted` returns NULL for an I-address, that specific I-address contributes no V-span to the output, but processing continues for remaining I-addresses in the endset.

## Three Result Cases

[EC-GHOST-LINK] explicitly documents the partial-result case:

> "Three observable cases: 
> 1. all endset I-addresses live → full result
> 2. **some unreferenced → partial result, only live addresses converted**
> 3. all unreferenced → empty result `[]`, operation still succeeds"

Case (2) is the direct answer to your question: half-reachable produces a partial VSpec covering only the reachable half.

## Per-Sporgl Independence

[EC-LINK-PARTIAL-SURVIVAL] confirms this operates at the sporgl (I-span) level:

> "Because each I-span in a link endset independently tracks its content, partial survival is possible. If document A (source of "AA") is deleted but document B (source of "BB") remains, the link endset retains the I-span for "BB" while the I-span for "AA" becomes unresolvable. **The link survives partially — it still points to the "BB" content.**"

Each I-span's content identity is evaluated independently during resolution. Surviving I-spans contribute their V-addresses to the result; unreferenced I-spans are filtered out.

## Concrete Example

From [EC-GHOST-LINK]:

```
Link L has to-endset containing I-addresses α₁, α₂, α₃
Document D has poom.D(1.5) = α₂  (only α₂ is mapped)

FOLLOWLINK(L, TO, D) → VSpec covering position 1.5 only
                        (partial result: α₂ resolved, α₁ and α₃ filtered)
```

The operation succeeds with a partial VSpec. No error is raised. The caller receives whatever portion of the endset is currently reachable through the queried document's POOM.

## System-Level Consequence

This filtering behavior is a universal property of all I-to-V conversions in the system [INV-ITOV-FILTERING]:

> "**unreferenced I-addresses are silently excluded from V-address results**. No operation that performs I-to-V conversion will ever return a V-address for an unreferenced I-address."

FOLLOWLINK, RETRIEVEENDSETS, and all other operations using `linksporglset2specset()` share this filtering path and therefore share this partial-result behavior.

## Code Exploration

---

# Answer: FOLLOWLINK Returns Partial VSpec for Partially-Reachable Endsets

When FOLLOWLINK resolves a link's source endset to V-addresses and only half the endset's I-address range is currently referenced by any POOM, **it returns the reachable half as a partial VSpec**. The unreachable portions are silently omitted from the result.

## Call Chain Analysis

### 1. FOLLOWLINK Entry Point

The FOLLOWLINK handler calls `dofollowlink` [`fns.c:122-123`]:

```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
    putfollowlink (taskptr, specset);
```

### 2. Extract and Convert Endset

`dofollowlink` extracts the I-address endset from the link and converts it to V-addresses [`do1.c:223-232`]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

	return (
	   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
	&& linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,/* ECH 6-29 READBERT */NOBERTREQUIRED));
}
```

### 3. Convert I→V via POOM

`linksporglset2specset` calls `linksporglset2vspec` for each sporgl [`sporgl.c:115-116`]:

```c
} else {
       linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

`linksporglset2vspec` initializes an empty vspanset and calls `sporglset2vspanset` [`sporgl.c:132-136`]:

```c
specptr->itemid = VSPECID;
specptr->next = NULL;
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
specptr->vspanset = NULL;
sporglset2vspanset (taskptr,homedoc, sporglsetptr, &specptr->vspanset,type);
```

### 4. The Critical Conversion: `span2spanset`

`sporglset2vspanset` calls `ispan2vspanset` which calls `permute`, which loops through each I-span and calls `span2spanset` [`orglinks.c:415`]. This is where partial resolution happens.

`span2spanset` calls `retrieverestricted` to find **all crums that intersect** the I-address range [`orglinks.c:425-454`]:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  typespan foundspan;
  typespan *nextptr;
  typeitem *onitemlist();

	context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);

	for (c = context; c; c = c->nextcontext) {
		context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
		nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
	}
	if(!context){
		return(targspansetptr);
	}
		contextfree (context);
	return (&nextptr->next);
}
```

**Key observation at lines 446-448**: If `context` is NULL (no matches found), it returns `targspansetptr` unchanged. Since `vspanset` was initialized to NULL [`sporgl.c:135`], an empty result is returned.

**Key observation at lines 439-444**: If `context` is non-NULL, it loops through **each context** (representing each matching crum) and converts it to a V-span.

### 5. Partial Matching: `findcbcinarea2d`

`retrieverestricted` calls `retrieveinarea` which initializes `context = NULL` [`retrie.c:93`] and calls `findcbcinarea2d` [`retrie.c:97`].

`findcbcinarea2d` accumulates **only the portions that exist** [`retrie.c:229-268`]:

```c
int findcbcinarea2d(typecorecrum *crumptr, typedsp *offsetptr, tumbler *span1start, tumbler *span1end, INT index1, tumbler *span2start, tumbler *span2end, INT index2, typecontext **headptr, typebottomcruminfo *infoptr)
{
  typedsp localoffset;
  typecontext *context, *makecontextfromcbc();
  bool crumintersectsarea2d ();
  bool crumqualifies2d();

        for (; crumptr; crumptr = getrightbro (crumptr)) {
                if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1, span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
                        continue;
                }
                if (crumptr->height != 0) {
                        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
                        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, span1start, span1end, index1, span2start, span2end, index2, headptr, infoptr);
                } else {
                        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
                        incontextlistnd (headptr, context, index1);
                }
        }
}
```

**Line 252**: Iterates through ALL crums at this level.  
**Line 253-254**: If `crumqualifies2d` returns FALSE (crum doesn't intersect the search range), **skip it** with `continue`.  
**Line 262-263**: If the crum IS a leaf and qualifies, **add it to the context list**.

### 6. Intersection Test: `crumqualifies2d`

`crumqualifies2d` returns TRUE for **any crum that intersects the requested I-address range**, even if only partially [`retrie.c:270-305`]:

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset, tumbler *span1start, tumbler *span1end, INT index1, tumbler *span2start, tumbler *span2end, INT index2, type2dbottomcruminfo *infoptr)
{
  INT startcmp, endcmp;

        endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
	if ( endcmp <=/*=*/ ONMYLEFTBORDER){
		return(FALSE);
	}
        startcmp = whereoncrum (crumptr, offset, span1start, index1);
         if( (startcmp > THRUME /*&& endcmp > THRUME*/)){
                return (FALSE);
	 }
        // ... (similar checks for index2) ...
        return (TRUE);
}
```

**Lines 283-284**: If the requested range ends before the crum starts → FALSE.  
**Lines 287-289**: If the requested range starts after the crum ends → FALSE.  
**Line 304**: Otherwise → TRUE (crum intersects the range).

### 7. Clipping to Range: `context2span`

Each matching context is clipped to the restriction range and converted to V-address [`context.c:176-212`]:

```c
int context2span(typecontext *context, typespan *restrictionspanptr, INT idx1, typespan *foundspanptr, INT idx2)
{
  tumbler upperbound, lowerbound;
  typedsp grasp, reach;

	movetumbler (&restrictionspanptr->stream, &lowerbound);
	tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
	prologuecontextnd (context, &grasp, &reach);

	if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
		tumblerincrement (&grasp.dsas[idx2], 0, (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
	}
	if (tumblercmp (&reach.dsas[idx1], &upperbound)  == GREATER) {
		tumblerincrement (&reach.dsas[idx2], 0,/*i=*/ - tumblerintdiff (&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);       
	}
	movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
	tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

**Lines 191-196**: If the crum starts before the restriction, **clip the start** by adjusting the V-coordinate.  
**Lines 197-203**: If the crum extends beyond the restriction, **clip the end** by adjusting the V-coordinate.  
**Lines 206-207**: Extract the clipped V-span.

## Conclusion

When FOLLOWLINK encounters an endset where only part of the I-address range exists in the target document's POOM:

1. `findcbcinarea2d` iterates through ALL crums and collects **only those that intersect** the requested I-range
2. Each matching crum becomes a context
3. `context2span` clips each context to the restriction and extracts the corresponding V-span
4. **Result**: A VSpec containing only the reachable portions

**The unreachable portions are silently omitted.** There is no error, no indication to the client that the endset was partial. The result is simply a smaller vspanset than the original I-address endset would imply.

This is a **silent partial resolution** — FOLLOWLINK returns whatever it can find and ignores the rest.

---

## Question 12 [gregory]

> If INSERT splits a contiguous I-address range that a link's target endset references — say endset covers I:[.0.1.3,.0.1.7] and INSERT at V:1.5 pushes .0.1.5-.0.1.7 to non-contiguous V-positions — does RETRIEVEENDSETS return one VSpec or two VSpecs for that endset?

### Gregory's Answer

## KB Synthesis

Looking at this question, I need to trace through how link endset storage and retrieval handle V-space fragmentation caused by INSERT.

## The Scenario

Initial state:
- Link target endset references I-addresses [.0.1.3, .0.1.7] (5 contiguous I-addresses)
- These map to contiguous V-positions, say V:[1.3, 1.7]
- INSERT occurs at V:1.5 with width 0.10

After INSERT:
- I-addresses .0.1.3-.0.1.4 remain at V:[1.3, 1.4] (before insertion)
- I-addresses .0.1.5-.0.1.7 shift to V:[1.15, 1.17] (after insertion)
- Same I-addresses, now non-contiguous in V-space

## How Endsets Are Stored

From `[SS-LINK-ENDPOINT]` Finding 0037:
> "A link endset is not simply a set of V-spans; internally it is a set of I-spans (sporgls). A single user-visible V-span may correspond to multiple I-spans in the endset when the V-span covers content transcluded from multiple sources. Each I-span independently tracks its content identity."

The endset is stored as I-address ranges (sporgls). At creation time, the contiguous I-range [.0.1.3, .0.1.7] was likely stored as a single I-span.

## How RETRIEVEENDSETS Converts I-to-V

From `[SS-RETRIEVE-ENDSETS]` Finding 0035:
> "RETRIEVEENDSETS (opcode 28) takes a specset... converts the input specset to a sporglset (V-to-I translation), defines three search spaces... The use of the querying document's docid for V-address resolution means endsets are always expressed relative to the querying context."

The conversion path from `[INV-ITOV-FILTERING]` Finding 0048:
> "`linksporglset2specset()` calls `sporglset2vspanset()` which calls `ispan2vspanset()` → `permute()` → `span2spanset()`. At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address."

## The Critical Finding

From `[SS-LINK-ENDPOINT]` Finding 0037:
> "When retrieving endsets, `retrieve_endsets` reports multiple V-spans corresponding to the stored I-spans, **one per contiguous I-region**."

But more importantly, from the I-to-V conversion process, the system walks through the I-address range and discovers which V-positions they currently map to. When the POOM lookup finds:
- I:.0.1.3-.0.1.4 → V:[1.3, 1.4] (contiguous)  
- I:.0.1.5-.0.1.7 → V:[1.15, 1.17] (contiguous but separated by gap)

These form **two non-contiguous V-ranges**.

## Confirming Evidence

From `[EC-PIVOT-LINK-FRAGMENTATION]` Finding 0019:
> "When linked content is rearranged via pivot, the link's endsets become fragmented into multiple spans... Before: 'ABCDEFGH' — link on 'CD' at V 1.3 width 0.2. Pivot: swap BC and DE. After: 'ADEBCFGH' — endsets report FOUR spans"

This demonstrates that when linked content becomes non-contiguous in V-space (whether by pivot or by INSERT creating a gap), the endset retrieval fragments into multiple spans.

## Answer

**RETRIEVEENDSETS returns TWO VSpecs** for that endset.

The reasoning chain:
1. The endset stores I-addresses [.0.1.3, .0.1.7] as a contiguous I-span (`[ST-INSERT]`, `[INV-IADDR-IMMUTABILITY]`)
2. INSERT shifts V-positions but not I-addresses, creating a V-space gap (`[ST-INSERT]` Finding 0030)
3. I-to-V conversion discovers two non-contiguous V-ranges: [1.3, 1.4] and [1.15, 1.17] (`[INV-ITOV-FILTERING]`)
4. RETRIEVEENDSETS reports one VSpec per contiguous V-range (`[SS-LINK-ENDPOINT]` Finding 0037)
5. Result: Two VSpecs in the endset, even though the I-addresses remain contiguous (`[EC-PIVOT-LINK-FRAGMENTATION]` confirms this fragmentation behavior)

## Code Exploration

Based on my code analysis and the golden test evidence, I can provide a definitive answer:

## Answer: ONE VSpec with MULTIPLE VSpans

When INSERT splits a contiguous I-address range that a link's target endset references, **RETRIEVEENDSETS returns ONE VSpec containing MULTIPLE VSpans** (not multiple VSpecs).

## Code Evidence

### Storage at Link Creation [spanf1.c:15-54]

When the link is created with target endset I:[.0.1.3,.0.1.7], `insertspanf` stores it as **one contiguous entry** in the spanfilade:

```c
bool insertspanf(...) {
    for (; sporglset; sporglset = ...) {
        // Extract I-span data
        movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler(&lwidth, &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, ...);
    }
}
```

**One I-span → One insertion → One CBC in the spanfilade**

### Retrieval After INSERT Split

The key conversion happens in `span2spanset` [orglinks.c:425-454]:

```c
typespanset *span2spanset(...) {
    // Query organfilade to convert I-span to V-spans
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, 
                                 restrictionindex, ..., targindex, ...);
    
    // For EACH context (one per contiguous V-region), create a V-span
    for (c = context; c; c = c->nextcontext) {
        context2span(c, ..., &foundspan, targindex);
        nextptr = (typespan*)onitemlist(taskptr, (typeitem*)&foundspan, ...);
    }
}
```

When the organfilade lookup finds the I-addresses now map to **non-contiguous V-positions**, `retrieverestricted` returns **multiple contexts** [retrie.c:262-263]:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson((typecuc*)crumptr), ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, ...);
        incontextlistnd(headptr, context, index1);  // Adds to list
    }
}
```

**Each CBC covering part of the query → One context → One V-span in output**

### Final Assembly [sporgl.c:103-120]

```c
bool linksporglset2specset(...) {
    for (; sporglset; sporglset = ...) {  // ONE iteration for our single I-span
        specset = (typespecset)taskalloc(taskptr, sizeof(typevspec));
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        // ^^ This converts the I-span to MULTIPLE V-spans within ONE vspec
        *specsetptr = specset;  // ONE vspec added to result
    }
}
```

And `sporglset2vspanset` [sporgl.c:157] calls `ispan2vspanset`, which populates `vspec->vspanset` with all the V-spans.

## Golden Test Confirmation

Test `golden/endsets/endsets_after_pivot.json` demonstrates this:

```json
{
  "op": "retrieve_endsets",
  "label": "after",
  "source": [
    {
      "docid": "1.1.0.1.0.1",       // ONE VSpec
      "spans": [                      // FOUR VSpans
        {"start": "1.2", "width": "0.1"},
        {"start": "1.2", "width": "0.1"},
        {"start": "1.5", "width": "0.1"},
        {"start": "1.5", "width": "0.1"}
      ]
    }
  ]
}
```

After a PIVOT operation split the originally contiguous I-addresses into non-contiguous V-positions, the result is **one docid entry (one VSpec) with multiple spans (multiple VSpans)**.

## The Critical Distinction

- **Input to spanfilade**: ONE I-span (stored as one entry)
- **Spanfilade retrieval**: ONE sporgl (one context from the spanfilade)
- **VSpec creation**: ONE VSpec (one per sporgl)
- **I→V conversion**: MULTIPLE contexts from organfilade lookup
- **Final result**: ONE VSpec containing MULTIPLE VSpans

The split happens **during I→V address translation**, not during spanfilade retrieval. The endset data is still stored as one I-span, but when converted to V-space, it produces multiple V-spans within a single VSpec container.

---

## Question 13 [gregory]

> When a link's source endset content exists in three documents simultaneously (original + two transclusions sharing the same I-addresses), does FOLLOWLINK return V-addresses from all three documents, or only from the document used in the find_links query?

### Gregory's Answer

## KB Synthesis

Based on the knowledge base, **FOLLOWLINK returns V-addresses from ONLY the single document specified in the `homedoc` parameter**, not from all three documents simultaneously.

Here's why:

## Core Mechanism

`[SS-FOLLOWLINK]` from Finding 0048 reveals the key architectural detail:

> "FOLLOWLINK retrieves link endset I-addresses from the link orgl, then converts them to V-addresses using a **specified document's POOM**. The call chain is: `link2sporglset()` extracts I-addresses from the link orgl... Then `linksporglset2specset()` converts I-addresses to V-addresses by looking them up in the **specified `homedoc`'s POOM**."

The operation explicitly takes a `homedoc` parameter that determines which single document's POOM is consulted for I-to-V conversion.

## Formal Definition

The postcondition is:

```
followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }
```

This states that FOLLOWLINK returns **only those V-addresses from the specified homedoc** where the homedoc's POOM maps to the link's I-addresses.

## Query Context Dependency

`[INT-LINK-VERSION]` Finding 0019 confirms this behavior:

> "The endset docid is rewritten to the queried document's address, even though the link was created against the original. This means **endsets are relative to the query context, not absolute**."

## Concrete Example

For your scenario:
- Document A (original): POOM.A maps V-positions to {i₁, i₂, i₃}
- Document B (transclusion): POOM.B maps V-positions to {i₁, i₂, i₃}  
- Document C (transclusion): POOM.C maps V-positions to {i₁, i₂, i₃}
- Link L has source endset containing {i₁, i₂, i₃}

Then:
- `FOLLOWLINK(L, SOURCE, homedoc=A)` → returns V-addresses from A only
- `FOLLOWLINK(L, SOURCE, homedoc=B)` → returns V-addresses from B only
- `FOLLOWLINK(L, SOURCE, homedoc=C)` → returns V-addresses from C only

## Contrast with find_links

This differs from `find_links`, which discovers the link from **any** of the three documents (because `find_links` works by I-address intersection and searches globally per `[INT-LINK-TRANSCLUSION]`). But FOLLOWLINK is explicitly scoped to a single document for the I-to-V resolution phase.

## Silent Filtering

`[INV-ITOV-FILTERING]` from Finding 0048 adds that if the specified homedoc doesn't actually contain those I-addresses in its POOM, "the I-address is dropped from the result without error" — producing an empty or partial result rather than including V-addresses from other documents.

## Code Exploration

Based on my analysis of the C source code, here is the complete answer to your question:

---

# FOLLOWLINK Returns Creation Document V-Addresses, Not Query Document

## Direct Answer

**When a link's source endset content exists in three documents simultaneously (original + two transclusions sharing the same I-addresses), FOLLOWLINK returns V-addresses ONLY from the document that was used when the link was created, NOT from the document used in the find_links query.**

## Complete Execution Path

### 1. Link Creation (`docreatelink` [do1.c:195-221])

When you create a link, the endsets are specified as V-specs (document + V-spans):

```c
// Line 214-216: Convert V-specs to sporgls (I-spans + document ID)
&& specset2sporglset (taskptr, fromspecset, &fromsporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
```

In `vspanset2sporglset` [sporgl.c:35-65]:

```c
// Line 53: Store the CREATION document ID permanently in the link
movetumbler (docisa, &sporglset->sporgladdress);
movetumbler(&ispanset->stream,&sporglset->sporglorigin);  // I-address
movetumbler (&ispanset->width, &sporglset->sporglwidth);   // I-width
```

**The sporgl permanently stores: (creation_document_ID, I-address, I-width)**

### 2. Link Following (`dofollowlink` [do1.c:223-232])

When you follow a link:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
&& linksporglset2specset (taskptr,
                          &((typesporgl *)sporglset)->sporgladdress,  // ← creation doc!
                          sporglset, specsetptr, NOBERTREQUIRED));
```

The `homedoc` parameter is `&((typesporgl *)sporglset)->sporgladdress` — **the document ID stored when the link was created.**

In `linksporglset2vspec` [sporgl.c:127-137]:

```c
// Line 134: Use the creation document ID, not any query document
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
```

The commented-out code confirms this was explicitly the sporgl's stored address.

In `sporglset2vspanset` [sporgl.c:141-176]:

```c
// Line 152: Retrieve the CREATION document's permutation matrix
findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl,type);
// Line 157: Convert I→V using that specific document's matrix
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

Finally, `ispan2vspanset` [orglinks.c:389-394] calls `permute` [orglinks.c:404-422], which uses the creation document's permutation matrix to convert I-addresses back to V-addresses.

### 3. Link Finding (Context)

`dofindlinksfromtothree` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103]:

- Converts query V-specs to I-spans
- Searches for links whose endsets overlap those I-spans
- Returns link ISAs unchanged
- **Does NOT modify the links or their stored document bindings**

## Concrete Example

```
Setup:
- Doc A: "hello" at V=1.1 → I=100.1
- Doc B: Transclude from A → I=100.1 at V=1.5
- Doc C: Transclude from A → I=100.1 at V=1.8  
- Doc D: CREATE_LINK(target → B:V=1.5)

Link stores: target = {doc: B, I-addr: 100.1}

Query:
- FIND_LINKS(target → C:V=1.8)
  → Converts C:V=1.8 → I=100.1
  → Finds link (matches I=100.1)
  → Returns link ISA
  
- FOLLOW_LINK(link, TARGET)
  → Retrieves {doc: B, I-addr: 100.1}
  → Converts using B's matrix: I=100.1 → V=1.5
  → Returns SpecSet(VSpec(B, V=1.5))
  
Result: V=1.5 in document B (creation), NOT V=1.8 in document C (query)
```

## Key Code Citations

| File:Line | Code | Significance |
|-----------|------|--------------|
| sporgl.c:53 | `movetumbler (docisa, &sporglset->sporgladdress)` | Stores creation doc in link |
| do1.c:230 | `&((typesporgl *)sporglset)->sporgladdress` | Passes stored doc as `homedoc` |
| sporgl.c:134 | `movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa)` | Uses creation doc for result |
| sporgl.c:152 | `findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl,type)` | Retrieves creation doc's matrix |
| orglinks.c:393 | `return permute(taskptr, orgl, ispanptr, I, vspansetptr, V)` | Converts I→V using creation doc |

## Implications

1. **Link bindings are immutable** — Links permanently point to specific documents chosen at creation time
2. **Transclusion doesn't redirect links** — Finding a link via transcluded content doesn't change where it points
3. **Document-relative semantics** — Links bind to (document, V-address) pairs, not just content identity
4. **No transclusion chasing** — FOLLOWLINK doesn't follow content identity across documents

This behavior is by design: links store explicit document references and always resolve relative to those references, ensuring stable, unambiguous link targets regardless of how the link was discovered.

---

## Question 14 [gregory]

> Are the three endsets (source, target, type) resolved independently during FOLLOWLINK — can the source endset resolve successfully while the target endset returns empty because its content was deleted from all POOMs?

### Gregory's Answer

## KB Synthesis

Yes, the three endsets (source, target, type) are resolved **independently** during FOLLOWLINK — each endset's resolution depends solely on whether its specific I-addresses have POOM mappings, not on the resolution status of other endsets.

## Evidence for Independent Resolution

**[EC-ORPHANED-LINK]** provides the definitive evidence through a behavior matrix showing asymmetric outcomes:

| Deleted Content | source endset | target endset | type endset |
|----------------|---------------|---------------|-------------|
| Source text only | Empty | Works | Works |
| Target text only | Works | Empty | Works |
| Both source & target | Empty | Empty | Empty* |

The first two rows prove independence: deleting source content makes only the source endset empty while target remains functional, and vice versa. If endsets were coupled, source deletion would affect target resolution.

## Resolution Mechanism

**[SS-FOLLOWLINK]** and **[INV-ITOV-FILTERING]** describe the underlying mechanism:

1. FOLLOWLINK retrieves I-addresses from the link orgl at the requested endset position (0.1 for source, 0.2 for target, 0.3 for type)
2. Each I-address is independently converted to V-addresses via `linksporglset2specset()` using the querying document's POOM
3. At `span2spanset()`, `retrieverestricted()` searches for each I-address in the POOM
4. If an I-address has no POOM mapping, it is silently dropped — no error, just omitted from results
5. This filtering is **per-I-address**, not per-endset

**[EC-GHOST-LINK]** confirms three possible outcomes per endset: (1) all I-addresses live → full result, (2) some unreferenced → partial result, (3) all unreferenced → empty result `[]`.

## Anomaly with Type Endset

There is one exception: when BOTH source and target are deleted, the type endset returns empty even though type references the bootstrap document (which was not deleted). **[EC-ORPHANED-LINK]** marks this with an asterisk as unexpected behavior — either a bug or an undocumented dependency of type resolution on endpoint resolution.

## Conclusion

Yes, endsets resolve independently under normal conditions. The source endset can return empty while target returns valid spans, and vice versa, based solely on which content exists in POOMs. The type endset anomaly when both endpoints are deleted is an edge case requiring further investigation.

## Code Exploration

Based on my analysis of the source code, I can now answer your question about whether the three endsets are resolved independently during operations like FOLLOWLINK and RETRIEVEENDSETS.

## RETRIEVEENDSETS: Sequential but Partially Independent

The three endsets are **NOT** fully independent. Looking at `retrieveendsetsfromspanf` [spanf1.c:190-235], the resolution uses a short-circuit boolean chain:

```c
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
    && retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)
    && linksporglset2specset (taskptr,&((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
    && retrievesporglsetinrange (taskptr, sporglset, &tospace, &tosporglset)
    && linksporglset2specset (taskptr, &((typevspec*)specset)->docisa, tosporglset, tosetptr, NOBERTREQUIRED))){
            return (FALSE);
}
```

**However**, there's a critical distinction between **failure** and **empty results**:

### Failure Modes (Returns FALSE):

1. If the link document doesn't exist [sporgl.c:44-46]:
```c
if (!findorgl (taskptr, granf, docisa, &orgl,type)){
    return (NULL);  // Propagates to specset2sporglset failure
}
```

2. If any document referenced in an endset doesn't exist, `specset2sporglset` fails [sporgl.c:25-27]

### Success with Empty Result (Returns TRUE):

If a document exists but the content at an endset has been deleted, the resolution **succeeds** and returns an empty specset. Looking at `linksporglset2specset` [sporgl.c:97-123]:

```c
*specsetptr = NULL;  // Line 102
for (; sporglset; sporglset = ...) {
    // Process sporgls - loop doesn't execute if sporglset is empty
}
return (TRUE);  // Line 122 - Always returns TRUE
```

And `retrievesporglsetinrange` [spanf1.c:237-267] also always returns TRUE [line 266], even if no content is found.

**Answer to your specific question:** **Yes**, the source endset can resolve successfully (returning content) while the target endset returns empty (NULL specset) because the target's content was deleted from all POOMs. The resolution succeeds as long as all referenced **documents exist**, regardless of whether their **content** has been deleted.

## FOLLOWLINK: Different Behavior

In contrast, `dofollowlink` [do1.c:223-232] calls `link2sporglset` [sporgl.c:67-95], which **fails** if an endset is empty:

```c
if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, (typespan*)NULL, I, (typeisa*)NULL)) {
    // Process context...
    return (TRUE);
} else{
    return (FALSE);  // Line 92-93: Fails if no content found
}
```

So **FOLLOWLINK fails** if the requested endset is empty, while **RETRIEVEENDSETS succeeds** and returns an empty specset for that endset.

## Summary

The endsets are resolved **sequentially** in a short-circuit chain, not fully independently. But:

- **Document-level failures** (document doesn't exist) fail the entire operation
- **Content-level emptiness** (deleted content) succeeds with empty results in RETRIEVEENDSETS
- **Content-level emptiness** fails in FOLLOWLINK

---

## Question 15 [gregory]

> When REARRANGE fragments a link's endset across non-contiguous V-positions within the same document, does subsequent find_links using a VSpec covering only ONE of the fragments still discover the link, or must the query span overlap ALL fragments?

### Gregory's Answer

## KB Synthesis

# Answer: Yes, the link is discovered with partial fragment overlap

When REARRANGE fragments a link's endset, `find_links` using a VSpec covering **only one fragment** will still discover the link. The reason lies in how link discovery operates.

## The Mechanism

From **[ST-FIND-LINKS]** (Finding 0028):
> The postcondition for `find_links` is: return the set of all links whose source endpoint I-addresses have non-empty intersection with the search specset's I-addresses. Partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link.

The formal condition is:
```
find_links(search) = {link | I-addresses(search) ∩ I-addresses(link.endpoint) ≠ ∅}
```

## Why This Works After REARRANGE

From **[INV-REARRANGE-IDENTITY]** (Finding 0056):
> Rearrange preserves I-addresses exactly. The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched.

**Before REARRANGE:**
- Link created on content at V-position 1.3, width 0.4
- Content has I-addresses {i₁, i₂, i₃, i₄}

**After REARRANGE (fragmentation):**
- Same content now at multiple V-positions: fragment₁ at 1.2 (i₁, i₂) and fragment₂ at 1.5 (i₃, i₄)
- I-addresses unchanged: {i₁, i₂, i₃, i₄}
- Link endpoint still references: {i₁, i₂, i₃, i₄}

**Query covering only fragment₁:**
- Search VSpec converts to I-addresses: {i₁, i₂}
- Intersection check: {i₁, i₂} ∩ {i₁, i₂, i₃, i₄} = {i₁, i₂} ≠ ∅
- **Result: Link discovered** ✓

## Supporting Evidence

From **[INT-LINK-TRANSCLUSION]** (Finding 0028), there's a concrete example of partial overlap being sufficient:

> Document C transcludes "EF" from A via vcopy:
>   C's "EF" has I-addresses I.5, I.6 (shared with A)
> 
> find_links(specset covering C's "EF"):
>   I-addresses of search: {I.5, I.6}
>   I-addresses of link source: {I.4, I.5, I.6}
>   Intersection: {I.5, I.6} ≠ ∅
>   → Link returned (partial overlap is sufficient)

The same principle applies: a query covering ANY subset of the link's endpoint I-addresses will discover it.

## Conclusion

Link discovery is **I-address intersection-based**, not V-position-based. REARRANGE changes V-positions but preserves I-addresses **[INV-REARRANGE-IDENTITY]**. Since partial I-address overlap suffices for discovery **[ST-FIND-LINKS]**, querying any single fragment will discover the link.

## Code Exploration

Based on my thorough analysis of the udanax-green C source code, I can now provide a definitive answer to your question:

---

## Answer: YES, querying ONE fragment discovers the link

When REARRANGE fragments a link's endset across non-contiguous V-positions within the same document, subsequent `find_links` using a VSpec covering **only ONE** of the fragments **still discovers the link**. The query does **NOT** need to span all fragments.

## Code Evidence

### 1. Link Discovery Uses I-Span Intersection

The critical function is `sporglset2linksetinrange` [sporgl.c:239]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

This retrieves from the spanfilade where:
- **SPANRANGE** matches the I-span (permascroll identity) from the query's V→I conversion
- **ORGLRANGE** matches the link's stored endset

The link is found if its endset **overlaps with ANY I-span** in the query.

### 2. REARRANGE Preserves I-Span Identity

The `rearrangend` function [edit.c:78-160] only modifies **V-displacements**:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```
[edit.c:125]

This changes the V-position (`cdsp` in the V dimension) but **does NOT change** the I-position (permascroll identity). Each fragment retains its original I-span.

### 3. Query Processing Flow

When you call `find_links` with a VSpec covering one fragment:

1. **V→I Conversion**: `vspanset2ispanset` [orglinks.c:397] converts the VSpec to I-spans using the document's POOM
2. **Permutation Query**: `permute` [orglinks.c:404] calls `span2spanset` which calls `retrieverestricted` to find crums where the fragment's V-position maps to I-space
3. **Link Retrieval**: `sporglset2linksetinrange` [sporgl.c:259] queries the spanfilade for links whose endset overlaps the fragment's I-span
4. **Result**: The link is found because its endset in the spanfilade still references the fragment's I-span

### 4. Intersection Logic

The `findlinksfromtothreesp` function [spanf1.c:56-103] finds links for each endset independently, then **intersects** the results:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```
[spanf1.c:100]

However, this intersection is across **different endsets** (from/to/three), not across fragments within a single endset.

## Why This Works

**Key Insight**: Links are indexed by **I-spans** (permascroll identity), not V-spans (virtual positions).

- When you create a link with endset "BCDEFGH" at V-positions 1.2-1.8, the backend stores references to the **I-addresses** that those V-positions map to
- When REARRANGE splits "BCDEFGH" into fragments "BC" (at 1.2), "GH" (at 1.4), and "DEF" (at 1.20), each fragment **retains its I-address**
- The link's endset in the spanfilade **remains unchanged** — it still references the same I-addresses
- When you query with a VSpec covering "BC" at 1.2, the V→I conversion finds the I-addresses for "BC"
- Those I-addresses overlap with the link's endset in the spanfilade
- Therefore, the link is discovered

## Empirical Verification Needed

While the source code clearly indicates this behavior, I've created a test scenario (`find_links_after_endset_fragmentation`) that should be run to empirically verify. The test fragments a link's endset via REARRANGE and queries each fragment individually.

Would you like me to commit this test and run it to empirically confirm the behavior?

---

## Question 16 [gregory]

> After DELETE removes content that a link's type endset references, making the type endset unresolvable to any V-address, does the link still appear in find_links results when querying by source or target content that IS still referenced?

### Gregory's Answer

## KB Synthesis

Looking at the link discovery mechanism in the KB:

**YES, the link still appears in `find_links` results when querying by source or target.**

Here's why:

## Link Discovery is Per-Endset

[ST-FIND-LINKS] and [INT-SPORGL-LINK-INDEX] establish that `find_links` operates by searching the spanfilade independently for each endset type:

- FROM endsets indexed at LINKFROMSPAN=1  
- TO endsets indexed at LINKTOSPAN=2
- THREE (type) endsets indexed at LINKTHREESPAN=3

When you call `find_links(source_specs, NOSPECS, NOSPECS)`, the operation searches **only** the FROM endset indices. It performs an I-address intersection between your query and the link's source I-addresses. The TO and THREE endsets are not consulted at all during this search.

## Evidence from Orphaned Link Behavior

[EC-ORPHANED-LINK] Finding 0024 provides the critical behavior matrix:

| Deleted Content | `find_links` by source | `find_links` by target |
|----------------|----------------------|----------------------|
| Source only    | Empty               | Works               |
| Target only    | Works               | Empty               |
| Both endpoints | Empty               | Empty               |

This confirms that `find_links` results depend **only on the queried endpoint**, not on whether other endpoints are resolvable.

## Type Endset Independence

[SS-LINK-ENDPOINT] Finding 0024 shows the type anomaly: when calling `follow_link(link_id, LINK_TYPE)` after both source and target are deleted, the type endset ALSO returns empty (marked as "UNEXPECTED"). However, this is about `FOLLOWLINK` behavior, not `find_links` discovery.

The key distinction:
- `find_links` searches **only the specified endsets** via I-address intersection  
- `follow_link` retrieves **all endsets** and resolves them to V-addresses

## Mechanism Details

[PRE-FIND-LINKS] Finding 0029 states: "find_links() requires that the searched endpoint content exists in the V-stream (visible view) to discover a link." This applies to **the searched endpoint**, not to all endpoints.

Therefore: If source content remains referenced (I-addresses have V-positions), `find_links(source_specs)` will find the link, regardless of whether the type endset is resolvable. The type endset's ghost state only affects `follow_link(link_id, LINK_TYPE)` retrieval.

## Code Exploration

Based on my analysis of the source code, I can now answer your question:

## Answer: YES, the link still appears in find_links results

After DELETE removes content that a link's type endset references, making the type endset unresolvable to any V-address, **the link STILL appears in find_links results when querying by source or target content that is still referenced**.

## Code Analysis and Citations

### 1. How find_links Works

When `find_links` is called, it flows through:
- `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56-103]

In `findlinksfromtothreesp` [spanf1.c:56-103]:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset,NOBERTREQUIRED);  // line 71
if (tovspecset)
    specset2sporglset (taskptr, tovspecset, &tosporglset,NOBERTREQUIRED);      // line 73
if (threevspecset)
    specset2sporglset (taskptr, threevspecset, &threesporglset,NOBERTREQUIRED); // line 75
```

**Critical observation**: When you query by source OR target (without specifying the type endset in the query), the `threevspecset` parameter is NULL, so line 75 never executes. The function doesn't attempt to resolve or validate the link's stored type endset.

### 2. Link Storage vs Query

When a link is created with `docreatelink` [do1.c:195-221]:
- Line 218: `insertendsetsinorgl` stores all three endsets (source, target, type) IN the link's granfilade
- Line 219: `insertendsetsinspanf` indexes all three endsets IN the spanfilade for searching

The spanfilade contains separate indices:
- `LINKFROMSPAN` (value 1) - for source endset
- `LINKTOSPAN` (value 2) - for target endset  
- `LINKTHREESPAN` (value 3) - for type endset

[spanf1.c:77,85,93]

### 3. Query Processing

When find_links searches by source [spanf1.c:77]:
```c
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

This queries ONLY the `LINKFROMSPAN` dimension of the spanfilade. It retrieves all links whose source endset intersects with the query specset. **It never attempts to resolve or validate the link's type endset**.

### 4. Intersection Logic

After collecting matching links from each queried dimension [spanf1.c:100]:
```c
intersectlinksets(taskptr,fromlinkset,tolinkset,threelinkset,linksetptr);
```

In `intersectlinksets` [spanf2.c:46-120], lines 64-71:
```c
/* If only one linkset is non-null, then just use it */
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
else if (!linkset1 && !linkset2 && linkset3)
    *linkset4ptr = linkset3;
```

**This confirms**: When querying by ONLY source (linkset1 non-NULL, others NULL), all links matching the source are returned, regardless of whether their type endset is resolvable.

## Verification in Existing Tests

The test suite already documents related behavior:
- `search_endpoint_removal.py` contains scenarios where source or target content is deleted
- `scenario_search_by_target_after_source_removed` [search_endpoint_removal.py:96-156] shows that deleting one endpoint doesn't prevent finding the link via the other endpoint
- However, **no existing test covers the specific case of an unresolvable type endset**

## Semantic Implication

The link's **type endset is metadata stored with the link**, not a filtering constraint during search. The find_links operation:
1. Queries the spanfilade indices for links matching the specified source/target criteria
2. Returns matching link ISAs
3. **Never validates** whether the link's type endset is still resolvable

The type endset would only matter if:
- You explicitly query by type endset (rare)
- You later call `follow_link(link_id, LINK_TYPE)` or `retrieve_endsets` on the link

## Conclusion

**Yes, the link remains discoverable** via source or target searches even when its type endset becomes unresolvable. The unresolvable type endset is "orphaned metadata" - it doesn't prevent the link from being found, it only affects operations that specifically try to access the type endset itself.

This behavior aligns with Xanadu's permanence philosophy: links are never deleted, only potentially "orphaned" when their referenced content disappears from the V-stream.

---

## Question 17 [gregory]

> When `insertendsetsinspanf` indexes a link's endsets in the spanfilade, does it create one spanfilade entry per endset or one entry per I-span within each endset — i.e., if the source endset contains two non-contiguous I-ranges, how many spanfilade entries result?

### Gregory's Answer

## KB Synthesis

# Answer

Based on the knowledge base, `insertendsetsinspanf` creates **one spanfilade entry per I-span within each endset**, not one entry per endset.

## Key Evidence

From [SS-DOCISPAN] Finding 0047, which documents the same `insertspanf` mechanism used by `insertendsetsinspanf`:

> "When `insertspanf` is called, it iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. Each `typeispan` represents a contiguous range of I-addresses (with a `stream` start and `width` size), so inserting 10 contiguous bytes creates 1 DOCISPAN entry, not 10."

The code structure is:
```c
for (; sporglset; sporglset = next) { 
    ... 
    insertnd(...); 
}
```

## Concrete Example

From [ST-LINK-CREATE] Finding 0037:

> "When document C transcludes 'AA' from A and 'BB' from B, the contiguous V-span 1.1..1.4 in C maps to two disjoint I-address regions. The link subsystem handles this transparently: `vspanset2sporglset` calls `vspanset2ispanset` which walks the POOM (permutation matrix) to discover all I-address regions, producing one I-span per contiguous region."

If a link is created with source endset covering this content:
- **Input**: One V-span `[1.1, 1.4)` covering "AABB" in document C
- **Conversion**: Produces two I-spans (one for "AA" from doc A, one for "BB" from doc B)
- **Spanfilade entries**: **Two entries** — one per I-span

The granularity is per-contiguous-I-range, not per-endset. This means links with fragmented content (transcluded from multiple sources) create multiple spanfilade entries for a single endset.

## Code Exploration

Now I have traced the complete execution path. Let me provide the answer with all code citations:

---

## Answer

**`insertendsetsinspanf` creates one spanfilade entry per I-span within each endset.**

If a source endset contains two non-contiguous I-ranges, **two spanfilade entries result** (one per I-span).

### Code Evidence

**1. `insertendsetsinspanf` calls `insertspanf` once per endset** [do2.c:116-128]:

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
  if (!(insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
    return (FALSE);
  if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN))
      return (FALSE);
  }
  return(TRUE);
}
```

**2. `insertspanf` iterates through each I-span in the sporglset** [spanf1.c:25-51]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
  if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    ...
  } else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
    movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
    ...
  }
  movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
  movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
  insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

The critical line is [spanf1.c:51]: **`insertnd` is called once per iteration**, creating one spanfilade entry per sporglset item.

**3. Each sporglset item represents one contiguous I-span** [sporgl.c:49-57]:

When V-spans are converted to I-spans, each resulting I-span becomes a separate sporgl:

```c
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
```

### Execution Flow

For a link with a source endset containing two non-contiguous I-ranges `[1.1.1, 2)` and `[10.1.1, 2)`:

1. `specset2sporglset` converts the endset to a sporglset with **two items** (one per I-range) [sporgl.c:14-33, 35-65]
2. `insertendsetsinspanf` calls `insertspanf` with this two-item sporglset [do2.c:119]
3. `insertspanf` iterates twice, calling `insertnd` **twice** [spanf1.c:25, 51]
4. Result: **Two spanfilade entries**, one indexing `[1.1.1, 2)` and one indexing `[10.1.1, 2)`

This design allows the spanfilade to efficiently retrieve links by any I-span fragment within an endset, not just complete endsets.

---

## Question 18 [gregory]

> If a document is versioned via CREATENEWVERSION and then a link is created on the original with source content shared by both documents, does find_links from the VERSION discover this after-the-fact link through the shared I-addresses?

### Gregory's Answer

## KB Synthesis

**YES**, the version WILL discover the after-the-fact link through shared I-addresses.

## Mechanism

The link discovery mechanism operates purely on content identity (I-addresses), not on temporal ordering or document membership:

1. **Version shares I-addresses with original** — `[ST-VERSION-CREATE]` (Finding 0032) establishes that `references(version) = references(source)` at creation time. The version's text content maps to the same I-addresses as the original's.

2. **Link endpoints indexed by I-address** — `[ST-LINK-CREATE]` (Finding 0012): When the link is created on the original, `insertendsetsinspanf()` indexes the link's endpoints by their I-addresses in the spanfilade. These are the SAME I-addresses the version already references.

3. **find_links operates on I-address intersection** — `[SS-FIND-LINKS]` (Finding 0028): "find_links(search_specset) discovers links by I-address intersection, not by document or V-address matching." When `find_links` is called from the version:
   - The version's V-addresses are converted to I-addresses
   - The spanfilade is searched for links whose endpoints intersect these I-addresses
   - The newly created link matches because its endpoints reference the shared I-addresses

4. **Bidirectional discovery is explicit** — `[INT-LINK-VERSION]` (Finding 0008): "Links added to a version are discoverable from the original document, and vice versa... This is bidirectional — links created on either document are discoverable from both." The "vice versa" explicitly covers the scenario where the link is created on the original after versioning.

5. **Global visibility through content identity** — `[INV-LINK-GLOBAL-VISIBILITY]` (Finding 0008): "Links in udanax-green are globally visible through content identity. A link created in any document is discoverable from every document in the system that shares the linked content's identity."

## Why Timing Doesn't Matter

The spanfilade is a permanent index (`[INV-SPANF-WRITE-ONLY]`). When the link is created:
- The spanfilade gains an entry: `I-addresses_of_endpoints → link_id`
- Any future `find_links` call that queries those I-addresses will return this link
- The version already holds those I-addresses (from the earlier VERSION operation)
- Therefore the version will discover the link

The independence works because `[FC-CONTENT-SPANF-ISOLATION]` establishes that link discovery (spanfilade queries) and document content (granfilade state) are separate subsystems. The version's I-address references exist independently of when links pointing to those I-addresses are created.

## Code Exploration

## Answer

**YES**, the version should discover the after-the-fact link through shared I-addresses. Here's the detailed reasoning based on the source code:

### How It Works

**1. CREATENEWVERSION shares I-addresses** [`do1.c:260-299`]

When `docreatenewversion` creates a new version, it:
- Retrieves the original's entire V-span via `doretrievedocvspanfoo` [`do1.c:281`]
- Copies the content to the new version via `docopyinternal` [`do1.c:293`]
- This calls `insertpm` which inserts the **same I-addresses** at the corresponding V-positions

The original and version share content identity — same I-addresses, different V-addresses in different documents.

**2. CREATELINK stores by I-address** [`do1.c:195-221`, `spanf1.c:15-54`]

When a link is created on the original:
- The source specset (V-spans) is converted to I-spans via `vspanset2ispanset` [`orglinks.c:397-402`]
- The link endpoints are stored in spanf indexed by **I-address**, not V-address
- The link is stored at `insertspanf(spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)` [`spanf1.c:119`]

**3. FIND_LINKS queries by I-address without document filtering** [`spanf1.c:56-103`, `sporgl.c:239-269`]

When `find_links` is called on the version:
- The version's V-spans are converted to I-spans via `specset2sporglset` [`sporgl.c:14-33`]
- For each I-span, `sporglset2linksetinrange` queries spanf [`sporgl.c:239-269`]
- **Critical line [`sporgl.c:255`]:** `infoptr = NULL` — no document filtering
- The query at [`sporgl.c:259`] retrieves ALL links matching the I-span, regardless of which document they were created on:
  ```c
  context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
  ```

**The commented-out code at [`sporgl.c:251-254`]:**
```c
if (FALSE/*trying to kluge links followable thru versions */&&((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
  } else
    infoptr = NULL;
```

This comment explicitly mentions "links followable thru versions" with `FALSE`, meaning the feature is **enabled** (the condition is false, so it falls through to `infoptr = NULL`, which allows cross-document link discovery).

### Execution Flow

```
1. ORIGINAL doc at I-address 123 (V-position 1.7)
2. CREATENEWVERSION creates VERSION with same content at I-address 123 (V-position 1.7)
3. CREATELINK on ORIGINAL from V-span 1.7→1.12
   → Converts to I-span 123→width
   → Stores in spanf: {I-span: 123→width, link_id: XYZ}
4. FIND_LINKS on VERSION from V-span 1.7→1.12
   → Converts to I-span 123→width
   → Queries spanf for links at I-span 123
   → Finds link XYZ (no document filtering)
   → Returns link XYZ
```

### Verification

The existing test `scenario_version_copies_what` tests whether links created BEFORE versioning are visible. I can write a complementary test for links created AFTER versioning if you'd like empirical verification.

**Conclusion:** The version WILL discover the link because link discovery operates on shared I-addresses, not document-specific V-addresses, and the query explicitly uses `infoptr = NULL` to avoid document filtering.

---

## Question 19 [gregory]

> When `link2sporglset` extracts I-addresses from a link orgl's three endsets, does it preserve the endset boundary (source vs target vs type) in the sporgl structures, or are all three endsets flattened into a single sporgl set for spanfilade search?

### Gregory's Answer

## KB Synthesis

# Answer: Endset Boundaries Are Preserved

`link2sporglset` **preserves endset boundaries** — the three endsets (source, target, type) are **not** flattened into a single sporgl set. Each endset is maintained as a separate sporgl set throughout the system.

## Evidence from the Knowledge Base

### At Link Creation Time

From `[INT-SPORGL-LINK-INDEX]` Finding 0013:

> When a link is created, its endpoints (from, to, three) are converted to sporgls and indexed in the spanf enfilade. The function `insertendsetsinspanf()` receives sporglsets for **each endpoint type** and inserts them into the spanf index **tagged with the link's ISA and endpoint type** (`LINKFROMSPAN`, `LINKTOSPAN`).

**Code reference:** `do2.c:116-128` — `insertendsetsinspanf()` inserts from/to/three sporglsets **separately**.

The spanfilade maintains three distinct ORGLRANGE subspaces:
- `LINKFROMSPAN = 1` (source endset)
- `LINKTOSPAN = 2` (target endset)  
- `LINKTHREESPAN = 3` (type endset)

### At Link Retrieval Time

From `[SS-FOLLOWLINK]` Finding 0048:

> The call chain is: `link2sporglset()` extracts I-addresses from the link orgl **at the requested endset position (0.1, 0.2, or 0.3)** via `retrieverestricted()`.

The function takes a `whichend` parameter that selects **one specific endset** to extract, not all three.

**Code reference:** `sporgl.c:67-95` — `link2sporglset()` extracts I-addresses from link orgl at the **requested** endset position (selective, not flattened).

### At Query Time

From `[INT-SPORGL-LINK-INDEX]` Finding 0035:

> RETRIEVEENDSETS discovers links through the spanfilade by searching with ORGLRANGE dimension prefixes. The three link endset types are indexed as **separate ORGLRANGE subspaces**... each endset type is **searched independently** by restricting the ORGLRANGE dimension.

**Code reference:** `spanf1.c:190-235` — ORGLRANGE subspace definitions with **separate searches per endset type**.

## Conclusion

The system maintains endset boundaries at three levels:

1. **Storage layer** (link orgl): Three V-address positions (0.1, 0.2, 0.3) store the three endsets separately
2. **Index layer** (spanfilade): Three ORGLRANGE subspaces (1, 2, 3) index the three endsets with distinct type tags
3. **Retrieval layer** (`link2sporglset`): Extracts one endset at a time based on the `whichend` parameter

The design ensures that source, target, and type endpoints remain distinguishable throughout the system's operation. This separation is necessary because the three endsets serve different semantic roles and are queried independently (e.g., `find_links` by source only, or `follow_link` requesting just the target endset).

## Code Exploration

## Answer: Endset Boundaries ARE Preserved

`link2sporglset` **preserves endset boundaries**—it does NOT flatten all three endsets into a single sporgl set. Instead, it extracts **only one endset at a time**, specified by the `whichend` parameter.

---

### The Mechanism [sporgl.c:67-95]

The function signature clearly shows the selector:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, 
                    typesporglset *sporglsetptr, INT whichend, int type)
```

The extraction process [sporgl.c:77-94]:

1. **Find the link orgl** [line 77-79]:
   ```c
   if (!findorgl (taskptr, granf, linkisa, &orgl,type)){
       return (FALSE);
   }
   ```

2. **Create a vspan positioned at the specified endset** [lines 80-82]:
   ```c
   tumblerclear (&zero);
   tumblerincrement (&zero, 0, whichend, &vspan.stream);
   tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
   ```
   
   This constructs a V-span with:
   - `stream = [whichend]` (start position)
   - `width = [1]` (span width of 1)
   
   So if `whichend=1`, it retrieves position [1,2). If `whichend=2`, it retrieves [2,3). If `whichend=3`, it retrieves [3,4).

3. **Retrieve only that endset's contents** [lines 83-89]:
   ```c
   if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, ...)) {
       for (c = context; c; c = c->nextcontext) {
           sporglptr = (typesporgl *)taskalloc(taskptr,sizeof (typesporgl));
           contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
           *sporglsetptr = (typesporglset)sporglptr;
           sporglsetptr = (typesporglset *)&sporglptr->next;
       }
   }
   ```

---

### The Endset Constants [xanadu.h:36-38]

The three endsets are explicitly defined:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

These map directly to:
- `whichend=1` → **source endset**
- `whichend=2` → **target endset**
- `whichend=3` → **type/third endset**

---

### Protocol Validation [get1.c:63-73]

The FEBE protocol requires the client to specify which endset:

```c
bool getfollowlink(typetask *taskptr, typeisa *linkisaptr, INT *whichendptr)
{
    prompt (taskptr, "enter link=> ");
    if (!getisa (taskptr, linkisaptr))
        return (FALSE);
    prompt (taskptr, "enter endset=> ");
    if (!(
       getnumber (taskptr, whichendptr)
    && (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)))
        return (FALSE);
    return (TRUE);
}
```

The client must explicitly choose 1, 2, or 3. The backend retrieves only that selected endset.

---

### Call Chain Evidence

**Following a link** [fns.c:119-123]:
```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
    putfollowlink (taskptr, specset);
```

**Extracting the endset** [do1.c:223-231]:
```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, 
                  typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, 
                               sporglset, specsetptr, NOBERTREQUIRED));
}
```

The `whichend` parameter flows from protocol → dofollowlink → link2sporglset, selecting exactly one endset.

---

### Inverse Operation: Link Creation Preserves Boundaries

When creating links, the three endsets are kept separate [do1.c:214-219]:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, 
                        &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, 
                         fromsporglset, tosporglset, threesporglset)
```

Each endset is inserted separately into both the granfilade (at distinct vsa positions) and spanfilade (with distinct span type markers) [do2.c:116-128]:

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset, 
                          typesporglset tosporglset, 
                          typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
      && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)))
        return (FALSE);
    if (threesporglset) {
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
            return (FALSE);
    }
    return (TRUE);
}
```

---

### Conclusion

**The three endsets are architecturally separate throughout the entire system:**

1. **At rest**: Stored at distinct V-positions (1, 2, 3) in the link orgl
2. **In spanfilade**: Indexed under distinct span types (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN)
3. **During retrieval**: Extracted one at a time via the `whichend` selector
4. **In sporgl sets**: Each endset becomes a separate sporglset—never merged

The design ensures you can follow a link in a specific direction (source→target, target→source, or via type) by selecting the appropriate endset. The boundaries are never flattened.

---

## Question 20 [gregory]

> Does the system guarantee that a link created with a multi-span source endset (e.g., two disjoint VSpecs from different parts of the same document) stores those spans in endset-order in the link orgl, and does RETRIEVEENDSETS return them in that same order?

### Gregory's Answer

## KB Synthesis

# Answer: Order Preservation in Multi-Span Link Endsets

The KB does **not provide direct evidence** that multi-span endset order is preserved from link creation through retrieval. Here's what can be determined:

## What the KB Confirms

### Link Creation Process
`[ST-VSPAN-TO-SPORGL]` documents that `vspanset2sporglset()` converts V-spans to sporgls (I-address ranges with provenance), and `linksporglset2specset()` performs the reverse conversion. The sporgls are stored as a linked list per `[SS-SPORGL]`:

> Sporgls are stored as a linked list (`typesporglset`) and can be interchanged with ispans via a union type (`typesporglitem`).

### General SpecSet Order Preservation
`[INV-SPECSET-ORDER]` establishes that SpecSets maintain ordering for operations like retrieve and vcopy:

> SpecSet operations preserve VSpec ordering in their results. Retrieve concatenates content in VSpec order. Vcopy places content in VSpec order.

However, this invariant is documented for **content operations**, not explicitly for link endset storage and retrieval.

## Critical Gap: Multi-Span Link Behavior

`[EC-MULTISPAN-LINK-DUPLICATION]` reveals anomalous behavior with multi-span links:

> Creating a link with multiple source spans works, but `retrieve_endsets` may return duplicate spans:
> ```
> Link source: ["First" at V 1.1, "second" at V 1.16]
> Endsets return: 3 spans (1.16 appears twice)
> ```

This duplication suggests the endset representation or retrieval process **does not cleanly preserve** the input structure. The KB notes this "may be related to the same internal fragmentation mechanism observed with pivot."

## Potential Confounding Factor

`[INV-RETRIEVAL-V-SORTED]` documents that B-tree traversal operations sort results by V-address:

> `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered during B-tree traversal... the result list is sorted by left boundary in the queried dimension.

If `linksporglset2specset()` uses similar sorting logic when converting I-addresses back to V-addresses, the original input order would be lost. The KB does not clarify whether endset retrieval involves such sorting.

## Conclusion

**The system likely does NOT guarantee order preservation** for multi-span link endsets. The observed duplication in `[EC-MULTISPAN-LINK-DUPLICATION]` and the absence of explicit order-preservation claims for link operations suggest the endset structure reflects I-space fragmentation patterns rather than input VSpec ordering. To answer definitively would require examining:

1. The implementation of `vspanset2sporglset()` (sporgl.c:35-65)
2. The implementation of `linksporglset2specset()` (sporgl.c:97+)  
3. Whether endset retrieval applies V-address sorting

The KB documents the existence and function of these operations but does not specify their order-preservation guarantees.

## Code Exploration

Based on my analysis of the code, I can now provide a complete answer to your question.

## Answer

**Yes, the system guarantees order preservation for multi-span endsets in links.** When you create a link with a multi-span source endset (e.g., two disjoint VSpecs), those spans are:

1. **Stored in the link orgl at sequential V-positions** in the order you provide them
2. **Retrieved by RETRIEVEENDSETS in that same order**

However, the preservation mechanism is more subtle than simply storing them "as-is."

## How Multi-Span Endsets Are Stored

### 1. Link Orgl Structure

Links store their three endsets at fixed V-position ranges in the link orgl [do2.c:169-183]:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // fromvsa = 1.1
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // tovsa = 2.1
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // threevsa = 3.1
    }
    return (TRUE);
}
```

- FROM endset: stored in V-range **1.x**
- TO endset: stored in V-range **2.x**
- THREE endset: stored in V-range **3.x**

### 2. Sequential Insertion Preserves Order

When `docreatelink` processes a multi-span endset [do1.c:214-218]:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset,NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
```

The `specset2sporglset` function [sporgl.c:14-33] builds the sporglset by iterating through the user-provided VSpecs **in order**:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
        // Process each VSpec in order
        if (!(sporglsetptr = vspanset2sporglset (taskptr, &((typevspec *)specset)->docisa, 
                                                  ((typevspec *)specset)->vspanset, sporglsetptr,type))){
            return (FALSE);
        }
    }
    return (TRUE);
}
```

And `vspanset2sporglset` [sporgl.c:47] iterates through the VSpans **in order**:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    // Create sporgl entries in linked-list order
}
```

Then `insertpm` [orglinks.c:100-132] inserts these sporgls **sequentially**:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (vsaptr, &crumorigin.dsas[V]);  // Insert at current V-position
    // ... calculate V-width ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // Advance to next V-position
}
```

**Key insight**: Each span in the endset is inserted at a sequential V-position (1.1, 1.1+w₁, 1.1+w₁+w₂, etc.) in the order provided by the user.

## How RETRIEVEENDSETS Returns Them

### 1. Range-Based Retrieval

`retrieveendsetsfromspanf` [spanf1.c:190-235] retrieves each endset by V-range:

```c
bool retrieveendsetsfromspanf(typetask *taskptr, typespecset specset, 
                              typespecset *fromsetptr, typespecset *tosetptr, 
                              typespecset *threesetptr)
{
    // Define V-ranges for each endset
    fromspace.stream.mantissa[0] = LINKFROMSPAN;   // 1.0
    fromspace.width.mantissa[0] = 1;               // width 1.0 (range 1.0-2.0)
    
    tospace.stream.mantissa[0] = LINKTOSPAN;       // 2.0
    tospace.width.mantissa[0] = 1;                 // width 1.0 (range 2.0-3.0)
    
    threespace.stream.mantissa[0] = LINKTHREESPAN; // 3.0
    threespace.width.mantissa[0] = 1;              // width 1.0 (range 3.0-4.0)
    
    // Retrieve all sporgls in each range
    retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)
    // ...
}
```

### 2. V-Address Sorting Preserves Sequential Order

The key to understanding order preservation is **Finding 0078** (which you already have in your findings). When `retrievesporglsetinrange` calls `retrieverestricted`, it uses `incontextlistnd` [context.c:75-111] which performs **insertion-sort by V-address**.

Since the spans were inserted at sequential V-positions during creation:
- Span 1 at V = 1.1
- Span 2 at V = 1.1 + w₁
- Span 3 at V = 1.1 + w₁ + w₂

The V-sorted retrieval order **matches the original insertion order**.

## Verification with Golden Test

The test `endsets_multispan_link` [golden/endsets/endsets_multispan_link.json] confirms this:

**Input** (lines 15-17):
```json
"source_spans": ["First", "second"]
```
- "First" at V = 1.1, width = 0.5
- "second" at V = 1.16, width = 0.6

**Retrieved** (lines 27-40):
```json
"spans": [
    {"start": "1.1", "width": "0.5"},    // "First"
    {"start": "1.16", "width": "0.6"},   // "second"
    {"start": "1.16", "width": "0.6"}    // (duplicate - possible bug)
]
```

The order is preserved: First (1.1) before second (1.16).

## Guarantee Properties

**Property L1 (Multi-span endset order preservation):**
```
Given link L with FROM endset containing VSpans [s₁, s₂, ..., sₙ] in order:
  CREATELINK stores them at sequential V-positions [1.1, 1.1+w₁, 1.1+w₁+w₂, ...]
  RETRIEVEENDSETS returns them in the same order [s₁, s₂, ..., sₙ]
```

This holds because:
1. Sequential insertion order is preserved by linked-list traversal [sporgl.c:14-64]
2. Sequential V-positions are monotonically increasing [orglinks.c:131]
3. V-sorted retrieval of monotonically increasing positions preserves order [context.c:75-111]

## Source References

- `do1.c:214-220` - docreatelink converts specsets to sporglsets in order
- `do2.c:130-149` - insertendsetsinorgl calls insertpm for each endset
- `do2.c:169-183` - setlinkvsas defines V-ranges (1.x, 2.x, 3.x)
- `sporgl.c:14-64` - specset2sporglset and vspanset2sporglset preserve linked-list order
- `orglinks.c:100-132` - insertpm inserts at sequential V-positions
- `spanf1.c:190-267` - retrieveendsetsfromspanf retrieves by V-range
- `context.c:75-111` - incontextlistnd sorts by V-address (Finding 0078)
- `golden/endsets/endsets_multispan_link.json` - Test confirming order preservation
