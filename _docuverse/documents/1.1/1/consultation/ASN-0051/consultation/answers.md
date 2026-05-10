# Consultation Answers — Link Survivability

**Inquiry:** What guarantees does the system provide about links across state changes? What survives, what changes, and what can a link holder rely on?
**Date:** 2026-03-20 19:19
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content that a link points to is edited — words inserted before or after the linked passage — must the link continue to address exactly the same content it originally addressed?

### Nelson's Answer

# Yes — absolutely and by design.

This is one of the most fundamental properties of Xanadu links. I designed them specifically so that editing operations — insertions, deletions, rearrangements — do not disturb existing links.

## The Mechanism: Links Attach to Bytes, Not Positions

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

A link is a strap binding bytes together. If you insert words before, after, or around the linked passage, the strap stays attached to the same bytes. The visual positions shift — of course they do — but the link doesn't care about visual positions. It cares about *which bytes*.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## Why This Works: Two Address Spaces

The architecture has two separate address spaces:

- **Istream** (permanent): where content lives forever. Every byte gets a permanent I-address at creation. That address never changes.
- **Vstream** (ephemeral): the document's current arrangement. V-addresses shift with every edit.

Links point to **Istream addresses**. Editing changes **Vstream addresses**. The two are independent. When you insert a word before a linked passage, the V-addresses after the insertion point all shift — but the I-addresses of the linked bytes remain exactly as they were.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The user and front end work with V-addresses (intuitive positions). The link system works with I-addresses (permanent identity). This separation is the whole point.

## The Survivability Guarantee

I stated this explicitly as a system property:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

Note the boundary condition: links survive as long as *any* bytes remain at each end. You could delete most of a linked passage and the link would still hold onto whatever bytes remain. Only the complete deletion of all bytes at one end breaks the connection.

> "This also works for alternative versions in which part of each end has survived." [LM 4/42]

## Why This Matters

Without this property, Xanadu's entire vision collapses. If editing broke links, then:

- Every edit would damage the web of connections others had built to your content
- Published documents could never be revised without destroying scholarship built upon them
- The "ongoing braid" of document evolution would shred the literature's connective tissue

The whole point of the system is that **literature is interconnected** and those connections must survive the continuous editing that living documents require. Span-based, content-addressed linking is how I solved that.

---

## Question 2 [nelson]

> If a linked passage is deleted from a document, what must the system guarantee about the link itself — does it persist, become invalid, or enter some other state?

### Nelson's Answer

## Link Persistence After Content Deletion

The system guarantees that the link **persists**. This follows from two architectural properties working together: links attach to Istream (permanent) addresses, and deletion only affects Vstream (current arrangement).

### Links Attach to Bytes, Not Positions

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

The "strap between bytes" metaphor is key. The link grips the bytes themselves — identified by their permanent Istream addresses — not the positions those bytes happen to occupy in a document's current arrangement.

### Deletion Does Not Destroy Bytes

DELETE in Xanadu removes content from Vstream only. The Istream content is untouched:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes enter a state Nelson describes as "not currently addressable" — they vanish from the document's current view but remain permanently in Istream storage. They also survive in previous versions and in any other documents that transclude them.

### Therefore the Link Survives

Since the link's endset points to Istream addresses, and those addresses are permanent, the link retains valid targets even after Vstream deletion. The survivability guarantee from [LM 4/43] states:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

Because Istream is append-only and bytes are never destroyed, "something is left at each end" is always structurally true. The deleted bytes still exist — they are merely removed from the current arrangement.

### What the Reader Experiences

Nelson explicitly addresses the case where a document is updated and a reader follows an old link:

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

That final clause — "if it's still there" — acknowledges the case where the linked passage has been deleted from the current version. The link itself remains valid; the front end must decide how to present it. Options include:

1. Show the content in the **previous version** where it still exists (historical backtrack)
2. Show the content at its **Istream home** (permanent address)
3. Show it in **other documents** that transclude it
4. Indicate that the passage was removed from the current version but remains accessible

### Summary

| Aspect | State After Deletion |
|--------|---------------------|
| **The link itself** | Persists — it is a first-class object at its own address |
| **The link's endset targets** | Still valid — point to permanent Istream addresses |
| **The bytes in Istream** | Unchanged — append-only, never destroyed |
| **The bytes in Vstream** | Removed from current version's arrangement |
| **Previous versions** | Still contain the passage |
| **Other transclusions** | Unaffected — still show the content |

The link neither becomes invalid nor enters a degraded state. It continues to function exactly as before, because its targets — Istream bytes — are permanent. What changes is only the current document's Vstream arrangement, which is the one thing the link does *not* depend on.

---

## Question 3 [nelson]

> Must a link created against one version of a document remain meaningful when the document reaches a later version, or is a link bound to the version in which it was made?

### Nelson's Answer

## Links Are Not Bound to Their Version

A link made against one version of a document remains meaningful across all versions. This is not a secondary feature but a direct consequence of the architecture, and Nelson states the principle explicitly:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

### Why This Works: Istream Attachment

Links attach to **Istream addresses** (permanent content identity), not **Vstream addresses** (ephemeral arrangement positions). Since different versions of a document are different Vstream arrangements over shared Istream content, a link to specific bytes works wherever those bytes appear — in any version, past or future.

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The link is a "strap between bytes." The bytes have permanent I-addresses. Versions rearrange which bytes appear and where, but the bytes themselves don't change identity. The strap holds.

### The Correspondence Mechanism

What makes cross-version link following possible is **correspondence** — the system's ability to identify which parts of different versions share the same Istream origin:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The FEBE operation `SHOWRELATIONOF2VERSIONS` computes this:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

Correspondence is structural — it falls out of shared I-addresses, not from metadata or tracking. If two V-positions in different versions map to the same I-address, they correspond. The system can therefore trace a link from version 1 to the "same place" in version 5.

### The Supersession Case

Nelson explicitly addresses what happens when a document is updated and someone follows a link made to the old version:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

Note the caveat: "if it's still there." If the newer version deleted the bytes the link pointed to, there is no corresponding content to follow to. The link still resolves against the old version (which must remain on the network), but it cannot "reach through" to content that no longer exists in the new version.

### The Condition for Cross-Version Validity

A link remains meaningful across versions **if any of the bytes it references survive** in the target version. The condition is the same as for editing survivability:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

This applies across versions because versions are just different arrangements of the same content pool. The link doesn't know or care which version it's being resolved against — it only cares whether the referenced I-addresses appear in that version's V-stream.

### Summary

| Question | Answer |
|----------|--------|
| Is a link bound to its version? | **No.** |
| Can it follow to other versions? | **Yes**, via correspondence (shared I-addresses). |
| Does this require explicit action? | **No** — it's structural, computed from the addresses. |
| When does it fail? | When the linked bytes are absent from the target version. |
| Nelson's principle | "A link to one version is a link to all versions." [LM 2/26] |

---

## Question 4 [nelson]

> Can the creator of a link ever destroy it, or does the system guarantee that once a link exists it is permanent in the same way that content is permanent?

### Nelson's Answer

## Can a Link Creator Destroy a Link?

**Yes, the owner can delete a link from their document's current version. No, the link is not truly destroyed.** Links follow exactly the same non-destruction semantics as content bytes.

### The "Deleted Links" State

Nelson explicitly includes "DELETED LINKS" as a valid document state, parallel to deleted bytes:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This tells us three things:

1. **Links can be deleted** — removed from the document's current Vstream arrangement
2. **Deleted links persist** — they await "historical backtrack functions," meaning they remain in Istream
3. **Deleted links may survive in other versions** — if someone versioned your document before you deleted the link, that version still contains it

### Who Can Delete

Only the owner of the link's home document:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

This means: if you created a link in your document pointing to someone else's content, only you can delete it. The target document's author cannot delete your link — though they could delete the content it points to, potentially breaking it.

### Why Links Are Never Truly Destroyed

Links are stored in Istream alongside content bytes. The only entities actually stored in tumbler-space are "content bytes and links" [LM 4/23]. Since Istream is append-only — "User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" [LM 2/14] — deleted links remain in permanent storage just as deleted bytes do.

The parallel is exact:

| | Content Bytes | Links |
|---|---|---|
| **Deletion removes from** | Vstream (current view) | Vstream (current view) |
| **Persists in** | Istream (permanent) | Istream (permanent) |
| **Recoverable via** | Historical backtrack | Historical backtrack |
| **Survives in** | Other versions | Other versions |

### The Published Document Complication

For published documents, there's an additional permanence layer. Published documents cannot be easily withdrawn:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

The owner can publish a superseding version without certain links, but "the former version must remain on the network. This is vital because of the links other users may have made to it" [LM 2/43]. So even if you "delete" a link from your published document by publishing a new version, the old version — containing the link — remains accessible.

### Summary

The system treats link deletion identically to content deletion: it is a **Vstream operation**, not an **Istream operation**. The link disappears from the document's current arrangement but remains permanently in storage, recoverable through historical backtrack, and potentially alive in other versions. Nelson's non-destruction guarantee — "without damaging the originals" [LM 2/45] — applies to links just as it applies to every other element in the docuverse.

---

## Question 5 [nelson]

> When a document is reorganized — passages reordered or moved to different positions — must links to those passages track the content rather than the location?

### Nelson's Answer

# Yes — Links Track Content, Not Location

This is one of the most emphatically stated design principles in Literary Machines. Links attach to **bytes** (Istream identity), not to **positions** (Vstream arrangement). When a document is reorganized, links follow the content wherever it moves.

## The Core Statement

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."
> — [LM 4/42]

The "strap between bytes" metaphor is precise: a strap fastened to specific bytes stays attached to those bytes regardless of where they are moved, reordered, or rearranged.

## Why This Works: The Two Address Spaces

The mechanism that makes this possible is the separation of Istream (permanent content identity) from Vstream (current arrangement):

- **Istream addresses are permanent.** Every byte has an immutable identity address that never changes.
- **Vstream addresses are ephemeral.** They represent the document's current arrangement and shift with every edit.
- **Links point to Istream.** Therefore they are unaffected by Vstream rearrangement.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."
> — [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this."
> — [LM 4/11]

The V-address (position) changes constantly during editing. The I-address (identity) never changes. Links reference identity, so they are immune to positional changes.

## What Links Survive

The survivability guarantee from [LM 4/43]:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

Specifically:

- **Rearrangements** — content moved to new positions: links follow
- **Insertions** — new content added around linked content: links unaffected
- **Deletions** — content removed: links survive if *any* bytes at each endset remain
- **Alternative versions** — content present in some versions but not others: links work wherever the bytes exist

Links break **only** when all bytes at one end are completely deleted — when there is literally nothing left for the "strap" to hold onto.

## The REARRANGE Operation Confirms This

The FEBE protocol includes an explicit REARRANGE operation:

> "Rearrange transposes two regions of text."
> — [LM 4/67]

This operation changes Vstream arrangement. It does not affect Istream content. Therefore it cannot break links. This is by design — the operation exists precisely because the architecture guarantees that reorganization is safe.

## Summary

The answer is unequivocal. Links **must** track content rather than location. This is not merely a desirable property but an architectural consequence of the Istream/Vstream separation. Links reference permanent content identity (I-addresses), not ephemeral arrangement positions (V-addresses). When you reorganize a document, you change only the Vstream mapping — the links, attached to Istream bytes, are structurally incapable of being affected.

---

## Question 6 [nelson]

> If two independent links point to the same passage and that passage is later split across two documents, must both links survive and continue to reach their original content?

### Nelson's Answer

# Yes. Both links must survive.

This follows directly from three interlocking properties Nelson specifies.

## 1. Links attach to bytes, not positions or documents

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The two links each hold I-addresses — permanent references to specific bytes in the append-only Istream. They do not reference a document, a Vstream position, or any arrangement that can change. They reference the bytes themselves.

## 2. Istream content is permanent

In Xanadu, bytes never move and never disappear. "Splitting a passage across two documents" means changing which documents' Vstreams reference those bytes — it does not alter, relocate, or destroy the bytes at their I-addresses.

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Since both links point to I-addresses, and I-addresses are permanent, the links' targets still exist regardless of how Vstream arrangements change.

## 3. Broken, discontiguous endsets are valid

After the split, the passage that was once contiguous in a single document's Vstream may now appear as fragments in two different documents' Vstreams. Nelson explicitly states this is fine:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

The endsets of both links may now span bytes scattered across multiple documents. This is a supported state, not an error.

## The survivability guarantee

Nelson states the condition under which links break:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

In Xanadu's append-only storage, the bytes are never destroyed — only rearranged in Vstream or removed from a particular version's view. Since all the original bytes still exist at their I-addresses, there is always "something left at each end." Both links survive unconditionally.

## Independence of the two links

The two links are independent objects at their own addresses, owned by their respective creators:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Neither link's survival depends on the other. Both point to the same I-addresses. Both survive for the same reason: their targets are permanent.

## What changes is the user experience, not the link validity

After the split, following either link may lead to content distributed across two documents rather than appearing in one. The front end must resolve which documents currently show those bytes in their Vstreams. But the link mechanism itself — the "strap between bytes" — remains intact. The system can always locate the bytes because I-addresses are permanent and globally unique.

## Summary

Both links **must** survive. This is not a special case requiring special handling — it is the normal operation of a system where links attach to permanent byte identities (Istream), not to ephemeral arrangements (Vstream). The passage may scatter across any number of documents; the links follow the bytes, not the documents.

---

## Question 7 [nelson]

> What can a link holder rely on about the identity of the endpoints — must the system guarantee that the content at each end is exactly what was there when the link was created, or only that the addresses remain valid?

### Nelson's Answer

## What a Link Holder Can Rely On: Content Identity at Endpoints

The short answer: **both**. The system guarantees that addresses remain valid AND that the content at those addresses is exactly what was there when the link was created. But there are important nuances about partial survival and the absence of cryptographic proof.

---

### The Core Guarantee: Istream Immutability

Links point to **Istream addresses** — the permanent identity space where content lives forever. Istream is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content at an Istream address **never changes**. This is not a policy — it is the architectural foundation. There is no operation in the FEBE protocol that overwrites Istream content. INSERT appends new bytes to Istream. DELETE removes content from Vstream (the current arrangement) but leaves Istream untouched:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Therefore, the bytes referenced by a link's endsets at creation time are **guaranteed to be the same bytes** at any future time. The content is immutable at the address level.

---

### Links Attach to Bytes, Not Positions

Nelson is emphatic that links are "straps between bytes," not pointers to positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Because the link is attached to the bytes themselves (via their permanent I-addresses), and those bytes never change, the link holder can rely on the content identity at each endpoint being exactly what it was at creation.

---

### The Partial Survival Nuance

While the **bytes** never change, the **span** a link covers may shrink. If some bytes in an endset are removed from the current Vstream arrangement, the link survives on whatever bytes remain:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The visual annotation on page 4/43 makes the condition explicit:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

So a link holder can rely on this: every byte the link still touches is **identical** to what was there at creation. But the link may now touch **fewer** bytes than it originally did. The surviving content is exact; the coverage may have narrowed.

---

### What About Complete Deletion?

If ALL bytes at one end are removed from the current Vstream, the link loses practical navigability in that version. However, the I-addresses remain valid — those bytes still exist in Istream. The delete-semantics design intent confirms:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The link's endset addresses don't become invalid. The content is still there in Istream. But the link may not be discoverable through normal Vstream navigation in the current version. Previous versions and other documents that transclude the same content still provide paths to those bytes.

---

### No Cryptographic Verification

The guarantee is **architectural and contractual**, not cryptographic. Nelson explicitly acknowledges the absence of technical verification:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

The system relies on the Storage Vendor franchise to faithfully preserve content. If a vendor is compromised or dishonest, there is no cryptographic backstop to prove content has been tampered with. The architectural design (append-only Istream) makes tampering structurally unnecessary, but does not make it technically detectable.

---

### Summary

| Aspect | Guarantee |
|--------|-----------|
| **Address validity** | Permanent. Tumbler addresses never expire or get reassigned. |
| **Content identity** | Exact. Istream is immutable; bytes at an I-address never change. |
| **Span coverage** | May shrink. If some bytes leave the Vstream, the link survives on the remainder. |
| **Vstream context** | Not guaranteed. The document arrangement around the linked bytes may change. |
| **Cryptographic proof** | None. Trust is contractual (Storage Vendor franchise), not mathematical. |

The link holder can rely on the strongest possible content guarantee short of cryptographic verification: the system's fundamental architecture makes it impossible to change content at an I-address through any defined operation. The bytes the link was created against are the bytes it will always find. What may change is how many of those bytes remain visible in the current version of the document — but those that remain are exact.

---

## Question 8 [nelson]

> Must the system preserve the directionality and endpoint ordering of a link across all state changes, or can editing operations ever alter which end is the source and which is the target?

### Nelson's Answer

## Link Directionality Is Fixed at Creation and Immutable

The system **must** preserve the directionality and endpoint ordering of a link across all state changes. No editing operation can alter which end is the source and which is the target.

### The Structural Argument

A link's three endsets (from-set, to-set, type) are assigned at creation via MAKELINK and become permanent structural properties of the link. Nelson:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

The parenthetical — "what 'from' and 'to' mean depend on the specific case" — tells you that directionality carries **semantic weight** chosen by the link creator. A citation link goes from citing text to source. A comment link goes from commentary to subject. Swapping these would invert the meaning.

### No Operation Exists to Modify Links

Of the 17 FEBE commands in XU.87.1, none modifies a link's endsets after creation. The link operations are:

- **MAKELINK** — creates with fixed endsets
- **FINDLINKSFROMTOTHREE** — searches by endset constraints
- **RETRIEVEENDSETS** — returns endsets as stored
- **FINDNUMOFLINKSFROMTOTHREE** / **FINDNEXTNLINKSFROMTOTHREE** — pagination

There is no EDITLINK, MODIFYLINK, or SWAPENDSETS. The only way to "change" a link's directionality would be to delete it and create a new one — which produces a different link at a different address.

### Editing Operations Cannot Reach Link Structure

The editing operations (INSERT, DELETEVSPAN, REARRANGE, COPY, APPEND) operate on **document content** — bytes in the Vstream. Links point to **Istream addresses**, which are permanent. Nelson explicitly states:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Editing changes *where* bytes appear in the Vstream. It does not touch which bytes a link's from-set or to-set reference, let alone swap them.

### Survivability Preserves Endset Identity

Link survivability means links survive editing of the *content they point to*:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The surviving link retains its original endset assignment. If the from-set bytes survive and the to-set bytes survive, the link survives — with the from-set still "from" and the to-set still "to." Survivability is about **persistence**, not transformation.

### The One-Sided Link Confirms This

Nelson's discussion of one-sided links (like paragraph designators) reveals that endpoint ordering is a deliberate architectural choice, not something the system infers:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

He finds it "inane" to call a single endset "from" — because the from/to distinction carries real semantic meaning. If the system could freely swap endpoints, this complaint would be nonsensical.

### Summary

Link directionality is:
1. **Assigned at creation** — via MAKELINK's three endset parameters
2. **Semantically meaningful** — "what 'from' and 'to' mean depend on the specific case"
3. **Structurally immutable** — no FEBE operation modifies link endsets
4. **Unreachable by editing** — content editing changes Vstream, not link structure
5. **Preserved through survivability** — surviving links keep their original endpoint ordering

The system has no mechanism, accidental or deliberate, by which an editing operation could swap or alter which end is source and which is target.

---

## Question 9 [nelson]

> When new content is inserted at the exact boundary of a linked passage, must the system have a definite rule about whether the link expands to include the insertion or excludes it?

### Nelson's Answer

# Boundary Insertion and Link Endsets

The question answers itself once you understand what links actually attach to.

## Links Attach to Bytes, Not Positions

A link's endset is a set of I-address spans — permanent addresses in the Istream where specific bytes live forever:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" seizes specific bytes by their permanent identity. It does not seize a region of the document's current arrangement.

## New Content Gets New I-Addresses

When you INSERT, the new bytes are appended to the Istream and receive fresh, never-before-used I-addresses:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The INSERT operation changes the Vstream arrangement — "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66] — but creates entirely new Istream content. The linked bytes have not moved, changed, or been touched in any way.

## Therefore: No Ambiguity Exists

The link's endset still references exactly the same I-addresses it always did. The newly inserted bytes have *different* I-addresses. The link does not "know about" the insertion, and there is no mechanism by which it would expand.

This is not an edge case requiring a special rule. It is the natural consequence of the Istream/Vstream separation:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses shift. I-addresses don't. Links point to I-addresses. New content has new I-addresses. The link excludes the insertion — always, automatically, with no rule needed.

## The Strap Metaphor Is Exact

Think of it physically. You strap a set of beads together. Someone slides new beads onto the string next to your strapped group. Your strap hasn't changed — it still holds the same beads. The new beads are *adjacent* in the arrangement but *outside* the strap.

This is precisely the "strap between bytes" model. Survivability means the strap stays on whatever bytes remain:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Note: survive *insertions*. The link survives because it is unaffected. Insertion creates new bytes elsewhere in Istream; the linked bytes are untouched.

## If You Want the Link to Cover New Content

You would need to explicitly modify the link's endset to include the new I-addresses — or create a new link. The system does not silently expand endsets. That would violate the permanence of I-addresses and the definiteness of endsets.

## Summary

No boundary rule is needed because the architecture makes the answer structural. Links reference I-address spans. Insertions create new I-addresses. The two sets are disjoint by construction. The link excludes the insertion — not by convention, but by the geometry of the address space.

---

## Question 10 [nelson]

> If a link connects passages owned by two different users and one user's document undergoes extensive revision, what guarantee does the other user have that their end of the link remains intact and reachable?

### Nelson's Answer

# Link Integrity Across Ownership Boundaries Under Revision

The other user has a **layered set of guarantees** — architectural, structural, and contractual — that their end of the link remains intact and reachable even under extensive revision of the connected document.

## 1. Links Attach to Bytes, Not Positions

The foundational guarantee is architectural. Xanadu links are not pointers to positions in a document; they are "straps between bytes" identified by their permanent Istream addresses:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Editing operations — insertions, deletions, rearrangements — change the **Vstream** (the document's current arrangement). They do not alter the **Istream** (the permanent content store). Since links point to I-addresses, not V-addresses, editing literally cannot touch what links point to.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-addresses shift around. The I-addresses — and therefore the link endpoints — are immovable.

## 2. "Deletion" Does Not Destroy Content

Even if the revising user deletes the passage that one end of the link connects to, the bytes are not destroyed. DELETE in Xanadu removes content from the Vstream (current view) only:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist in Istream. The link still resolves to them. The content is recoverable through historical backtrack or through previous versions that still contain it.

## 3. The Survivability Condition

The explicit survivability guarantee from Nelson:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

This is the critical condition. A link breaks only when **all** bytes at one endset have been removed from every version and every transclusion. Given Istream's append-only nature, this effectively cannot happen — the bytes are permanent.

Nelson extends this to alternative versions:

> "This also works for alternative versions in which part of each end has survived." [LM 4/42]

## 4. Published Documents Cannot Be Withdrawn

The contractual layer reinforces the structural guarantee. Once published, a document stays published precisely **because** others have linked to it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The revising user may publish a new version, but the old version must remain:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

## 5. Links Reach Through to New Versions

If the revising user publishes a superseding version, the other user's link doesn't just cling to the old version — it can follow correspondence into the new one:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because versions share Istream content, the system can compute which parts of the new version correspond to the linked passage in the old. The reader following the link can be directed to the same content in the current version, if it still exists there.

## 6. Link Ownership Is Independent

The other user's link is **their property**, stored at their address. The revising user has no power over it:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

The revising user owns their document; the linking user owns their link. Neither can touch the other's property.

## Summary of Guarantees

| Threat | Protection |
|--------|------------|
| Content rearranged | Links point to I-addresses, unaffected by V-address changes |
| Content "deleted" | Bytes remain in Istream; link still resolves |
| Document revised with new version | Old version stays on network; link reaches through to new version |
| Document withdrawn | Not permitted for published documents (contractual) |
| Other user tries to remove the link | Cannot — link is owned by its creator, not the target's owner |

The guarantee is comprehensive: as long as the Xanadu system operates according to its design, the other user's link endpoint remains intact and reachable. The system was designed so that the web of interconnections — the structure of literature — cannot be destroyed by any individual participant's editing activity.

---

## Question 11 [gregory]

> When a link's source endset spans I-addresses `[i, i+5)` and a DELETE removes the content at `[i+2, i+4)` from the only document containing it, does `RETRIEVEENDSETS` for that link still return the full original I-span `[i, i+5)`, or does it return only the portions `[i, i+2)` and `[i+4, i+5)` that remain reachable through some POOM?

### Gregory's Answer

## KB Synthesis

## Answer

`RETRIEVEENDSETS` returns only the two surviving portions — not the full original span. Here is the reasoning:

**What the spanfilade retains (permanently)**

The link's source endset was indexed in the spanfilade when the link was created. That entry covers I-addresses `[i, i+5)`. Because the spanfilade is write-only [INV-SPANF-WRITE-ONLY], the entry persists after DELETE. The granfilade content bytes at those I-addresses also persist permanently [INV-IADDR-IMMUTABILITY].

**What DELETE actually changes**

DELETE operates only on the target document's POOM [ST-DELETE, FC-GRANF-ON-DELETE]. It calls `deletend`, which frees the bottom crums mapping I-addresses `[i+2, i+4)` to V-positions via `disown` + `subtreefree`. Since this was the *only* document containing those I-addresses, those I-addresses are now unreferenced in any POOM anywhere. The spanfilade entry is unchanged.

**The I-to-V conversion filter**

Both FOLLOWLINK and RETRIEVEENDSETS share the same I-to-V conversion path: `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` [INV-ITOV-FILTERING, SS-FOLLOWLINK]. At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for each I-address. When it returns NULL (no POOM entry), the I-address is **silently dropped** — no V-span is generated, no error is raised [SS-FOLLOWLINK, Finding 0048].

For the surviving portions `[i, i+2)` and `[i+4, i+5)`, the POOM still has valid mappings (those bytes were not deleted), so they convert successfully to V-spans.

**Result**

RETRIEVEENDSETS returns **two separate V-spans** corresponding to `[i, i+2)` and `[i+4, i+5)` — not the original single contiguous span. The deleted middle portion is silently absent. This is precisely the partial survival mechanism documented in [EC-LINK-PARTIAL-SURVIVAL]: "each I-span in a link endset independently tracks its content, so partial survival is possible."

The formal statement from [INV-ITOV-FILTERING] governs this: `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i`. Since no POOM in any document maps `[i+2, i+4)` to any V-position, no V-address for that range can appear in the result.

---

## Code Exploration

Now I have all the pieces. Let me compile the definitive answer.

---

## Answer

**`RETRIEVEENDSETS` returns only the surviving portions `[i, i+2)` and `[i+4, i+5)` — not the full original I-span `[i, i+5)`.** The deleted gap `[i+2, i+4)` vanishes from the result because the I→V conversion step uses the current POOM state, and the deleted content has no V-position mapping anywhere.

Here is the complete traced execution.

---

### Step 0: The Critical Misread of the API

The first thing to clarify: `RETRIEVEENDSETS` does **not** take a link ISA as its argument. It takes a **content specset** — a document region. `getretrieveendsets` [get1.c:185–188] just calls `getspecset`, and the golden tests confirm this:

```python
doc_span = SpecSet(VSpec(source_opened, [Span(Address(1, 1), Offset(1))]))
session.retrieve_endsets(doc_span)   # whole-document V-span, not link address
```

This means: "find all link endsets that overlap this document region." The specset is converted to I-spans through the current POOM before the spanfilade is queried.

---

### Step 1: What DELETE Does (and Doesn't Do)

`dodeletevspan` [do1.c:158–167]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` [orglinks.c:145–152]:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width)) return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

DELETE calls `deletend` only on the **document's POOM** (in `granf`). It removes the V→I mapping for `[i+2, i+4)`. The link's endset entry in the **spanfilade** is never touched — no `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c` (confirmed by Finding 0057).

**After DELETE:**
- Document POOM: maps V-positions to `[i, i+2)` and `[i+4, i+5)`. The gap `[i+2, i+4)` has no V-mapping.
- Spanfilade: still contains the link endset crum `ORGLRANGE = 1.L` (LINKFROMSPAN + link ISA L), `SPANRANGE = [i, i+5)`.

---

### Step 2: RETRIEVEENDSETS Entry Point

`retrieveendsets` [fns.c:350–362] → `doretrieveendsets` [do1.c:369–374] → `retrieveendsetsfromspanf` [spanf1.c:190–235].

---

### Step 3: The Spanfilade Query

Inside `retrieveendsetsfromspanf`, three things happen:

**3a. Convert the query specset to I-spans** via `specset2sporglset` [sporgl.c:14–33]:

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
```

For a VSPEC like `(doc_D, V-range)`, this calls `vspanset2sporglset` [sporgl.c:35–65], which calls `vspanset2ispanset` → `permute` on the document's POOM to get the I-spans currently accessible in that V-range.

After the DELETE, the document's POOM maps the queried V-region to only **`[i, i+2)` and `[i+4, i+5)`** — the gap `[i+2, i+4)` produces nothing.

So `sporglset` contains two entries: sporglorigin=`i`, sporglwidth=`2` and sporglorigin=`i+4`, sporglwidth=`1`.

**3b. Search the spanfilade** via `retrievesporglsetinrange` [spanf1.c:237–267]:

```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE, (typeisa*)NULL);
```

Where `whichspace` = `{stream.mantissa[0]=LINKFROMSPAN=1, width.mantissa[0]=1}` = ORGLRANGE range `[1.0…, 2.0…)`.

The spanfilade crum for link L's from-endset has:
- `ORGLRANGE = prefixtumbler(L, LINKFROMSPAN)` = `1.L` — **within `[1.0…, 2.0…)` ✓**
- `SPANRANGE = [i, i+5)`

Does `[i, i+5)` overlap `[i, i+2)` (first query)? **Yes** — intersection `[i, i+2)`.  
Does `[i, i+5)` overlap `[i+4, i+5)` (second query)? **Yes** — intersection `[i+4, i+5)`.

The crum qualifies both times (via `crumqualifies2d` [retrie.c:270–305]). The link L is found.

**3c. Extract the full crum range** via `contextintosporgl` [sporgl.c:205–220]:

```c
contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
// -> sporglptr->sporglorigin = context->totaloffset.dsas[SPANRANGE] = i
// -> sporglptr->sporglwidth  = context->contextwid.dsas[SPANRANGE]  = 5
```

`fromsporglset` gets the **full** endset range: `sporglorigin=i`, `sporglwidth=5` = `[i, i+5)`. The spanfilade returns the stored crum's complete range, not an intersection of it with the query.

---

### Step 4: I→V Conversion Filters the Deleted Gap

`linksporglset2specset` [sporgl.c:97–123] → `sporglset2vspanset` [sporgl.c:141–176] → `ispan2vspanset` [orglinks.c:389–394]:

```c
typevspanset *ispan2vspanset(..., typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` [orglinks.c:404–422] calls `span2spanset` which calls `retrieverestricted` on the document's POOM with the I-span `[i, i+5)` in the I-dimension to find corresponding V-spans.

The document's POOM after DELETE:
- V→I: some V-range A maps to `[i, i+2)`
- V→I: some V-range B maps to `[i+4, i+5)`
- `[i+2, i+4)` → **no V-mapping** (removed by `deletend`)

`permute` walks the POOM and finds crums overlapping `[i, i+5)` in the I-dimension. It returns:
- V-range A (for `[i, i+2)`)
- V-range B (for `[i+4, i+5)`)
- **Nothing** for `[i+2, i+4)` — no crum exists for it.

---

### Step 5: Observed Behavior (Golden Test Confirmation)

`golden/endsets/endsets_after_source_delete.json` records the analogous experiment (deleting from the *beginning* of a linked region rather than the middle, producing one surviving span rather than two):

```json
"before": { "spans": [{ "start": "1.7", "width": "0.10" }] },
"after":  { "spans": [{ "start": "1.7", "width": "0.4"  }] }
```

Link was on "right here" (10 chars). DELETE removed "right " (6 chars). The endset shrunk to only "here" (4 chars). The deleted content simply vanishes from the endset — the link does not "break" but does contract.

For a **middle** deletion (`[i+2, i+4)` removed from `[i, i+5)`), the same mechanism produces **two disjoint spans** rather than one: the link is not broken but is split, exactly as Finding 0019 §3 ("Pivot Operations Fragment Link Endsets") shows for rearrangements.

---

### Summary of the Call Chain

```
RETRIEVEENDSETS(doc_V_span)
  fns.c:350    retrieveendsets()
  do1.c:373    doretrieveendsets() -> retrieveendsetsfromspanf()
  spanf1.c:222   specset2sporglset(doc_V_span)
                   sporgl.c:48  vspanset2ispanset() via doc POOM
                   -> after delete: I-spans = [i,i+2) + [i+4,i+5)
  spanf1.c:223   retrievesporglsetinrange(I-spans, LINKFROMSPAN)
                   retrie.c:56  retrieverestricted(spanf, SPANRANGE=[i,i+2), ORGLRANGE=1.*)
                     -> finds crum: SPANRANGE=[i,i+5), ORGLRANGE=1.L  [OVERLAP]
                   retrie.c:56  retrieverestricted(spanf, SPANRANGE=[i+4,i+5), ORGLRANGE=1.*)
                     -> finds same crum again
                   -> fromsporglset = {origin=i, width=5} (full endset, unrestricted)
  spanf1.c:224   linksporglset2specset(homedoc, fromsporglset=[i,i+5))
                   sporgl.c:157  ispan2vspanset([i,i+5), doc_POOM)
                     orglinks.c:393  permute(POOM, [i,i+5), I->V)
                     -> [i,i+2)   maps to V-range A  [EXISTS in POOM]
                     -> [i+2,i+4) maps to nothing     [DELETED, absent from POOM]
                     -> [i+4,i+5) maps to V-range B  [EXISTS in POOM]
  RESULT: two V-spans — V-range A and V-range B
```

---

### Conclusion

`RETRIEVEENDSETS` returns **`[i, i+2)` and `[i+4, i+5)` expressed as V-addresses** — the portions that remain reachable through the document's current POOM. It does **not** return the full original I-span `[i, i+5)`.

The mechanism is:
1. **The spanfilade is never cleaned up** (`insertspanf` has no inverse; `dodeletevspan` [do1.c:158–167] touches only the POOM via `deletend` [orglinks.c:149]). The full `[i, i+5)` endset crum persists.
2. **The query converts the caller's content to current I-spans** via `vspanset2ispanset` on the live POOM. After deletion, only `[i, i+2)` and `[i+4, i+5)` are returned from the POOM — the gap produces nothing.
3. **Both surviving fragments overlap the stored crum** `[i, i+5)` → the link is found.
4. **The returned full crum `[i, i+5)` is then converted back to V-spans** via `ispan2vspanset` on the same live POOM. The gap `[i+2, i+4)` has no V-position anywhere → it is absent from the result.

The link survives the delete. Its endset adapts to reflect only the currently accessible content. The deleted content is simply invisible — no V-position for it exists in any POOM.

---

## Question 12 [gregory]

> If a link L references content at I-addresses `[i, i+3)`, that content is deleted from all documents (making L orphaned), and then a COPY transcludes just `[i+1, i+2)` (a subset of the original endset) into a new document, does `find_links` on that new document rediscover L — and if so, does the returned endset show only the single transcluded byte or the full original three-byte span?

### Gregory's Answer

## KB Synthesis

## Answer

**Yes, `find_links` rediscovers L. The returned endset shows only the single transcluded byte, not the original three-byte span.**

---

### Part 1: Rediscovery

`find_links` operates on I-address intersection, not V-stream presence [SS-FIND-LINKS]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

Partial overlap suffices. D_new's COPY puts `[i+1, i+2)` into its POOM. L's source endset covers `[i, i+3)`. The intersection is `{i+1}` — non-empty. L is returned.

Two invariants make this work despite the prior deletion:

1. **The spanfilade is write-only** [INV-SPANF-WRITE-ONLY]: When L was originally created, `insertendsetsinspanf` indexed `[i, i+3) → L` in the spanfilade. DELETE removes POOM entries but never touches the spanfilade [ST-DELETE, Finding 0057]. Those index entries still exist.

2. **The spanfilade is not disturbed by orphaning** [INV-LINK-PERMANENCE]: Even when all documents deleted the content, L's spanfilade entries persisted. The COPY into D_new creates a new DOCISPAN entry for D_new at `i+1` [SS-DOCISPAN], but the link index entry `i+1 → L` was already there from L's creation.

---

### Part 2: The Endset Shows Only One Byte

The endset resolution is governed by [INV-ITOV-FILTERING] and [SS-FOLLOWLINK]:

> FOLLOWLINK extracts I-addresses from the link orgl, then converts them to V-addresses using the **querying document's POOM**. If an I-address has no POOM mapping, it is silently dropped — no V-span is added to the result.

D_new's POOM maps:
- `i` → no entry (not transcluded) → **dropped**
- `i+1` → some V-position v₁ → **included**
- `i+2` → no entry (not transcluded) → **dropped**

The endset returned is the V-span `[v₁, v₁+1)` in D_new — one byte.

This matches the behavior documented in the `partial_vcopy_of_linked_span` test [SS-FOLLOW-LINK]: a link created on "hyperlink text" (14 chars) is discovered via a transcluded "link" (4 chars), but `follow_link` resolves to only the 4 chars present in the querying document, not the original 14.

The same filtering applies here, but more aggressively: only 1 of 3 original bytes is present in D_new, so only 1 appears in the endset.

---

### What Cannot Be Recovered

The original 3-byte span is unrecoverable through normal operations. `follow_link` against any document that once held the full `[i, i+3)` range returns empty `[]` — because deletion freed those POOM entries [ST-DELETE, FC-VERSION-ISOLATION]. The link orgl in I-space still stores the full original I-address range [INV-LINK-PERMANENCE], but resolution requires a live POOM mapping, and none exists for `i` or `i+2`. COPY is the only mechanism for identity-preserving restoration [ST-COPY, Finding 0064], and only `i+1` was re-introduced.

---

## Code Exploration

Now I have all the information needed. Let me trace the full execution path to answer both sub-questions.

---

## Full Answer

### Scenario Setup Recap

- Link L created with a from-endset (or to-endset) covering I-addresses `[i, i+3)` (3 bytes)
- All documents' POOMs updated by `dodeletevspan` to remove `[i, i+3)` from V-space
- New document D: COPY transcluded only `[i+1, i+2)` (1 byte) into it
- Question: Does `find_links` on D rediscover L? And what does the endset show?

---

### Part 1: Does `find_links` rediscover L?

**Yes.** Here is the trace:

#### Step A — Link creation stores the full I-span in the spanfilade

When L was created, `docreatelink` [do1.c:195–221] called `insertendsetsinspanf` [do2.c:116–128], which called `insertspanf` [spanf1.c:15–54] for each endset sporgl. That call stored a crum in the global `spanf` with:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // I-address: i
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);     // width: 3
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[spanf1.c:49–51]

The spanfilade crum records: `SPANRANGE = [i, i+3)`, `ORGLRANGE = linkisa.LINKFROMSPAN`.

#### Step B — Deletion does NOT touch the spanfilade

`dodeletevspan` [do1.c:158–167] calls only:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
logbertmodified(docisaptr, user);
```
[orglinks.c:149–150]

Only the **document's POOM** is modified. The global `spanf` and L's own POOM (`insertpm` records) are never touched. L's spanfilade entry for `[i, i+3)` persists intact.

#### Step C — COPY of `[i+1, i+2)` into D

`docopy` [do1.c:45–65] calls:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)    // [i+1, i+2)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)         // D's POOM: V→[i+1,i+2)
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // spanf DOCISPAN entry
```

D's POOM now has a single crum: `I-axis = [i+1, i+2)` ↔ `V-axis = some vD`.

#### Step D — `find_links` on D

`findlinksfromtothree` [fns.c:189] → `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56]:

```c
specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```
[spanf1.c:71, 77]

`specset2sporglset` [sporgl.c:14] → `vspanset2sporglset` [sporgl.c:35]:

```c
vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);    // permute V→I in D's POOM
```

D's POOM maps `vD → [i+1, i+2)`, so `ispanset = [i+1, i+2)`. This becomes a sporgl with `sporglorigin=i+1, sporglwidth=1`.

`sporglset2linkset` [sporgl.c:222] → `sporglset2linksetinrange` [sporgl.c:239]:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:229]. The restriction is SPANRANGE = `[i+1, i+2)`. The query checks whether L's spanfilade crum (`SPANRANGE = [i, i+3)`) qualifies:

```c
bool crumqualifies2d(... span1start=[i+1], span1end=[i+2] ...) {
    endcmp = whereoncrum(crumptr, ..., span1end=[i+2], SPANRANGE);   // [i,i+3) contains i+2 → THRUME
    // NOT ≤ ONMYLEFTBORDER → passes
    startcmp = whereoncrum(crumptr, ..., span1start=[i+1], SPANRANGE); // [i,i+3) contains i+1 → THRUME
    // NOT > THRUME → passes
    ...
    return TRUE;
```
[retrie.c:270–305]

`[i, i+3)` contains `[i+1, i+2)` entirely, so `crumqualifies2d` returns TRUE. The context is built from this crum. Then:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
onlinklist(taskptr, linksetptr, &linksa);
```
[sporgl.c:264–265]

L's ISA is extracted from the ORGLRANGE and added to the result. **L is found.**

---

### Part 2: What does the endset show?

`find_links` returns only link ISAs — no endset is included in the `findlinksfromtothreesp` result. The subsequent call to retrieve L's endset goes through two distinct paths:

#### Path A — `follow_link` (via `dofollowlink`)

`dofollowlink` [do1.c:223] → `link2sporglset` [sporgl.c:67]:

```c
retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)
```

This queries L's **own POOM** (populated by `insertpm` at creation time) at V-address `whichend`. L's POOM crum has `I-axis = [i, i+3)` (the full 3 bytes stored at creation). `contextintosporgl` [sporgl.c:205] extracts:

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);  // original source doc
movetumbler(&context->totaloffset.dsas[I], &sporglptr->sporglorigin);     // i
movetumbler(&context->contextwid.dsas[I], &sporglptr->sporglwidth);       // 3
```

Then `linksporglset2specset` [sporgl.c:97]:

```c
} else {
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

Since `sporgladdress` (the original source doc) is non-zero, it calls `sporglset2vspanset` [sporgl.c:141] → `ispan2vspanset` [orglinks.c:389] → `permute` on the **original source document** with I-span `[i, i+3)`. That document's POOM no longer has any mapping for those bytes (deleted). `permute` → `span2spanset` → `retrieverestricted` finds no crums. **Returns empty vspanset.**

The document D (which has `[i+1, i+2)`) is never consulted here, because `homedoc` in the sporgl is the original source document set at link creation time [sporgl.c:53]:

```c
movetumbler(docisa, &sporglset->sporgladdress);   // set to original source doc
```
[sporgl.c:53]

#### Path B — `retrieve_endsets` (via `retrieveendsetsfromspanf`)

`retrieveendsetsfromspanf` [spanf1.c:190] finds L's spanfilade entry for its from-endset. `contextintosporgl` [sporgl.c:205] extracts the stored I-span: `sporglorigin=i, sporglwidth=3` — the **full 3 bytes** — with `sporgladdress = homedoc` (original source doc). `linksporglset2vspec` then calls `ispan2vspanset` on the original source document with `[i, i+3)` → **empty vspanset** (deleted).

The returned specset is a `VSPECID` node with `docisa=homedoc` and `vspanset=NULL`.

#### The clipping function `context2span` is not the issue

`context2span` [context.c:176–212] does proportional clipping when translating between I and V dimensions in `span2spanset`/`permute`. This function would correctly return just 1 byte if called on document D's POOM with restriction `[i, i+3)`. But it is only invoked during `ispan2vspanset` on `homedoc` — and `homedoc` is always the **original source document**, not D, because that is what was stored in the spanfilade at creation time.

---

### Summary

| Question | Answer | Key Code |
|---|---|---|
| Does `find_links` on D find L? | **Yes** | `crumqualifies2d` at retrie.c:270 passes because `[i, i+3) ∩ [i+1, i+2) ≠ ∅` |
| What endset does `follow_link` return? | **Empty vspanset** | `sporglset2vspanset` at sporgl.c:141 looks up `[i, i+3)` in original source doc (deleted); D is never consulted |
| What is stored in the spanfilade? | **Full 3-byte I-span `[i, i+3)`** | `insertspanf` at spanf1.c:49–51 stores the full original width; deletion never modifies `spanf` |
| Is the 1-byte transcluded copy ever reflected in the endset? | **No** | The `homedoc` pointer in the sporgl permanently locks endset resolution to the original source document |

**The returned endset is neither "1 byte" nor "3 bytes"** — it is **empty** (`vspanset = NULL`). The spanfilade stores the full original 3-byte I-span `[i, i+3)` and that is what `crumqualifies2d` matches against during `find_links`. But when any endset retrieval attempts to resolve those I-addresses back to V-space, it does so against `homedoc` (the original source document, where the content was deleted). The 1-byte copy in D updates D's own POOM and a new DOCISPAN entry in `spanf`, but it does not update L's LINKFROMSPAN/LINKTOSPAN entries or L's internal POOM. There is no mechanism by which L's stored endsets point at D.

---

## Question 13 [gregory]

> After REARRANGE with a 3-cut pivot splits a contiguous endset span across two non-adjacent V-regions in the same document, does `RETRIEVEENDSETS` followed by I-to-V conversion via `span2spanset` return a two-VSpec specset reflecting both V-positions, or does the conversion lose one of the fragments?

### Gregory's Answer

## KB Synthesis

## Answer: Both V-positions Are Returned — With Possible Duplication

After a pivot, the I-to-V conversion returns a multi-VSpec specset covering both V-regions. The conversion does **not** lose fragments.

### Mechanism

**Step 1 — Pivot preserves I-addresses, changes V-mapping** [INV-REARRANGE-IDENTITY]: A pivot displaces V-positions but leaves I-addresses unchanged. If the endset originally covered a contiguous I-address range α..β at V-region R₁, after the pivot those I-addresses now map to two disjoint V-regions (e.g., part at R₁, part at R₂).

**Step 2 — POOM is a multimap** [SS-POOM-MULTIMAP]: The POOM accumulates every matching leaf via `findcbcinarea2d()`, which traverses all siblings and descends into all qualifying subtrees. `incontextlistnd()` inserts each found context into a V-sorted linked list, never replacing. This means `ispan2vspanset(poom, α..β)` returns **all** V-positions that contain I-addresses in that range — both R₁ and R₂.

**Step 3 — RETRIEVEENDSETS conversion path** [SS-RETRIEVE-ENDSETS]: The call chain is `linksporglset2specset()` → `sporglset2vspanset()` → `span2spanset()` → `retrieverestricted()`. The result is sorted by V-position [INV-RETRIEVAL-V-SORTED]. Unreferenced I-addresses are silently dropped, but both V-regions are active in the POOM after the pivot, so nothing is filtered.

**Step 4 — Result** [INV-RETRIEVAL-TREE-INDEPENDENCE]: The conversion returns a specset with (at least) two VSpecs: one for each V-region containing the endset's I-addresses. The V-ordering invariant guarantees they appear in ascending V-address order.

### The Duplication Caveat

[EC-PIVOT-LINK-FRAGMENTATION] reports that after a pivot swapping "BC" and "DE" within a document containing a link on "CD", the endsets report **four spans** (`1.2 width 0.1` twice, `1.5 width 0.1` twice), and `find_links` returns the same link **twice**. The duplication arises because the spanfilade stores multiple sporgls for the link endset (one per contiguous I-span, per [SS-SPORGL] and [ST-LINK-CREATE]), and each sporgl independently resolves to its V-address — the same V-position can be discovered via multiple sporgl entries in the index.

### Summary

| Question | Answer |
|---|---|
| Does `span2spanset` return both V-positions? | **Yes** — POOM multimap semantics accumulate all matches [SS-POOM-MULTIMAP] |
| Can conversion lose a fragment? | **No** — `findcbcinarea2d` traverses all qualifying subtrees [SS-POOM-MULTIMAP] |
| Are results V-sorted? | **Yes** — `incontextlistnd` maintains sorted order [INV-RETRIEVAL-V-SORTED] |
| Any anomaly? | **Duplication** — same V-position may appear multiple times [EC-PIVOT-LINK-FRAGMENTATION] |

---

## Code Exploration

Now I have enough to trace the full execution path. Let me compile the complete analysis.

---

## Full Answer

### 1. What REARRANGE Does to the POOM

`dorearrange` [do1.c] → `rearrangepm` [orglinks.c:137–142] → `rearrangend` [edit.c:78–160].

For a 3-cut pivot (`nblades == 3`), `makeoffsetsfor3or4cuts` [edit.c:177–181] computes:

```c
diff[1] = blades[2] - blades[1];      // forward shift for section 1
diff[2] = -(blades[1] - blades[0]);   // backward shift for section 2 (negate)
diff[3] = 0;                           // (unused for 3 cuts)
```

`makecutsnd` splits POOM crums at the knife positions. Then [edit.c:113–135]:

```c
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = rearrangecutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 1: case 2: case 3:
        tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V]);
        ivemodified(ptr);
        break;
    }
}
```

The POOM crum's V-displacement (`cdsp.dsas[V]`) is updated in place. After a 3-cut pivot, a contiguous I-span that previously mapped to one contiguous V-region now maps to **two non-adjacent V-regions**. The spanfilade is **not touched** by any of this.

---

### 2. The Spanfilade Stores I-Spans — Immutable Under REARRANGE

When a link is created, `insertspanf` [spanf1.c:15–54] inserts POOM crums into the spanfilade indexed by:
- `SPANRANGE` = I-space content address
- `ORGLRANGE` = link's orgl address with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` prefix

REARRANGE calls `rearrangend` only on the document orgl (POOM), not the spanfilade. The I-span stored in the spanfilade remains exactly as inserted at `CREATELINK` time.

---

### 3. RETRIEVEENDSETS Execution Path

`retrieveendsets` [fns.c:350–362] →
`doretrieveendsets` [do1.c:369–374] →
`retrieveendsetsfromspanf` [spanf1.c:190–235]:

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset(taskptr, &docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

**Step A: `specset2sporglset`** [sporgl.c:14–33]  
Converts the input specset (identifying the link, typically a VSPECID) to a sporglset in I-space via `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset`. This produces the link's I-span identity.

**Step B: `retrievesporglsetinrange`** [spanf1.c:237–267]  
Queries the spanfilade:

```c
context = retrieverestricted((typecuc*)spanf, sporgl_as_ispan, SPANRANGE,
                              whichspace, ORGLRANGE, NULL);
for (c = context; c; ...) {
    contextintosporgl((type2dcontext*)c, NULL, sporglset, SPANRANGE);
    // extracts: sporglorigin = totaloffset.dsas[SPANRANGE] (I-span start)
    //            sporglwidth = contextwid.dsas[SPANRANGE]  (I-span width)
    //            sporgladdress = context2dinfo.homedoc
```

The spanfilade is unchanged by REARRANGE, so this finds the original single I-span entry for the endpoint. `fromsporglset` gets one sporgl whose `sporglorigin`/`sporglwidth` is the original (pre-REARRANGE) I-span.

---

### 4. I-to-V Conversion: `linksporglset2specset` → `ispan2vspanset` → `span2spanset`

`linksporglset2specset` [sporgl.c:97–123] →
`linksporglset2vspec` [sporgl.c:127–137] →
`sporglset2vspanset` [sporgl.c:141–176]:

```c
ispan.stream = sporglptr->sporglorigin;
ispan.width  = sporglptr->sporglwidth;
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` [orglinks.c:389–394]:

```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

`permute` [orglinks.c:404–422] calls `span2spanset` once per input span.

`span2spanset` [orglinks.c:425–454]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I,
                              NULL, V, NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, I, &foundspan, V);
    nextptr = onitemlist(taskptr, &foundspan, targspansetptr);
}
```

`retrieverestricted` [retrie.c:56–85] → `retrieveinarea` [retrie.c:87–110] → `findcbcinarea2d` [retrie.c:229–268]:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(..., span1start, span1end, I, span2start, span2end, V, ...))
        continue;
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, crumptr->cenftype);
        findcbcinarea2d(findleftson(crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
        incontextlistnd(headptr, context, I);  // inserts sorted by I-address
    }
}
```

This recursively walks the **rearranged POOM**. After the 3-cut REARRANGE, there are (at minimum) two groups of leaf crums covering the original I-span `[I₁, I₁+N)`:
- Group A: crums with `cdsp.dsas[I]` ∈ `[I₁, I₁+M)`, V-displacement → region A
- Group B: crums with `cdsp.dsas[I]` ∈ `[I₁+M, I₁+N)`, V-displacement → region B

`crumqualifies2d` [retrie.c:270–305] returns `TRUE` for crums in **both groups** because the I-span restriction covers `[I₁, I₁+N)`. Both groups produce context records. `incontextlistnd` [context.c:75–111] inserts them in I-sorted order.

Back in `span2spanset`, `context2span` [context.c:176–212] is called for each context:

```c
// clips the crum's I-range to the query restriction
// then maps the clipped I-range to V via totaloffset.dsas[V] / contextwid.dsas[V]
movetumbler(&grasp.dsas[V], &foundspanptr->stream);
tumblersub(&reach.dsas[V], &grasp.dsas[V], &foundspanptr->width);
```

Group A contexts map to VSpan for V-region A. Group B contexts map to VSpan for V-region B.

`onitemlist` [orglinks.c:464–537] → `putvspaninlist` [orglinks.c:329–387] accumulates both VSpans. Since V-region A and V-region B are non-adjacent, the adjacency-merge check (`spancmp == 0`) never fires [orglinks.c:346–348], and they remain as **two separate entries** in the vspanset.

---

### 5. Shape of the Returned Specset

The result is **one VSPEC** (not two), with a **two-entry `vspanset`** — one VSpan per V-region. `linksporglset2vspec` [sporgl.c:127–137] wraps the entire multi-fragment vspanset into a single VSPECID item:

```c
specptr->itemid = VSPECID;
specptr->vspanset = NULL;
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
```

The client receives (for the `fromset`): one VSPECID node whose `vspanset` field is a linked list of two VSpans.

---

### 6. Verdict

**The conversion does NOT lose either fragment.** `span2spanset` operates by querying the post-REARRANGE POOM with the original I-span. The rearranged POOM has been split (by `makecutsnd` during REARRANGE) at the knife positions, so `findcbcinarea2d` locates leaf crums in both V-regions. Each leaf crum produces a context; each context maps through `context2span` to a VSpan; `putvspaninlist` preserves both non-adjacent VSpans as distinct entries.

The returned specset for each endset (from/to/three) is a single VSPECID containing a two-fragment vspanset — one VSpan per non-adjacent V-region. Both V-positions are faithfully reflected in the output.

**One structural caveat**: the system returns one VSPEC with two VSpans in its `vspanset`, not two separate VSPEC items. If the caller assumes a single-VSpan vspanset and only reads `vspanset->stream`/`vspanset->width` without following `vspanset->next`, it will see only one of the two V-regions. The data is complete in the response; whether the client faithfully iterates the vspanset is a client-side concern.

---

## Question 14 [gregory]

> When CREATENEWVERSION copies only text subspace `1.x` and not links from subspace `2.x`, is the link's own I-address (its orgl at `docISA.0.2.N`) excluded from the version's POOM — and if so, does `RETRIEVEDOCVSPANSET` on the version show zero entries in the link subspace even though `find_links` discovers the original's links through shared text I-addresses?

### Gregory's Answer

## KB Synthesis

Yes on all three counts, and the KB is explicit about each.

**Link subspace excluded from version POOM**

`CREATENEWVERSION` calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum. These fields track the **text subspace** displacement starting at position `1`, not position `0` (the link subspace). The link subspace at `2.x` is structurally outside this V-dimension range. [SS-DUAL-ENFILADE / Finding 0043], [ST-VERSION-CREATE / Finding 0043, 0046]

The copy then runs via `docopyinternal`, which inserts only the text V-span into the new document's POOM. No link orgl ISAs (the `docISA.0.2.N` entries) are placed into the version's POOM. [ST-VERSION-CREATE / Finding 0046]

**RETRIEVEDOCVSPANSET confirms zero link entries**

Golden test evidence from Finding 0043 is direct:

```
Source vspanset (normalized output):
  at 0 for 0.1   (link subspace — internal 2.x)
  at 1 for 1     (text subspace)

Version vspanset:
  at 1.1 for 0.34   (text only, no link subspace)
```

The version's `retrieve_vspanset` returns only a text span. [SS-VSPAN-VS-VSPANSET], [ST-VERSION-CREATE / Finding 0043]

**find_links works anyway — through shared text I-addresses**

This is the key decoupling. `find_links` does not query the POOM at all — it queries the **spanfilade** (span enfilade) by I-address. The version's text subspace shares permascroll I-addresses with the source's text subspace (that's what `docopyinternal` establishes). Those I-addresses are already indexed in the spanfilade because the source's original `INSERT`/`COPY` operations wrote DOCISPAN entries. [SS-DUAL-ENFILADE / Finding 0012], [FC-CONTENT-SPANF-ISOLATION / Finding 0036], [INT-LINK-VERSION / Finding 0046]

When you call `find_links` on the version, the call chain is:
1. Convert version V-span to I-spans (via the version's POOM, which maps text V-positions to shared permascroll I-addresses)
2. Search the spanfilade by those I-addresses
3. Return links whose endsets intersect

Since the I-addresses are identical between source and version, the same spanfilade entries fire. [INT-LINK-VERSION / Finding 0032, 0046], [INV-LINK-GLOBAL-VISIBILITY]

**The link orgl's own I-address (`docISA.0.2.N`) is irrelevant here**

The link's I-address (its identity in the granfilade, e.g. `1.1.0.1.0.1.0.2.1`) is neither copied nor needed for discovery. Discovery runs through the **endpoint content** I-addresses (the permascroll text that the link's FROM/TO/THREE endsets reference), not through the link orgl's own address. The version inherits discoverability because it inherits the endpoint content identity — not because it has any representation of the link in its POOM. [SS-THREE-LAYER-MODEL / Finding 0040], [INT-LINK-TRANSCLUSION / Finding 0043]

**Summary**

| | Version |
|---|---|
| Link subspace in POOM | Empty |
| `retrieve_vspanset` link entries | None |
| `find_links` result | Same as source |

The version's POOM-level link subspace is empty; link **discoverability** is preserved purely through shared text I-addresses in the spanfilade. These are independent mechanisms. [SS-THREE-LAYER-MODEL], [FC-SUBSPACE / Finding 0043], [ST-VERSION-CREATE / Finding 0043, 0046]

---

## Code Exploration

Now I have everything needed for a complete answer. Let me compile it with full code citations.

---

## Full Answer

### Summary

Yes, the link's own I-address (its orgl at `docISA.0.2.N`) **is excluded** from the new version's POOM. `RETRIEVEDOCVSPANSET` on the version shows **zero entries** in the link subspace. And `find_links` **does discover** the original's links through shared text I-addresses. Here is the complete code trace.

---

### 1. How CREATENEWVERSION Copies Content

`docreatenewversion` [do1.c:260-299]:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)         // [do1.c:281]
...
vspec.docisa = *isaptr;                                 // source = original doc
vspec.vspanset = &vspan;                               // the V-range to copy
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // [do1.c:293]
```

The vspan comes from `doretrievedocvspanfoo` [do1.c:301-309], which calls `retrievedocumentpartofvspanpm` [orglinks.c:155-162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // [orglinks.c:159]
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);  // [orglinks.c:160]
    return (TRUE);
}
```

This reads the root crum's `cdsp.dsas[V]` and `cwid.dsas[V]` directly.

---

### 2. The Root Crum's V-Span Covers Only Text

Per Finding 0066 and [wisp.c] `setwispnd`: for a POOM with text at V=1.x and link at V=2.x, the root's `cdsp.dsas[V]` = the minimum V-address across all content = **1** (text start). Its `cwid.dsas[V]` = the bounding box width = **1** (representing the extent of the text).

The comment at [do1.c:302] says `/* this routine is a kluge not yet kluged*/`, signaling this function is not intended to handle multi-subspace documents. The returned vspan is:

```
stream = 1    (= V=1, start of text subspace)
width  = 1    (= width 1, covering V=1.x only)
```

The range `[1, 1+1]` = `[1, 2)` encompasses the text subspace (V=1.x) but does **not** reach the link subspace at V=2.1 (since 2.1 > 2.0). The link at V=2.x sits just outside this range.

Validated empirically in `golden/versions/version_copies_link_subspace.json`:
```
Source vspanset: at 0 for 0.1    (link, normalized from V=2.x)
                 at 1 for 1      (text)

Version vspanset: at 1.1 for 0.15   (text only — confirmed)
```

---

### 3. specset2ispanset Finds Only Text I-Spans

`docopyinternal` [do1.c:66-82]:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // V→I on original doc
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)     // put I-spans in new doc
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // register in spanf
```

`specset2ispanset` [do2.c:14-46] → `vspanset2ispanset` [orglinks.c:397-402] → `permute(V→I)` [orglinks.c:404-422] → `retrieverestricted` traverses the original document's POOM with restriction span `[1, 2)` in V. This finds **only** the text crums (at V=1.x, mapping to permascroll I-addresses). The link crum at V=2.1 is outside the restriction range — it is never visited.

The returned `ispanset` is therefore **permascroll I-addresses only** — no link ISA.

`insertpm` [orglinks.c:75-134] inserts these text I-spans into the new version's POOM starting at `vsaptr = &vspan.stream = 1`. The link's I-address (docISA.0.2.N) is **never placed** in the new version's POOM at all — neither in text subspace nor link subspace. It is completely absent.

---

### 4. RETRIEVEDOCVSPANSET Shows Zero Link Entries

`doretrievedocvspanset` [do1.c:322-336] → `retrievevspansetpm` [orglinks.c:173-221]:

```c
if (is1story(&ccptr->cwid.dsas[V])) { /* if it is just text return that */
    // return single text span
} else {
    // extract link and text spans separately
    linkvspan.stream = ccptr->cwid.dsas[V] with mantissa[1]=0
    ...
    maxtextwid(taskptr, ccptr, &voffset, &maxwid);
}
```

`is1story` [tumble.c:237-247]:
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

Returns TRUE when only `mantissa[0]` is non-zero — i.e., the width spans only a single "story" (the V=1.x story with no link-subspace component).

The new version's POOM contains only text I-spans at V=1.x. Its root `cwid.dsas[V]` is a text-only tumbler with no multi-story component. `is1story` returns **TRUE**, so `retrievevspansetpm` takes the simple branch, returning **one text span and zero link entries**. The link subspace component is structurally zero because there are no crums at V=2.x in the new version's orgl.

`RETRIEVEDOCVSPANSET` output for the version: text span only. **Zero entries in the link subspace.**

---

### 5. find_links Discovers Original's Links Via Shared I-Addresses

When the version was built, `insertspanf(taskptr, spanf, newisaptr, ispanset, DOCISPAN)` [do1.c:79] registered the new version's text I-spans in the global spanf under the new version's ISA. These are **the same permascroll I-addresses** as the original document's text content.

When `findlinksfromtothreesp` [spanf1.c:56-103] is called with a V-spec pointing to the new version's text:

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                      orglrange, LINKFROMSPAN);
```

`specset2sporglset` on the new version maps its text V-positions to I-spans (permascroll addresses). These permascroll addresses are **identical** to the original's text I-spans, because `docopyinternal` copied the same permascroll content without allocating new I-addresses.

The original document's link registration (during `docreatelink` [do1.c:195-221]) called `insertendsetsinspanf` [do2.c:116-128]:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
```

This recorded in the global spanf: `text_permascroll_I-span → original_link_ISA` (under LINKFROMSPAN / LINKTOSPAN orgl-range keys derived from the link's ISA).

`sporglset2linkset` searches the spanf by I-span — not by document ISA. When the version's text permascroll I-spans are submitted, they match the registered link endpoints from the original. The link ISA (docISA.0.2.N) is returned.

**`find_links` discovers the original document's links** because:
- Link discovery is I-address-based (global spanf), not V-address-based (per-POOM)
- The new version shares permascroll I-spans with the original
- The original's link endpoints were registered against those same I-spans

This is validated by golden tests (Finding 0007: `version_with_links`; Finding 0026: `link_to_transcluded_content`).

---

### Concise Answer to Each Part

| Question | Answer | Mechanism |
|----------|--------|-----------|
| Is the link's I-address (orgl at `docISA.0.2.N`) excluded from the version's POOM? | **Yes, fully excluded** | `retrievedocumentpartofvspanpm` [orglinks.c:155-162] returns a vspan covering only V=1.x (text). `permute(V→I)` never visits the crum at V=2.x. The link's ISA is never passed to `insertpm`. |
| Does `RETRIEVEDOCVSPANSET` show zero entries in the link subspace? | **Yes, zero entries** | The new version's POOM has no crums at V=2.x. `retrievevspansetpm` [orglinks.c:173-221] via `is1story` [tumble.c:237] reports a single text span only. |
| Does `find_links` discover the original's links through shared text I-addresses? | **Yes** | The spanf stores link endpoints by permascroll I-address globally. `findlinksfromtothreesp` [spanf1.c:56-103] searches by I-span, not by document. The version shares text permascroll I-spans with the original, so the original's links are found through them. |

The architectural asymmetry is this: the POOM (V→I mapping) is **per-document and subspace-aware** — only the text subspace (V=1.x) is copied by `CREATENEWVERSION`. The spanf (I→link mapping) is **global and document-agnostic** — it tracks link endpoints purely by I-address, making links follow shared content identity across all versions.

---

## Question 15 [gregory]

> In a multi-session scenario where session A creates a link L targeting content in document D, and session B simultaneously deletes that content from D before A's operation completes — given run-to-completion atomicity, is there any window where L's spanfilade entries could reference I-addresses that were never actually present in D's POOM, or does the serialized execution guarantee consistency between link creation and POOM state?

### Gregory's Answer

## KB Synthesis

## Answer

No window exists where L's spanfilade entries can reference I-addresses that were **never actually present** in D's POOM. The combination of run-to-completion atomicity and the V-to-I filtering invariant forecloses it.

### Why atomicity closes the concurrent window

[INV-ATOMICITY] and [INV-SEQUENTIAL-DISPATCH] establish that the `bed.c` event loop is a total serializer: every FEBE operation runs to full completion (parse → mutate → respond) before the next begins. Two sessions' operations never interleave. So the scenario reduces to exactly two orderings:

---

**Case 1: CREATELINK executes before DELETE**

At CREATELINK time, D's POOM still contains the target I-addresses. [ST-CREATE-LINK] shows the operation converts the target V-span to I-addresses via `vspanset2sporglset` → `vspanset2ispanset`, reads the current POOM, finds the addresses, and writes them to the spanfilade via `insertendsetsinspanf`. The spanfilade entries reference I-addresses that *were* present in D's POOM at creation time.

Session B's DELETE then executes. [ST-DELETE] and [INV-SPANF-WRITE-ONLY] confirm DELETE removes only POOM mappings — the spanfilade is never modified. L's entries now point to I-addresses that are no longer in D's POOM: the standard post-hoc orphan/ghost-link state [EC-GHOST-LINK]. The addresses were genuinely present when written; they were only removed afterward.

---

**Case 2: DELETE executes before CREATELINK**

At CREATELINK time, D's POOM no longer contains the target I-addresses. The conversion chain `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` searches D's POOM for the requested V-positions. [INV-ITOV-FILTERING] establishes this as a universal invariant: when `retrieverestricted` returns NULL for an I-address with no current POOM mapping, `span2spanset` silently drops it. The resulting sporglset contains only I-addresses *currently* present in D's POOM.

[ST-CREATE-LINK] then calls `insertendsetsinspanf` with this filtered sporglset. If the deletion removed all the target content, the sporglset is empty and nothing is written to the spanfilade. If some content survived the deletion (e.g., adjacent content shifted into the query range), only those surviving I-addresses are indexed.

In neither sub-case does the spanfilade acquire entries for I-addresses that were never in D's POOM.

---

### Summary

| Ordering | Spanfilade entries at L's endpoints | Were they ever in D's POOM? |
|---|---|---|
| CREATELINK → DELETE | Valid I-addresses, later orphaned | Yes — present at creation time |
| DELETE → CREATELINK | Only currently-present I-addresses (possibly none) | Yes — present at creation time |

The serialized execution guaranteed by [INV-ATOMICITY] means CREATELINK always observes a consistent POOM snapshot. The V-to-I filtering at [INV-ITOV-FILTERING] acts as a further gate: even if session A passed a V-span spec for content that no longer exists, the POOM lookup would return nothing rather than synthesizing phantom I-address entries.

The only scenario that *would* produce spanfilade entries for I-addresses outside D's POOM is the post-hoc orphan (Case 1), but those addresses were genuinely present at the moment of indexing — which is the expected behavior of an append-only spanfilade in a system with permanent but POOM-mutable content.

---

## Code Exploration

I now have all the source I need. Let me compile the complete answer.

---

## Answer: Serialization, V→I Translation, and the Race Impossibility

### 1. The Event Loop Provides True Run-to-Completion Serialization

`bed.c` implements a single-process, single-threaded `select()`-based event loop. There is no threading, no async, no coroutines.

```c
// bed.c:110-142
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        user = fdtoplayer[i];
        task.inp = player[user].inp;
        task.outp = player[user].outp;
        task.account = player[user].account;
        ...
        xanadu(&task);   // ← complete request before incrementing i
```

Even when both sessions A and B have data ready when `select()` returns, the inner `for (i = 0; ...)` loop processes them one at a time, sequentially. `xanadu()` [bed.c:153] calls `(*requestfns[request])(taskptr)` and only returns after `sendresultoutput` and `tfree` complete. **There is no point at which two handlers execute concurrently or interleave.** The scenario "session B deletes before A's operation completes" cannot occur mid-operation — one fully serializes before the other begins.

The only real question is ordering: does B's `deletevspan` run before or after A's `createlink`?

---

### 2. Deletion Touches Only the POOM, Not the Permascroll

`dodeletevspan` [do1.c:158-167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
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

`deletend` operates on `docorgl` — D's POOM (permutation matrix enfilade). It removes the V→I mapping nodes for the deleted span. The granfilade (permascroll) is untouched. **I-addresses in the permascroll are permanent and are never deleted.**

---

### 3. The V→I Translation Path in `docreatelink`

`docreatelink` [do1.c:195-221] translates A's V-address specset to I-address sporglsets at lines 214-216:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14-33] calls `vspanset2sporglset` [sporgl.c:35-65] for each `VSPECID` spec:

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    ispanset = NULL;
    if (!findorgl (taskptr, granf, docisa, &orgl, type))
        return (NULL);
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
        for (; ispanset; ispanset = ispanset->next) {
            sporglset = taskalloc(...);
            sporglset->itemid = SPORGLID;
            movetumbler(docisa, &sporglset->sporgladdress);
            movetumbler(&ispanset->stream, &sporglset->sporglorigin);
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);
            *sporglsetptr = sporglset;
            sporglsetptr = &sporglset->next;
        }
    }
    return (sporglsetptr);
}
```

The V→I translation uses `vspanset2ispanset` [orglinks.c:389-394] → `permute` [orglinks.c:404-422] → `span2spanset` [orglinks.c:425-454] → `retrieverestricted` [retrie.c:56-85] → `findcbcinarea2d` [retrie.c:229-268].

This is a **live query against D's current POOM tree**. It finds only those POOM nodes whose V-range intersects the requested V-span. `crumqualifies2d` [retrie.c:270-305] gates every node on actual position.

---

### 4. The Two Serialization Cases

**Case A: A's `createlink` runs first, B's `deletevspan` runs second**

`specset2sporglset` queries D's POOM, finds the nodes covering A's requested V-span, and returns valid I-addresses. These I-addresses were present in D's POOM at the moment of translation, and they are permanently in the granfilade. B later calls `deletend` on D's POOM, removing those V→I mapping nodes — but the I-addresses in L's spanfilade remain permanently valid. They correctly reflect content that *was* in D when the link was created. **No phantom references.**

**Case B: B's `deletevspan` runs first, A's `createlink` runs second**

`deletend` has already removed D's POOM nodes covering the target V-span. When A's `specset2sporglset` calls `retrieverestricted`, it finds **no matching nodes**. `span2spanset` [orglinks.c:446-448]:

```c
if(!context){
    return(targspansetptr);   // ← returns unchanged (empty) if no context
}
```

`vspanset2ispanset` returns an empty ispanset. The inner `for (; ispanset; ...)` loop in `vspanset2sporglset` [sporgl.c:49] never executes. `fromsporglset`/`tosporglset` remain NULL.

`insertendsetsinspanf` [do2.c:116-128] calls `insertspanf` [spanf1.c:15-53] with a NULL sporglset:

```c
for (; sporglset; sporglset = ...) {  // ← never enters loop
    insertnd(...);
}
return (TRUE);
```

Nothing is inserted into the spanfilade. `insertpm` [orglinks.c:100-133] similarly loops over the empty sporglset and inserts nothing into the link's POOM.

**L is created successfully (docreatelink returns TRUE), but with empty endpoint entries — no spanfilade insertions, no POOM entries for its endpoints.** A "ghost link": it has a valid ISA and occupies a V-slot in D's link subspace, but `findlinksfromtothree` will never return it, and `followlink` will fail to produce endpoints.

---

### 5. Could the Spanfilade Ever Contain I-Addresses "Never Present in D's POOM"?

**No.** The proof follows directly from the architecture:

1. **Serialization**: Only one handler executes at a time. B cannot interrupt A mid-execution.

2. **Translation is a live query**: `specset2sporglset` translates V→I against D's **current** POOM state at the instant A's request runs. Any I-address it produces was, by definition, present in D's POOM at that instant.

3. **Deletion doesn't retroactively contaminate**: After A's `insertendsetsinspanf` completes, the spanfilade contains I-addresses that correspond to what was in D's POOM at A's execution time. B's subsequent `deletend` cannot reach back and alter those spanfilade entries — the spanfilade has no back-pointer into the POOM.

4. **Empty result on miss**: If the V-addresses don't map to anything in D's POOM (because B already deleted them), `retrieverestricted` returns NULL, and **zero bytes are written to the spanfilade**. There is no fallback path that constructs a fabricated I-address.

The one pathological outcome is **Case B's ghost link**: a link with a valid ISA but no indexed endpoints. The design trades "link creation always succeeds" against "link endpoints may be empty if the content was concurrently deleted." This is a semantic hazard — the caller receives an `linkisa` back from `putcreatelink` with no indication the endpoints resolved to nothing — but it is categorically not the phantom-I-address scenario the question asks about. The spanfilade's consistency with the POOM is guaranteed by the serialized execution and the live V→I query.

---

## Question 16 [gregory]

> When a link's endset references I-addresses shared by three documents (original, version, and transclusion target), and the original document deletes that content, does `find_links` still discover the link from both the version and the transclusion target independently — confirming that link discovery is purely I-address intersection against the spanfilade with no provenance tracking back to the creating document?

### Gregory's Answer

## KB Synthesis

Yes — both the version and the transclusion target independently discover the link after the original's deletion, and the mechanism is purely I-address intersection with no provenance tracking.

## Why deletion from the original doesn't affect the other documents

DELETE modifies only the originating document's POOM [ST-DELETE, Finding 0064]. The V-to-I mappings for α are removed from O's POOM, but [FC-DELETE-CROSS-DOC] establishes the frame condition explicitly: `∀ D' ≠ D : delete(D, vspan) ⟹ poom(D') = poom_before(D')`. The version's POOM and the transclusion target's POOM are unchanged.

## Why the spanfilade still indexes the link

The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c`. The entries mapping α → link L, written by `insertendsetsinspanf` during `docreatelink`, persist unconditionally. DELETE has no call path into any spanfilade removal function [ST-DELETE, Finding 0057]:

> `DELETE (dodeletevspan → deletevspanpm → deletend)` — no code path touches the link orgl or spanfilade entries.

The invariant: `spanf_entries_after(DELETE) = spanf_entries_before(DELETE)`.

## How discovery works from V and T

`find_links` converts the query specset to I-addresses, then intersects against the spanfilade [SS-FIND-LINKS, Finding 0028]. Since V and T both retain POOM entries mapping V-positions to α, their content spans successfully convert to α, the spanfilade intersection returns link L, and the link is found. The original's deletion is irrelevant to either query.

This is confirmed by [INV-LINK-GLOBAL-VISIBILITY]:

> A link created in any document is discoverable from every document in the system that shares the linked content's identity.

And [INT-LINK-VERSION, Finding 0046]:

> Version creates text I-address sharing, and `find_links` operates in I-space via the spanf index — shared I-addresses cause the version to "inherit" link discoverability.

## No provenance tracking back to the creating document

This is confirmed by [EC-FIND-LINKS-GLOBAL] and [PRE-FIND-LINKS, Finding 0069]. The `sporglset2linkset()` function contains a `TRUE||!homeset` guard that permanently overrides whatever orgl-range (document-scoping) parameter the caller passes, replacing it with a hardcoded unbounded range. The orgl dimension filter — which was designed to restrict results to a particular document's links — is disabled. All `find_links` calls are effectively global searches in the orgl dimension, filtered only on the span dimension (I-address content matching).

The result: link discovery is exactly `{L | endpoint_iaddrs(L) ∩ query_iaddrs ≠ ∅}` — pure I-address set intersection against the spanfilade — with no regard for which document originally created the link or which document's POOM currently contains those I-addresses.

## Summary

After O deletes content at α:
- O's POOM: α unmapped → `find_links(O content)` returns `[]`
- V's POOM: α still mapped → `find_links(V content)` returns `{L}` ✓
- T's POOM: α still mapped → `find_links(T content)` returns `{L}` ✓
- Spanfilade: α → L entry intact, forever

Both documents independently confirm the link. The discovery requires only that the querying document's V-positions still map to α (providing the I-address for the spanfilade lookup) and that the spanfilade entry exists — neither of which is affected by O's deletion.

---

## Code Exploration

---

## Answer

**Yes — confirmed.** `find_links` discovers the link independently from both the version and the transclusion target after the original deletes that content. Link discovery is purely I-address intersection against the spanfilade with no provenance tracking. Here is the complete code-traced proof.

---

### 1. What the Spanfilade Stores at Link Creation

`docreatelink` [`do1.c:195-221`]:
```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, ...)
```

`insertspanf` [`spanf1.c:15-54`] — for each SPORGLID item in the sporglset:
```c
movetumbler(&((typesporgl *)sporglset)->sporglorigin, &lstream);   // I-address start
movetumbler(&((typesporgl *)sporglset)->sporglwidth,  &lwidth);    // I-address width
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);                // SPANRANGE key
// ORGLRANGE key = spantype-prefixed link ISA
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The spanfilade crum stores `(I-address range) → (link ISA)`. No V-address is stored. No creating-document identifier is stored in the key.

---

### 2. What DELETE Does — and Does Not Do

`dodeletevspan` [`do1.c:158-167`] → `deletevspanpm` [`orglinks.c:145-152`]:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` is called on `docorgl` — the *original document's own POOM* (2D enfilade in granf), operating in the `V` dimension. There is no call to any spanf function. There is no `deletespanf` function anywhere in the codebase (confirmed in Finding 0057 — the spanfilade is write-only).

**Effect:** The original document's V→I mapping for the deleted span is removed. The spanfilade entry `(I₁..I₂) → L` is permanently intact.

---

### 3. How find_links Converts the Query to I-Addresses

`dofindlinksfromtothree` [`do1.c:348-353`] → `findlinksfromtothreesp` [`spanf1.c:56-103`]:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

`specset2sporglset` → `vspanset2sporglset` [`sporgl.c:35-65`]:
```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return NULL;
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V→I via THIS doc's POOM
    // package as sporgls...
}
```

`docisa` here is the ISA of the **requesting document** — version V, or transclusion target T. `findorgl` retrieves *that document's* granfilade POOM. `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` maps V-positions to I-addresses using *that document's* POOM.

V's POOM was written at `docreatenewversion` time [`do1.c:260-298`] via `docopyinternal` which called `insertpm` — mapping V_v → I₁..I₂. T's POOM was written at `docopy` time mapping V_t → I₁..I₂. Neither POOM was touched by O's `deletevspanpm`. Both still map their V-addresses to I₁..I₂.

---

### 4. The Homedoc Provenance Filter Is Permanently Disabled

`sporglset2linksetinrange` [`sporgl.c:239-268`]:
```c
infoptr = &linfo;
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (FALSE/*trying to kluge links followable thru versions */
        && ((typeitemheader *)sporglset)->itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;        // ← always executed — infoptr is ALWAYS NULL
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, (typeisa*)infoptr);  // NULL always
```

The guard `if (FALSE && ...)` is dead code. The branch that would load a `homedoc` into `linfo` is unreachable. `infoptr` is always `NULL`.

The comment records a deliberate design choice: an attempt to filter by source document was tried ("trying to kluge links followable thru versions") and then abandoned by hardcoding `FALSE`.

The downstream enforcement point is `findcbcinarea2d` [`retrie.c:274-280`]:
```c
if ((crumptr->height == 0) && infoptr
    && !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
    return (FALSE);
}
```

With `infoptr == NULL`, the `&& infoptr` short-circuits to false and the homedoc equality check is **never reached**. The spanfilade traversal returns every crum whose I-address range intersects the query, regardless of which document was the "source" when the link was created.

---

### 5. State After O Deletes Its Content

| Data Structure | State |
|---|---|
| O's POOM (granf) | V→I entry for deleted span: **removed** by `deletend` |
| V's POOM (granf) | V→I entry for same I₁..I₂: **intact** — different `docorgl` pointer |
| T's POOM (granf) | V→I entry for same I₁..I₂: **intact** — different `docorgl` pointer |
| Spanfilade entry | `SPANRANGE[I₁..I₂] → L (LINKFROMSPAN)`: **intact, permanent** |

`find_links` queried with V's V-addresses: V's POOM maps V_v → I₁..I₂ → sporglset non-empty → spanfilade query succeeds → **L found**.

`find_links` queried with T's V-addresses: T's POOM maps V_t → I₁..I₂ → sporglset non-empty → spanfilade query succeeds → **L found**.

`find_links` queried with O's (now-deleted) V-addresses: O's POOM has no mapping → `vspanset2ispanset` returns nothing → sporglset empty → nothing queried → **L not found** (not because of a provenance check, but because the V→I translation returns an empty set).

---

### Conclusion

The answer to both parts of the question is **yes**:

1. **`find_links` discovers the link from both V and T independently after O deletes the content.** The delete modifies only O's POOM. The spanfilade is permanent and untouched. V's and T's POOMs remain intact, so their V→I conversion still produces I₁..I₂, which the spanfilade matches to L.

2. **This confirms that link discovery is purely I-address intersection against the spanfilade with no provenance tracking.** The one code path that could have introduced provenance filtering — the `infoptr`/homedoc check at `sporgl.c:251` — is permanently dead via `if (FALSE && ...)`. The spanfilade stores I-address ranges as keys; retrieval is purely geometric intersection in I-space. No "creating document", "current hosting document", or "version lineage" participates in the query.

The author's own comment at `sporgl.c:251` — *"trying to kluge links followable thru versions"* — is the fossil record of the moment this property was explicitly chosen: the filter was attempted, found to break cross-transclusion link discovery, and disabled.

---

## Question 17 [gregory]

> If DELETEVSPAN is applied to a link's V-position in subspace `2.x` (creating a "reverse orphaned" link), and then new content is inserted whose I-addresses happen to overlap with the deleted link's endset I-spans, does `find_links` on that new content still discover the reverse-orphaned link through the spanfilade — even though the link has no POOM entry in any document?

### Gregory's Answer

## KB Synthesis

Yes — with a critical qualification about what "new content is inserted whose I-addresses happen to overlap" can mean in practice.

## The Premise Is Physically Unreachable for INSERT

Fresh INSERT cannot produce I-addresses that overlap with the reverse-orphaned link's endpoint I-spans. I-address allocation is strictly monotonically increasing and addresses are never reused [INV-NO-IADDR-REUSE], [INV-MONOTONIC]. `findisatoinsertmolecule` always queries the granfilade for its current maximum and increments by 1 — since the link's endpoint I-addresses are already in the granfilade, any new INSERT will allocate strictly higher addresses. The overlap scenario is structurally impossible for INSERTed content.

## But VCOPY Can Reach Those I-Addresses

VCOPY (transclusion) copies existing I-addresses into a new document's POOM without allocating new ones [ST-VCOPY]. If content sharing the link's endpoint I-spans is transcluded into any document, `find_links` on that document will discover the reverse-orphaned link.

## The Answer: Yes, the Link Is Discovered via the Spanfilade

This is the defining property of the reverse-orphaned state [EC-REVERSE-ORPHAN]. When DELETEVSPAN removes a link from the 2.x subspace, it modifies only the POOM layer — the link orgl in I-space and the spanfilade entries are completely untouched [SS-THREE-LAYER-MODEL]:

> `DELETEVSPAN(2.x)` → POOM entry removed; I-space link orgl unchanged; spanfilade entries unchanged.

From [INV-SPANF-WRITE-ONLY]: no operation ever removes spanfilade entries. The spanfilade maps `link_endpoint_I-addresses → link_ISA` and this mapping persists indefinitely.

`find_links` operates entirely in I-space via the spanfilade [SS-FIND-LINKS]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

It has no dependency on whether the link has a POOM entry in any document. So if a document's content shares I-addresses with the reverse-orphaned link's endpoint I-spans (via VCOPY of the original content), `find_links` will discover the link.

## Concrete Scenario

```
1. Create link L with source endpoint at I-addresses α₁..α₃
   → spanfilade: α₁..α₃ → (L, LINKFROMSPAN)  [ST-CREATE-LINK]
   → document D POOM: V:2.1 → link ISA  [SS-THREE-LAYER-MODEL]

2. DELETEVSPAN(D, 2.1)
   → D POOM: V:2.1 entry removed
   → spanfilade: α₁..α₃ → (L, LINKFROMSPAN)  UNCHANGED  [FC-LINK-DELETE-ISOLATION]
   → L is now "reverse orphaned"  [EC-REVERSE-ORPHAN]

3. VCOPY α₁..α₃ into new document D'
   → D' POOM: some V-positions mapped to α₁..α₃  [ST-VCOPY]

4. find_links(D', span covering α₁..α₃)
   → converts V-span to I-span α₁..α₃  [INT-SPORGL-LINK-INDEX]
   → spanfilade lookup: α₁..α₃ matches entry for L
   → returns [L]  ✓
```

The link's POOM absence is irrelevant to `find_links` because discovery is purely an I-address intersection query against the spanfilade [SS-SPANF-OPERATIONS], [INT-LINK-TRANSCLUSION]. The reverse-orphaned state does not reduce the link's discoverability — it only removes the link from `retrieve_vspanset` output for its former home document.

---

## Code Exploration

I now have all the code and prior findings needed to answer definitively. Here is the complete analysis.

---

## Answer: Yes — the Reverse-Orphaned Link Is Still Discoverable

The short answer is **yes**: `find_links` on new content whose I-addresses overlap with a reverse-orphaned link's endset I-spans **will** discover the link through the spanfilade. The link has no POOM entry in any document, but that is irrelevant to how link discovery works. Here is the complete code-traced explanation.

---

### Part 1 — What DELETEVSPAN Does and Does Not Touch

`dodeletevspan` in `do1.c:158-167`:

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

It calls `deletevspanpm` in `orglinks.c:145-152`:

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

This calls `deletend` on `docorgl` — the document's **POOM enfilade** in granf. It removes the V-to-I crums that cover the specified V-range (in this case, the link's 2.x address).

**Critically: nothing else is called.** There is no call to any spanfilade function. The code path terminates at `deletend` on the POOM.

---

### Part 2 — What the Spanfilade Holds and How It Got There

When `docreatelink` runs in `do1.c:195-221`, it does two things relevant here:

**Step A** — puts the link's ISA into the document's POOM (the entry that DELETEVSPAN later removes):
```c
docopy(taskptr, docisaptr, &linkvsa, ispanset)  // [do1.c:212]
```

**Step B** — inserts the link's endset I-spans into the global spanfilade:
```c
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // [do1.c:219]
```

`insertendsetsinspanf` in `do2.c:116-128` calls `insertspanf` three times:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

`insertspanf` in `spanf1.c:15-54` inserts 2D nodes into the spanfilade with:
- **ORGLRANGE axis** = the link ISA tumbler, prefixed with the spantype code (1, 2, or 3)
- **SPANRANGE axis** = the I-address of the endset content

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // [spanf1.c:51]
```

These entries encode: *"At I-address `lstream..lstream+lwidth`, link `linkisaptr` has an endset of type `spantype`."*

**DELETEVSPAN never touches these entries.** There is no `deletespanf` function anywhere in the codebase — inspection of `spanf1.c` and every file that calls spanfilade functions confirms only insertion and query functions exist (`insertspanf`, `findlinksfromtothreesp`, `retrieveendsetsfromspanf`, `finddocscontainingsp`, `retrievesporglsetinrange`). The spanfilade is write-once.

---

### Part 3 — How `find_links` Queries the Spanfilade

The call chain: `findlinksfromtothree` [fns.c:189] → `dofindlinksfromtothree` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103].

`dofindlinksfromtothree` in `do1.c:348-353`:
```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
  bool findlinksfromtothreesp();
  return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, ...);
}
```

`findlinksfromtothreesp` in `spanf1.c:56-103`:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // [spanf1.c:71]
...
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);  // [spanf1.c:77]
    ...
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // [spanf1.c:100]
```

**Step A: `specset2sporglset`** converts the query V-specset (the new content's V-address in its document) into a sporglset (I-address range). This goes through `vspanset2sporglset` in `sporgl.c:35-65` → `vspanset2ispanset` in `orglinks.c:397-402` → `permute` → `span2spanset` → `retrieverestricted` on the **query document's POOM**. The new content IS in its document's POOM (it was just inserted), so this conversion succeeds. The reverse-orphaned link's POOM deletion is irrelevant here — a different document is being queried.

**Step B: `sporglset2linkset`** in `sporgl.c:222-237` calls `sporglset2linksetinrange` in `sporgl.c:239-269`:

```c
int sporglset2linksetinrange(typetask *taskptr, typecuc *spanfptr,
    typesporglset sporglset, typelinkset *linksetptr,
    typeispan *orglrange, INT spantype)
{
  ...
  for (; sporglset; ...) {
    ...
    context = retrieverestricted(spanfptr,
        (typespan*)sporglset, SPANRANGE,   // restrict by I-address
        &range,              ORGLRANGE,    // restrict by spantype prefix
        (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);  // collect link ISA
    }
    contextfree(context);
  }
}
```

This calls `retrieverestricted` in `retrie.c:56-85`, which calls `retrieveinarea` → `findcbcinarea2d`, a recursive enfilade walk over the **spanfilade** (not any POOM). The 2D qualification is:
- SPANRANGE must overlap with the query I-addresses (the new content's I-spans)
- ORGLRANGE must fall within the spantype-prefixed range (LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN)

If the new content's I-addresses overlap with the reverse-orphaned link's endset I-spans, `findcbcinarea2d` in `retrie.c:229-268` will traverse to those spanfilade bottom-crums — because they are still there — and `crumqualifies2d` in `retrie.c:270-305` will return TRUE. The link ISA is extracted via `beheadtumbler` and placed in the result list.

**No POOM check of any kind appears in this path.** The function never asks "does the link have a 2.x entry in any document's POOM?" It only asks "does the spanfilade contain an entry at this I-address range with this spantype prefix?"

---

### Part 4 — The ORGLRANGE Prefix Namespace Separation

One subtlety worth noting: the spanfilade serves double duty — it indexes both link endsets (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) and document transclusion containment (DOCISPAN=4). These do not interfere because `prefixtumbler` in `insertspanf` and the `prefixtumbler`-based range restriction in `sporglset2linksetinrange` ensure that link discovery queries (`spantype=1,2,3`) never accidentally match document containment entries (`spantype=4`), and vice versa. The reverse-orphaned link's entries at `spantype=1,2,3` remain in the spanfilade at their original I-spans, correctly namespaced.

---

### Part 5 — Summary of the Two Enfilades

| Structure | What it stores | Modified by DELETEVSPAN? | Consulted by `find_links`? |
|-----------|---------------|--------------------------|---------------------------|
| **POOM** (per-document orgl in granf) | V→I mapping for document content and links | **Yes** — `deletend` removes the 2.x entry | **Only to convert query V-addresses to I-addresses** (query doc's POOM, not link's home doc) |
| **Spanfilade** (global spanf) | I-address → link ISA mappings, all endset types | **No** — no deletion function exists | **Yes** — the primary mechanism for link discovery |

---

### Conclusion

**Yes, `find_links` will discover the reverse-orphaned link.**

The complete code path for why:

1. `DELETEVSPAN` on a link's 2.x V-position only calls `deletevspanpm` → `deletend` on the document's POOM **[`do1.c:158-167`, `orglinks.c:145-152`]**. The spanfilade is untouched.

2. The link's endset I-spans were permanently inscribed in the spanfilade at creation time via `insertendsetsinspanf` → `insertspanf` → `insertnd` **[`do1.c:219`, `do2.c:116-128`, `spanf1.c:15-54`]**. No deletion function for the spanfilade exists **[`spanf1.c` entire file]**.

3. `find_links` calls `findlinksfromtothreesp` → `sporglset2linkset` → `sporglset2linksetinrange` → `retrieverestricted` on the spanfilade **[`do1.c:348-353`, `spanf1.c:56-103`, `sporgl.c:222-269`]**. This is a pure I-address lookup against the spanfilade. No POOM existence check is performed for the link or its home document at any point in this path.

4. If the new content's I-addresses (obtained by converting V-addresses via the query document's own POOM) overlap with the reverse-orphaned link's endset I-spans, `findcbcinarea2d` **[`retrie.c:229-268`]** will traverse the spanfilade and return the link ISA.

The link's absence from any document's POOM is invisible to this query path. The spanfilade is a permanent, write-only index — it records every link endset ever registered, independent of POOM state. This is confirmed and documented in **Finding 0040** (link removal from POOM, find_links still works) and **Finding 0057** (spanfilade entries not cleaned up on DELETE).

---

## Question 18 [gregory]

> When INSERT at position V:1.3 in a document shifts text content rightward via `makegappm`, and a link L has source endset referencing I-addresses of that shifted content, does `FOLLOWLINK` on L resolve the endset to the new V-positions (post-shift) by performing a fresh I-to-V lookup through the POOM, or does it cache any V-position from link creation time?

### Gregory's Answer

## KB Synthesis

**FOLLOWLINK performs a fresh I-to-V lookup through the current POOM — it always resolves to post-shift V-positions, never cached creation-time positions.**

## Mechanism

The resolution chain is documented in [SS-FOLLOWLINK] (Finding 0048):

1. `link2sporglset()` extracts the endset's I-addresses from the link orgl in I-space — these are permanent and unchanged by any edit
2. `linksporglset2specset()` converts those I-addresses to V-addresses by looking them up in the **specified document's current POOM**

The POOM is not read-only; it is the sole mutable layer [SS-POOM-MUTABILITY]. After INSERT at V:1.3, `makegappm` shifts all POOM entries in `[1.3, 2.1)` rightward by the insertion width [ST-INSERT, Finding 0054] — so the entry that previously mapped V:1.5 → I_content now maps V:1.8 → I_content. When FOLLOWLINK later resolves I_content through that POOM, it finds V:1.8, not the stale V:1.5.

## Empirical Confirmation

[INV-LINK-CONTENT-TRACKING] (Finding 0019) provides direct evidence:

> **V-address shifts**: When content is inserted within or before a linked region, the endset V-addresses shift to reflect the new positions:
> - Before: link on "here" at V 1.7 width 0.4
> - Insert "right " at position 1.7
> - After: link reports **1.13 width 0.4**

## Why No Caching Is Possible

Three interlocking properties make any V-position cache incorrect:

| Property | Entry |
|----------|-------|
| I-addresses never change after allocation | [INV-IADDR-IMMUTABILITY] |
| INSERT shifts V-positions in current POOM, leaves I-addresses untouched | [FC-INSERT-IADDR] |
| I-to-V filtering always goes through current POOM | [INV-ITOV-FILTERING] |

The link orgl stores I-addresses as its permanent reference point. V-positions are strictly derived, always computed live from the current POOM state. If a link's endpoint I-addresses have no current POOM mapping (e.g., after deletion), FOLLOWLINK silently returns empty — demonstrating it consults the POOM at call time, not at creation time [EC-GHOST-LINK].

## Clarification on Finding 0028

[SS-LINK-ENDPOINT] (Finding 0028) says "link endpoints are immutable V-spans fixed at creation time" and "follow_link always returns the original VSpan." This describes the *stored link data structure* — the link orgl itself does not update. What [SS-FOLLOWLINK] shows is that FOLLOWLINK doesn't return the stored V-span directly; it re-derives V-positions from stored I-addresses through the current POOM. The stored I-addresses are immutable; the V-positions derived from them are not.

---

## Code Exploration

Now I have everything needed to trace the full execution path. Here is the complete answer.

---

## Does FOLLOWLINK cache V-positions or perform a fresh I-to-V lookup?

**Answer: FOLLOWLINK performs a completely fresh I-to-V lookup through the POOM at follow time. No V-position is ever cached in a link.**

The architecture has three phases. Here is each one traced to specific lines.

---

### Phase 1: Link Creation — I-Addresses Are What Gets Stored

`docreatelink` [do1.c:195–221] does:

```c
specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // do1.c:214
insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)  // do1.c:218
insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)          // do1.c:219
```

`specset2sporglset` [sporgl.c:14–33] converts the client's specset. If the client sent V-spans (`VSPECID`), it calls `vspanset2sporglset` [sporgl.c:35–65], which converts them immediately to I-addresses at creation time:

```c
(void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);   // sporgl.c:48
// then for each ispan:
movetumbler (docisa, &sporglset->sporgladdress);          // sporgl.c:53 — document ISA
movetumbler (&ispanset->stream, &sporglset->sporglorigin); // sporgl.c:54 — I-address
movetumbler (&ispanset->width, &sporglset->sporglwidth);   // sporgl.c:55 — I-width
```

`vspanset2ispanset` [orglinks.c:397–402] calls `permute(..., V, ..., I)` [orglinks.c:404–422], which calls `retrieverestricted` on the POOM to read the current V→I mapping. The returned I-addresses are what get stored.

**What is stored in the link's ORGL:** `sporglorigin` (I-address) and `sporglwidth` (I-width) per endset entry. The link's own virtual address space uses positions like `1.x` (from-end), `2.x` (to-end), `3.x` (three-end) on the V-axis. The I-axis holds the I-addresses of the referenced content. **No V-position of the target content is persisted.**

---

### Phase 2: INSERT and makegappm — What Changes

`insertnd` [insertnd.c:15–111], when the enfilade is a POOM, calls `makegappm` first [insertnd.c:54]:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // insertnd.c:54
    // ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
```

`makegappm` [insertnd.c:124–172] makes two cuts at the insertion point, then walks the children:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 1:  /* crum is to the right of the cut — must shift */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // insertnd.c:162
        ivemodified (ptr);
        break;
    }
}
```

Only `cdsp.dsas[V]` — the V-dimension displacement — is modified. `cdsp.dsas[I]` (the I-dimension) is **untouched**. I-addresses are permanent identifiers for content; they never shift. The POOM now reflects a new V→I mapping: the same I-addresses are reached by higher V-addresses than before.

---

### Phase 3: FOLLOWLINK — The Fresh Lookup

`followlink` [fns.c:114–127] calls `dofollowlink` [do2.c:223–232]:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl*)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
```

**Step 3a — `link2sporglset` [sporgl.c:67–95]:** Queries the link's own ORGL to recover the stored I-addresses:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // sporgl.c:81 — select from/to/three
tumblerincrement (&zero, 0, 1, &vspan.width);           // sporgl.c:82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL))
    // sporgl.c:83
```

For each context result:

```c
contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);  // sporgl.c:86
```

`contextintosporgl` [sporgl.c:205–220] extracts:
```c
movetumbler (&context->totaloffset.dsas[I], &sporglptr->sporglorigin);  // sporgl.c:211 — I-address
movetumbler (&context->contextwid.dsas[I], &sporglptr->sporglwidth);    // sporgl.c:219 — I-width
```

After this step: we have the same I-addresses that were stored at link creation time. Nothing else.

**Step 3b — `linksporglset2specset` [sporgl.c:97–123]:** For each sporgl with a non-zero `sporgladdress`, calls:

```c
linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);  // sporgl.c:116
```

`linksporglset2vspec` [sporgl.c:127–137] → `sporglset2vspanset` [sporgl.c:141–176]:

```c
(void) findorgl (taskptr, granf, homedoc, &orgl, type);  // sporgl.c:152 — opens target doc's POOM
// builds ispan from sporglorigin/sporglwidth, then:
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);  // sporgl.c:157
```

`ispan2vspanset` [orglinks.c:389–394]:
```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);  // orglinks.c:393
```

`permute` [orglinks.c:404–422] → `span2spanset` [orglinks.c:425–454]:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanset, I,
                              (typespan*)NULL, V, (typeisa*)NULL);  // orglinks.c:435
```

**This is a live query into the target document's POOM.** It asks: "given these I-addresses, what V-addresses do they correspond to right now?" Because `makegappm` has already updated `cdsp.dsas[V]` on the shifted crums, `retrieverestricted` will now return the **post-insertion V-positions**.

---

### Summary

| Phase | Operation | V stored? | I stored? |
|-------|-----------|-----------|-----------|
| `docreatelink` | `vspanset2ispanset` converts client V→I at creation time | No | Yes (`sporglorigin`, `sporglwidth`) |
| `makegappm` on INSERT | Shifts `cdsp.dsas[V]` in target POOM | POOM updated | Unchanged |
| `dofollowlink` | `link2sporglset` reads stored I-addresses; `ispan2vspanset` queries live POOM | Computed fresh | Read from link |

The link's endset stores **only I-addresses** (`sporglorigin`/`sporglwidth`) in its ORGL. V-positions are **never cached**. At follow time, `ispan2vspanset` → `permute` → `retrieverestricted` performs a completely fresh I→V lookup through the current state of the target document's POOM, so any shifts caused by `makegappm` are automatically reflected. The invariance of I-addresses is the mechanism that makes links stable across insertions: the content is always found by its permanent I-address, and the current V-position is always computed on demand.

---

## Question 19 [gregory]

> Does the spanfilade entry for a link's endset record the document ID where the link was created, and if the link's home document is itself deleted from the POOM (all content removed), do the spanfilade endset entries for that link remain fully intact — meaning the link is discoverable from any other document sharing those I-addresses regardless of the creating document's state?

### Gregory's Answer

## KB Synthesis

## Spanfilade Endset Entries and Home Document Deletion

**What the spanfilade endset entries record:**

The spanfilade endset entries record the `sporgladdress` field from each sporgl — this is the ISA of the document *containing the endpoint content* at link creation time, not necessarily the home document [SS-SPORGL]. As [INT-SPORGL-LINK-INDEX] confirms, the provenance field is stored so link retrieval can reconstruct which document each endpoint references. The home document determines where the link orgl's *address is allocated* [SS-LINK-HOME-DOCUMENT], which is a separate concern from where the endpoint content lives.

**On spanfilade survival when the home document loses all content:**

Yes — the spanfilade endset entries remain fully intact. Three independent lines of evidence:

1. **The spanfilade is write-only.** No delete function exists anywhere in `spanf1.c` or `spanf2.c` [INV-SPANF-WRITE-ONLY]. No operation can remove a spanfilade entry once created.

2. **DELETE operates only on the POOM layer.** `deletevspanpm` calls only `deletend` (granf/POOM) and `logbertmodified` — there is no call to any spanf removal function [FC-LINK-DELETE-ISOLATION], [ST-DELETE]. The spanfilade frame condition for DELETE is explicit: `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before` [ST-DELETE Finding 0057].

3. **This specific scenario is directly confirmed.** [FC-LINK-PERSISTENCE] Finding 0024 explicitly tests and verifies: "Deleting all text from the home document has zero effect on link functionality — the link's source, target, and type endsets remain fully operational." The three-layer model [SS-THREE-LAYER-MODEL] formalizes this: `DELETEVSPAN` only removes POOM entries; I-space and spanfilade are structurally independent.

**Discoverability from other documents:**

Link discovery is purely content-identity-based — `find_links` converts V-spans to I-addresses then searches the spanfilade [SS-FIND-LINKS]. Since the spanfilade entries are intact, any document sharing the endpoint I-addresses (via transclusion or versioning) will discover the link regardless of the home document's POOM state [INV-LINK-GLOBAL-VISIBILITY], [INT-LINK-TRANSCLUSION].

**One caveat:** If the endpoint content itself was also removed from *all* documents (not just the home document), FOLLOWLINK would return empty results at the I-to-V conversion step [INV-ITOV-FILTERING], [EC-GHOST-LINK] — but the link remains discoverable from documents still holding those I-addresses. The home document's state is orthogonal to this.

---

## Code Exploration

I now have everything I need. Let me compile the full answer.

---

## Full Answer

### 1. What Does the Spanfilade Entry for a Link's Endset Actually Record?

**The entry records the link's own ISA — not the creating document's ISA.**

Trace from `docreatelink` [`do1.c:195`]:

```c
// do1.c:207-219
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // allocate link's ISA
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)         // plant link in creating doc's POOM
  && ...
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl (...)
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
);
```

`insertendsetsinspanf` [`do2.c:116`] calls `insertspanf` with `linkisaptr` three times:

```c
// do2.c:116-128
bool insertendsetsinspanf(..., typeisa *linkisaptr, ...)
{
  insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // LINKFROMSPAN = 1
  insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // LINKTOSPAN   = 2
  insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // LINKTHREESPAN= 3
}
```

Inside `insertspanf` [`spanf1.c:15`], the `isaptr` argument is `linkisaptr`:

```c
// spanf1.c:22-51
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // ORGLRANGE key = prefix(linkISA, FROM|TO|THREE)
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
...
for (; sporglset; ...) {
    if (itemid == SPORGLID) {
        movetumbler (&sporgl->sporglorigin,  &lstream);        // SPANRANGE = I-address of endset
        movetumbler (&sporgl->sporglwidth,   &lwidth);
        movetumbler (&sporgl->sporgladdress, &linfo.homedoc);  // homedoc = doc that holds that V-span
    }
    ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Each spanfilade crum for a link's endset stores:

| Field | Value | Source |
|-------|-------|--------|
| `ORGLRANGE` | `prefixtumbler(linkISA, 1|2|3)` | link's own ISA, prefixed by endset slot |
| `SPANRANGE` | I-address + width of endset content | from `sporglorigin`/`sporglwidth` |
| `linfo.homedoc` | ISA of the doc whose V-span maps to that I-address | from `sporgladdress` set by `vspanset2sporglset` [`sporgl.c:53`] |

`prefixtumbler` [`tumble.c:641`] prepends `bint` (1/2/3) as the leading digit of the link's ISA tumbler; this makes the ORGLRANGE key `<FROM|TO|THREE>.<link-account>.<link-doc>.<link-atom>`.

**The creating document's ISA does not appear in ORGLRANGE.** The `homedoc` crum field stores the ISA of whichever document's POOM maps the referenced V-address — which may or may not be the creating document, depending on where the link's endsets point.

---

### 2. What Happens When the Creating Document's Content Is Deleted?

`dodeletevspan` [`do1.c:158`]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm` [`orglinks.c:145`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // operates on docorgl only
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [`edit.c:31`] receives `(typecuc*)docorgl` as its first argument — the POOM node for that document. It performs all operations (cuts, disown, subtreefree, tumblersub) on that tree only. **`spanf` (the spanfilade) is never passed to `deletend` and is never modified by any code in the deletion chain.**

There is no call to `insertspanf`, no call to any spanfilade-writing function, anywhere in the path from `deletevspan` → `dodeletevspan` → `deletevspanpm` → `deletend`.

---

### 3. Link Discovery Is Blind to the Creating Document's State

When another document queries for links touching its I-addresses, `findlinksfromtothreesp` [`spanf1.c:56`] → `sporglset2linkset` [`sporgl.c:222`] → `sporglset2linksetinrange` [`sporgl.c:239`]:

```c
// sporgl.c:250-265
for (; sporglset; ...) {
    if (FALSE /*trying to kluge links followable thru versions*/
        && itemid == SPORGLID) {
        infoptr = &linfo;
        movetumbler(&sporgl->sporgladdress, &linfo.homedoc);
    } else
        infoptr = NULL;  // ← always reached due to `FALSE ||`

    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE,
                                 (typeisa*)infoptr);   // infoptr == NULL → no homedoc filter
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);  // strip prefix → extract link ISA
        onlinklist(taskptr, linksetptr, &linksa);
    }
}
```

The `if (FALSE || ...)` guard forces `infoptr = NULL` unconditionally — the `homedoc` field stored in each spanfilade crum is **never used as a filter** during link retrieval. Discovery is keyed purely on:
1. **SPANRANGE**: the I-address of the queried content
2. **ORGLRANGE**: the endset-type prefix range (`LINKFROMSPAN`=1, `LINKTOSPAN`=2, `LINKTHREESPAN`=3)

The link's ISA is then recovered by stripping the prefix off the ORGLRANGE value with `beheadtumbler`.

---

### Summary

**Part 1:** The spanfilade endset entry records the **link's own ISA** in ORGLRANGE (prefixed by endset slot number). The `homedoc` field records the ISA of the document whose V-space maps the referenced I-address — not the creating document's ISA per se (though they coincide when the endset points into the creating document). The creating document is **not** the keying identity in the spanfilade record.

**Part 2:** Yes — the spanfilade endset entries remain **fully intact** if the creating document's POOM content is deleted. `deletevspan` → `deletend` operates exclusively on `docorgl` (the document's enfilade subtree); `spanf` is never touched. Link discovery via `sporglset2linksetinrange` searches by I-address alone, with `homedoc` filtering disabled (`FALSE ||` at `sporgl.c:251`). Any document sharing those I-addresses will continue to find the link through the spanfilade, with no dependency on the creating document's POOM state.

---

## Question 20 [gregory]

> When a link has a source endset spanning I-addresses `[i, i+10)` and a COPY transcludes only `[i+3, i+7)` into a target document, does `find_links` on the target document match L because the partial I-address overlap is sufficient, and does the returned endset for L show all three endsets (source, target, type) in full or only the overlapping portion of the queried endset?

### Gregory's Answer

## KB Synthesis

## Short answer

Yes, the partial overlap suffices for `find_links`. The **stored** endsets are always complete and immutable; what you get back when *resolving* them depends on which document context is used for I→V conversion.

---

## Part 1: Does partial overlap match?

Yes. `find_links` uses non-empty I-address intersection as its sole criterion:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

[SS-FIND-LINKS] (Finding 0028) gives the canonical example: a link on "DEF" (`I.4–I.6`) is discovered by a document containing only "EF" (`I.5–I.6`). Partial overlap is sufficient; there is no minimum-coverage threshold.

In the question's case: source endset is `[i, i+10)`, target POOM has `[i+3, i+7)`. Intersection is `[i+3, i+7)` ≠ ∅ → L is found. [SS-FIND-LINKS], [INT-LINK-TRANSCLUSION]

---

## Part 2: What the endsets show

Two distinct questions are embedded here: what is *stored* vs. what is *returned* in a given resolution context.

### Stored endsets: always complete

The link orgl contains the full endsets as specified at `create_link` time. No operation modifies them. [INV-LINK-PERMANENCE], [SS-LINK-ENDPOINT] (Finding 0028):

> "Link endpoints are immutable V-spans fixed at creation time."

All three endsets — source `[i, i+10)`, target, type — are stored in full and never trimmed.

### Resolved endsets: filtered by POOM context

[SS-FOLLOWLINK] (Finding 0048) describes the actual mechanism:

> `link2sporglset()` extracts I-addresses from the link orgl. Then `linksporglset2specset()` converts I-addresses to V-addresses by looking them up in the specified `homedoc`'s POOM. If an I-address has no POOM mapping, it is **silently dropped** — no V-span is added to the result.

This is the universal I→V filtering invariant [INV-ITOV-FILTERING]:

> `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i ∧ i ∈ dom.ispace`

So the resolution outcome depends on context:

| Call | Context | Source endset returned |
|------|---------|----------------------|
| `follow_link(L, SOURCE, source_doc)` | source doc POOM has all `[i, i+10)` | Full `[i, i+10)` |
| `follow_link(L, SOURCE, target_doc)` | target doc POOM has only `[i+3, i+7)` | Partial: only those 4 bytes |
| `retrieve_endsets(target_vspan)` | resolves in target's V-space | Only `[i+3, i+7)` portion |

[SS-RETRIEVE-ENDSETS] (Finding 0035) makes the context-dependence explicit:

> "Key: endsets are resolved in terms of the querying document's V-space, not the link's home document."
> "The same link endset can produce different V-address results (or empty results) depending on which document context is used."

### The `follow_link` full-endset behavior in Finding 0028

[SS-FOLLOW-LINK] states: "Even when a link is found via partial I-address overlap, `follow_link` returns the full endpoint as it was specified at link creation time." This holds when the resolution context is the **source/home document** (which has all the I-address POOM mappings). The FEBE-level `follow_link` call uses the link's home document as resolution context by default, so the client sees the complete original specset — `retrieve_contents` on that result returns the full "hyperlink text" (14 chars), not the 4-char "link" that enabled discovery.

### Target and type endsets

These are unaffected by the partial transclusion. Their I-addresses live in other documents' POOMs. Resolution of the target endset depends on whether the target document is open and has those POOM mappings; the type endset resolves against the bootstrap document. Neither is filtered or shortened by the fact that only a partial source endset was transcluded. [SS-LINK-ENDPOINT], [FC-LINK-PERSISTENCE]

---

## Summary

- **Discovery**: `find_links` on the target matches L — partial I-address overlap `[i+3, i+7) ∩ [i, i+10)` is non-empty, which is sufficient. [SS-FIND-LINKS]
- **Stored endsets**: All three (source, target, type) are stored in full in the link orgl, permanently and immutably. [INV-LINK-PERMANENCE]
- **Resolved source endset from target doc**: Only the 4-byte overlapping portion `[i+3, i+7)` is returned, because only those I-addresses have V-position mappings in the target's POOM. The remaining `[i, i+3)` and `[i+7, i+10)` are silently dropped. [SS-FOLLOWLINK], [INV-ITOV-FILTERING]
- **Resolved source endset from source doc**: The full 10-byte range `[i, i+10)` is returned. [SS-FOLLOW-LINK]
- **Target and type endsets**: Returned in full, subject to their own document's POOM state, unaffected by the partial transclusion. [SS-LINK-ENDPOINT]

---

## Code Exploration

I have now traced the complete execution path through the source. Here is the full answer.

---

## Answer: `find_links` with Partial I-address Overlap

### Part 1 — Does `find_links` match L?

**Yes. Partial I-address overlap is sufficient.**

The call chain is:

```
find_links (fns.c:189)
  → dofindlinksfromtothree (do1.c:348-353)
  → findlinksfromtothreesp (spanf1.c:56-103)
  → sporglset2linkset (sporgl.c:222-237)
  → sporglset2linksetinrange (sporgl.c:239-269)
  → retrieverestricted (retrie.c:56-85)
  → findcbcinarea2d (retrie.c:229-268)
  → crumqualifies2d (retrie.c:270-305)
```

**Step-by-step:**

1. **V-to-I translation.** `findlinksfromtothreesp` converts the target-document V-spec (the range that covers the transcluded content) to I-spans via `specset2sporglset` → `vspanset2sporglset` → `vspanset2ispanset`. Because COPY preserves I-addresses, the target document's V-range maps to exactly `[i+3, i+7)` in permascroll space.

2. **Spanfilade query.** `sporglset2linksetinrange` (sporgl.c:239-269) calls:

   ```c
   prefixtumbler(&orglrange->stream, spantype, &range.stream);  // range = LINKFROMSPAN prefix
   context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, infoptr);
   ```

   - SPANRANGE restriction = `[i+3, i+7)` (the transcluded I-span)
   - ORGLRANGE restriction ≈ `[LINKFROMSPAN=1, LINKFROMSPAN+1=2)`

3. **The overlap test.** The match decision lives in `crumqualifies2d` (retrie.c:270-305):

   ```c
   endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
   if (endcmp <= ONMYLEFTBORDER) return FALSE;     // query ends before crum starts
   startcmp = whereoncrum(crumptr, offset, span1start, index1);
   if (startcmp > THRUME) return FALSE;            // query starts after crum ends
   ```

   This is a standard half-open interval intersection test: a crum at `[i, i+10)` qualifies if the query endpoint `i+7` is after `i` (endcmp = THRUME, not ONMYLEFTBORDER or TOMYLEFT) **and** the query start `i+3` is before `i+10` (startcmp = THRUME ≤ THRUME). Both conditions hold. The crum qualifies.

4. **ORGLRANGE check.** The stored crum's ORGLRANGE was set during `insertspanf` (spanf1.c:22):
   ```c
   prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
   ```
   This gives `1.linkISA` — a sub-address under digit `1` = LINKFROMSPAN. The query range `[1, 2)` covers all `1.x` addresses, so the ORGLRANGE check passes for link L's crum.

5. **Result extraction.** The matching crum's ORGLRANGE address `1.linkISA` is stripped of the prefix via `beheadtumbler` (sporgl.c:264) and added to the link set. `find_links` returns L's ISA.

---

### Part 2 — What does the returned endset show?

**`find_links` itself returns only link ISA tumblers. No endset data is in the response.**

The return type is `typelinkset` (spanf2.c:122-135), which is a linked list of `typelink` records containing only an `address` tumbler — just the link's ISA. The from/to/type endsets are absent from the `find_links` response.

**When endsets are retrieved after `find_links`:**

**Via `follow_link(L, whichend)` → `dofollowlink` (do1.c:223-232):**

```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
```

`link2sporglset` (sporgl.c:67-95) opens **L's own POOM** (the link document's permutation matrix) and queries it at V-position `whichend`:

```c
findorgl(taskptr, granf, linkisa, &orgl, type);
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // e.g., 1 = LINKFROMSPAN
tumblerincrement(&zero, 0, 1, &vspan.width);
context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL);
```

This returns the I-spans stored at that V-position — which were written during link creation by `insertendsetsinorgl` → `insertpm` (do1.c:218, do2.c:130-148, orglinks.c:75-133). Those I-spans are the **full original from-endset `[i, i+10)`**, not clipped to `[i+3, i+7)`.

`follow_link` returns the from-endset (`LINK_SOURCE=1`) as a V-spec covering `[i, i+10)` in the source document. The target endset and type endset are each returned in full via `LINK_TARGET=2` and `LINK_TYPE=3`.

**Via `retrieve_endsets` → `retrieveendsetsfromspanf` (spanf1.c:190-235):**

Called with the home document's text content V-span, this queries the spanfilade for crums whose SPANRANGE overlaps the queried content and whose ORGLRANGE is in `[LINKFROMSPAN, LINKFROMSPAN+1)`, `[LINKTOSPAN, LINKTOSPAN+1)`, and `[LINKTHREESPAN, LINKTHREESPAN+1)` separately.

When a crum matches, `contextintosporgl` (sporgl.c:205-220) extracts the context's coordinates:

```c
movetumbler(&context->totaloffset.dsas[SPANRANGE], &sporglptr->sporglorigin);  // crum start = i
movetumbler(&context->contextwid.dsas[SPANRANGE], &sporglptr->sporglwidth);    // crum width = 10
```

These are the **full crum dimensions** — not clipped to the query window. The crum for L's from-endset has SPANRANGE = `[i, i+10)`, so `sporglorigin = i` and `sporglwidth = 10` regardless of the `[i+3, i+7)` query that found it.

`linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset` then translates this full I-span back to V-space in the source document.

---

### Summary

| Question | Answer | Citation |
|----------|--------|----------|
| Does partial I-overlap suffice to match? | **Yes** — `crumqualifies2d` uses interval intersection | retrie.c:282-300 |
| What does `find_links` return? | **Link ISA addresses only** — no endset data | spanf2.c:122-135 |
| Source endset from `follow_link` | **Full original span `[i, i+10)`** — unclipped | sporgl.c:67-95 |
| Target & type endsets from `follow_link` | **Full original spans** — unclipped | sporgl.c:67-95, do2.c:130-148 |
| What `retrieve_endsets` extracts | **Full crum SPANRANGE** — `totaloffset + contextwid`, not intersection | sporgl.c:205-220, spanf1.c:248-264 |

**The overlap `[i+3, i+7)` is a discovery filter only.** It determines which links are found via the spanfilade. But once a link is found, all three endsets (source `[i, i+10)`, target, type) are returned in their full, creation-time form from either the link's own POOM (`follow_link`) or the spanfilade crum coordinates (`retrieve_endsets`). No clipping to the queried overlap occurs at any level.
