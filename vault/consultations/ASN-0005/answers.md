# Consultation Answers — Content Deletion

**Inquiry:** What must DELETE preserve? What happens to addresses, links, and other documents that reference deleted content? In what sense is deletion reversible?
**Date:** 2026-02-23 09:59
**Questions:** 10 (5 nelson, 5 gregory)

---

## Question 1 [nelson]

> When a user deletes content from their document, does the content's permanent address continue to exist, and can other documents still retrieve what was at that address?

### Nelson's Answer

# Yes, Absolutely. Deletion Is Arrangement, Not Destruction.

This is one of Xanadu's most fundamental design principles. When you delete content from your document, you are changing your document's *arrangement* (V-space), not destroying the content itself (I-space). The permanent address endures, and any other document that references that content is completely unaffected.

## The Two Address Spaces

Xanadu separates content identity from content arrangement:

- **I-Space (Invariant Space):** Where content permanently lives. Addresses are absolute and immutable. Content at an I-space address never changes.
- **V-Space (Virtual Space):** The document's current arrangement — a view that references I-space content. Can be rearranged across versions.

When you "delete," you remove content from your V-space arrangement. The I-space content remains untouched.

## Nelson's Explicit Statement

The diagram on page 4/9 shows "DELETED BYTES" as a valid system state, with this annotation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And more directly, on page 4/11:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is unambiguous. Deletion affects only the deleting document's current version.

## Why This Must Be So

The entire Xanadu architecture depends on this property:

**1. Append-only storage.** Nelson rejects "destructive replacement" at the deepest level:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**2. Transclusion depends on it.** When Document B transcludes content from Document A, it references the I-space address. If deletion could destroy I-space content, transclusion would be unreliable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Other documents fetch content from its permanent home location. That location must always resolve.

**3. Historical backtrack depends on it.** Every previous version of every document must remain reconstructible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If deletion destroyed I-space content, old versions could not be reconstructed.

**4. Link survivability depends on it.** Links attach to I-space content, not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links to "deleted" content continue to resolve because the I-space bytes still exist.

**5. Non-destruction is an explicit guarantee:**

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

## What Deletion Affects vs. Does Not Affect

| Aspect | Affected by DELETE? |
|--------|---------------------|
| V-space arrangement (current view) | **YES** — content removed |
| I-space content (permanent bytes) | **NO** — bytes remain forever |
| Previous versions of same document | **NO** — still contain the content |
| Other documents that transclude it | **NO** — their references still resolve |
| Links pointing to the content | **NO** — still resolve to I-space |
| Origin traceability (I-address) | **NO** — home document still identifiable |

## The Analogy

Think of I-space as a library where books have permanent shelf locations. V-space is a reading list that references those books. "Deleting" a book from your reading list does not burn the book. It remains on its shelf, available to anyone else whose reading list references it — and available to you if you ever consult an older version of your own list.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The braid accumulates strands. Deletion rearranges how strands are presented in the current view. No strand is ever cut from the braid itself.

---

## Question 2 [nelson]

> If document A includes shared content originally from document B, and document B's owner deletes that passage, does document A lose its copy or does the shared content survive independently?

### Nelson's Answer

## The Shared Content Survives

This is one of the clearest guarantees in the entire system. Document A does **not** lose access. The shared content persists independently of any deletion in Document B.

### Why: The I-Space/V-Space Separation

Nelson explicitly addresses this exact scenario on page 4/11:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Deletion in Xanadu is a **V-space operation only**. It removes content from a document's current arrangement (its virtual byte stream) but does not touch I-space, where the bytes permanently reside. Since Document A's transclusion references I-space addresses — not Document B's V-space positions — Document B's editing has no effect on Document A.

### The Mechanism

The storage model is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

When the original content was created in Document B, it was written to permanent I-space addresses. Those addresses never change and the content at them is immutable. Document A's transclusion is a V-space mapping pointing to those same I-space addresses. Document B's delete operation only modifies Document B's own V-space mapping — it says "stop showing these bytes in my current arrangement." The I-space content is untouched.

The deleted bytes in Document B enter a specific state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" refers to Document B's current V-stream only. The bytes remain fully addressable through their I-space addresses, which is how Document A reaches them.

### The Deeper Principle

This behavior is not incidental — it is the entire point of the architecture. Nelson designed the system so that modifications never damage originals:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And the non-destruction guarantee extends to all participants:

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

### Summary

| What happens | Effect on Document A |
|---|---|
| B's owner deletes the passage from B | **None** — A still shows the content |
| B's owner deletes the passage from all versions of B | **None** — I-space content persists |
| B's owner withdraws document B entirely | **None** — the bytes exist in I-space independently |

The content's permanent home is I-space. Documents are arrangements (views) over I-space content. Destroying a view does not destroy what the view looked at. This is the foundational insight of the I-space/V-space separation: content is permanent, arrangement is flexible.

---

## Question 3 [nelson]

> What happens to a link whose endpoint falls within a region that has been deleted — does the link itself survive, and can it still be followed?

### Nelson's Answer

# Link Survival After Deletion

The short answer: **yes, the link survives, and yes, it can still be followed.** This falls out from two independent guarantees that reinforce each other.

## Why the Link Survives

### 1. DELETE Does Not Destroy Content

DELETE in Xanadu removes content from **V-space** (the document's current arrangement) but leaves **I-space** (permanent storage) untouched.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes still exist at their permanent I-space addresses. They are simply no longer part of any V-space arrangement in that document's current version.

### 2. Links Attach to Bytes, Not Positions

This is the crucial architectural point. Links do not point to V-space positions (which shift during editing). They point to **spans of bytes** identified by permanent I-space addresses.

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The page 4/43 diagram states this explicitly:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

Since DELETE removes bytes from V-space but not I-space, the bytes the link is "strapped to" still exist. The link's endset addresses remain valid.

## When Would a Link Actually Break?

A link breaks **only** when all bytes at one of its endsets are completely destroyed — not just deleted from a V-space view, but removed from existence entirely. In Nelson's architecture, this effectively cannot happen through normal operations, because I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content at an I-space address **never changes and never disappears**. So within the Xanadu model, a link whose endpoint falls in a deleted region is not even close to breaking — the bytes are still there, permanently.

## How Can the Link Be Followed?

When a reader follows the link, the system resolves the endset's I-space addresses. The content is fetched from its permanent home:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The front end can then present the content in context. If the content has been "deleted" from the current version but exists in a previous version, the system can reconstruct that version:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

## Version-Spanning Behavior

Nelson goes further — links not only survive deletion but can "reach through" versions:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

So a link to content that was deleted in version 3 can still be followed in version 2 (where the content exists), or the front end can attempt to find corresponding content in a later version.

## Summary

| Question | Answer |
|----------|--------|
| Does the link survive deletion of its endpoint region? | **Yes** — the link attaches to I-space bytes, which are never destroyed |
| Can the link still be followed? | **Yes** — the bytes exist at their permanent I-space addresses |
| Does DELETE destroy the bytes? | **No** — DELETE removes from V-space only; I-space is append-only |
| When would a link actually break? | Only if **all** bytes at an endset were truly destroyed (not possible through normal Xanadu operations) |
| Can the reader see the deleted content? | **Yes** — via historical backtrack to a version where the content was present, or via the I-space address directly |

The entire architecture is designed around this property. Links are "straps between bytes," and those bytes are permanent. Deletion is a change of *view*, not a change of *reality*.

---

## Question 4 [nelson]

> Is deletion an act of removing content from existence, or an act of removing content from a particular document's visible arrangement while the content remains permanently stored?

### Nelson's Answer

# Deletion in Xanadu: Arrangement, Not Destruction

Deletion in Xanadu is **removal from a document's visible arrangement** (V-space). Content remains **permanently stored** in I-space. This is not an edge case or implementation detail — it is fundamental to the system's entire architecture.

## Nelson's Direct Statement

The diagram on page 4/9 shows "DELETED BYTES" as a valid system state with this annotation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This tells you exactly what deletion means: the bytes become "not currently addressable" in that document's current view. They are not destroyed. They await historical backtrack. They may still appear in other versions or other documents that transclude them.

## The Architectural Reason

Xanadu separates content identity (I-space) from content arrangement (V-space):

- **I-space** is where content permanently lives. Addresses are immutable. Content at an I-space address never changes.
- **V-space** is the document's current arrangement — a view that references I-space content.

Deletion operates on V-space only. It removes content from the current arrangement. The I-space content is untouched.

Nelson makes this explicit:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## The Deeper Principle

Nelson designed Xanadu specifically to abolish destructive replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

His alternative:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

And on modifications to published work:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

The phrase "without damaging the originals" is the key. Deletion is a modification to arrangement, not damage to content.

## What Survives Deletion

| Aspect | Affected by DELETE? |
|--------|---------------------|
| V-space arrangement (current view) | **Yes** — content removed from current view |
| I-space content (permanent storage) | **No** — bytes remain forever |
| Previous versions | **No** — still contain the content |
| Transclusions in other documents | **No** — other documents still show it |
| Links pointing to the content | **No** — still resolve to I-space |
| Historical backtrack | **No** — any previous state reconstructible |

## The Historical Backtrack Guarantee

Because deletion doesn't destroy content, users can always recover:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

## Links Also Follow This Pattern

Deleted links receive the same treatment as deleted bytes. The diagram on 4/9 shows:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The parallel is exact. Links, like bytes, are removed from current addressability but not from existence.

## Summary

Deletion in Xanadu is an act of **rearrangement**, not an act of **destruction**. The content remains permanently in I-space. The document's V-space mapping changes to exclude it from the current view. Previous versions, other documents that transclude the content, and links to the content are all unaffected. This is not a safety feature bolted on — it is the foundational storage model that makes permanent addressing, historical backtrack, and transclusion possible.

---

## Question 5 [nelson]

> If deletion is reversible, what must the system remember so that an undelete restores not just the content but also its original position and its relationships to links and shared references?

### Nelson's Answer

# What Must the System Remember for Undelete?

The short answer is: **almost nothing extra**, because the architecture already preserves everything needed. That is the entire point of the I-space/V-space separation. But let me be precise about what "already preserved" means and what specific information restoration requires.

## 1. Content: Already Remembered (I-Space Is Append-Only)

DELETE does not touch I-space. The bytes remain at their permanent I-addresses forever.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The content is never lost. There is nothing to "remember" about it — it never left. The I-address of every deleted byte continues to resolve. This is not a design choice for undo support; it is the fundamental permanence guarantee (P0).

## 2. Position: The V-to-I Mapping Is What Must Be Recoverable

What DELETE actually destroys is the **V-space arrangement** — the mapping from virtual positions (where the user sees content) to I-space addresses (where content permanently lives). To undelete, you need to reconstruct:

**(a) Where in the V-stream the span was.** The V-address at which the deleted span began, and the V-address at which it ended. Without this, you know WHAT was deleted but not WHERE it appeared in the document.

**(b) The ordered sequence of I-addresses within that span.** A document's V-stream can interleave native content and transcluded content from multiple sources. The POOM (positional mapping) holds entries like "V-positions 47–92 map to I-addresses from document X; V-positions 93–105 map to I-addresses from document Y." Restoring the span means restoring this exact interleaving.

**(c) How following content shifted.** DELETE compresses V-addresses:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66, describing INSERT — DELETE is the inverse]

Undelete must reverse this shift, re-opening the gap and restoring the original positions.

## 3. Links: Nothing Extra Needed

This is where the architecture pays its deepest dividend. Links attach to I-space, not V-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

When you delete content from V-space, the links still exist and still point to those I-addresses. The link endsets are unchanged. What changes is whether the linked content is *visible* in the document's current V-stream. The moment the V-to-I mapping is restored, the links "reconnect" automatically — they were never disconnected at the I-level.

The system does not need to remember "which links were attached to this span." The links remember themselves, because they point to permanent addresses that the deletion never touched.

## 4. Shared References (Transclusions): Also Automatic

If document A transcludes content from document B, and B deletes that content from B's V-space:
- A's V-stream still includes the content (A has its own POOM entries mapping to the same I-addresses)
- B's content is gone from B's view but untouched in I-space
- The transclusion relationship is encoded in the I-addresses themselves — transcluded content shares I-addresses with its source

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

For undelete: the I-addresses in the restored POOM entries tell you whether each byte was native or transcluded. Restoring the V-to-I mapping automatically restores the transclusion structure, because the structure IS the mapping.

## 5. How the System Actually Remembers: Version History

Nelson's design makes this explicit. The version history IS the memory:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

Every state of every document is reconstructible. "Undelete" is not a special operation — it is a request for a previous version's arrangement. The journal (in the formal model: Σ includes journals) records every operation, and the POOM at any historical point can be reconstructed by replay.

## Summary: What Must Be Remembered

| Component | Remembered by | Special undo state needed? |
|-----------|--------------|---------------------------|
| **Content bytes** | I-space (append-only, permanent) | No — never deleted |
| **V-position** | Journal / version history | No — recorded as part of the DELETE operation |
| **V→I mapping** | Journal replay reconstructs POOM | No — derivable from history |
| **Link relationships** | Links themselves (point to I-space) | No — links are unchanged |
| **Transclusion structure** | I-addresses encode origin | No — implicit in the mapping |
| **Shift of following content** | Journal (DELETE records position and length) | No — invertible from the operation record |

The answer, then, is that the system must remember **the DELETE operation itself** — where it happened and how long the span was. Given that single record plus the permanent I-space content, everything else is derivable. The V-to-I mapping is reconstructed from history. The links and transclusions were never broken. The content was never destroyed.

This is what Nelson means when he says the storage system "automatically keeps track of the changes and the pieces." The architecture does not need a special undo mechanism because the entire design is, in a sense, one giant undo buffer. Deletion is just rearrangement of the view; the reality underneath is permanent.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

You can always untwist the braid to any previous state, because every strand is preserved.

---

## Question 6 [gregory]

> After DELETE removes a V-span from document A, and document B holds a transclusion of the same I-addresses, does `find_links` called on document B still discover links whose endsets overlap those I-addresses — confirming that DELETE in A has zero effect on link discovery through B?

### Gregory's Answer

## KB Synthesis

# Answer

**YES**, `find_links` called on document B still discovers links whose endsets overlap those I-addresses. DELETE in A has zero effect on link discovery through B.

## Mechanism

The interaction works through three independent subsystems:

### 1. DELETE Frame Condition ([FC-DELETE-CROSS-DOC])
DELETE operates exclusively on the target document's POOM. From Finding 0064:
> "DELETE in one document has zero effect on any other document's POOM mappings. If document T transcluded content from document D (sharing I-addresses via COPY), and D subsequently deletes that content, T's POOM still maps to the shared I-addresses. T's content is unaffected."

Document B's V-to-I mappings remain intact after DELETE in A.

### 2. Link Discovery Mechanism ([ST-FIND-LINKS])
From Finding 0028:
> "`find_links(search_specset)` discovers links by I-address intersection, not by document or V-address matching. The search specset is converted to I-addresses, and links are returned if any I-address in the search overlaps with I-addresses in a link endpoint."

Link discovery operates purely in I-space, not V-space or document-space.

### 3. Transclusion Preserves Discovery ([INT-TRANSCLUSION-LINK-SEARCH])
This exact scenario is documented in Finding 0029:
> "When content is transcluded (vcopy'd) to another document, the copy retains the original content identity (I-stream addresses). If the original content is deleted, links referencing that content become undiscoverable from the original document but remain discoverable from the copy, because the copy's V-stream still contains content at those I-stream addresses."

**Concrete example from Finding 0029:**
```
- Original document contains "linked", link created on it
- vcopy("linked") from Original to Copy
- Delete "linked" from Original
- find_links(Original) → []
- find_links(Copy) → [link_id] ✓
```

## Supporting Invariants

- **[INV-IADDR-IMMUTABILITY]** (Finding 0064): "DELETE frees the POOM bottom crums that reference I-addresses, but the I-addresses themselves persist in the granfilade unconditionally."
- **[INV-LINK-CONTENT-TRACKING]** (Finding 0004): Links remain valid "as long as those content identities exist in the system (in any document)."
- **[FC-DOC-ISOLATION]**: Operations on document A cannot affect document B's structure.

## Conclusion

DELETE removes A's V-stream mappings → A's POOM no longer maps those I-addresses → `find_links(A)` fails. But B's POOM still maps the same I-addresses → B's query specset converts to those I-addresses → I-address intersection succeeds → links discovered from B. The DELETE has **zero effect** on link discovery through B.

## Code Exploration

Perfect! I found an existing golden test that directly answers your question. Let me provide the complete answer with code citations.

---

## Answer: YES — DELETE in A has zero effect on link discovery through B

After DELETE removes a V-span from document A, and document B holds a transclusion of the same I-addresses, `find_links` called on document B **still discovers links** whose endsets overlap those I-addresses. This confirms that DELETE in A has **zero effect** on link discovery through B.

### Empirical Evidence

The golden test `search_after_vcopy_source_deleted.json` demonstrates this behavior:

**Before deletion:**
- `find_links` on original doc: finds link `1.1.0.1.0.1.0.2.1` ✓
- `find_links` on copy doc: finds link `1.1.0.1.0.1.0.2.1` ✓

**After deleting V-span from original:**
- Original doc contents: `"Original content here"` (text removed)
- Copy doc contents: `"Prefix: linked"` (transclusion intact)
- `find_links` on original doc: returns `[]` (empty — no V→I mapping)
- `find_links` on copy doc: returns `["1.1.0.1.0.1.0.2.1"]` ✓ **LINK STILL FOUND**

### Code Architecture Analysis

This behavior arises from the separation of concerns between three data structures:

#### 1. Document A's POOM (modified by DELETE)

`dodeletevspan` operates exclusively on document A's enfilade [backend/do1.c:158-167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  );
}
```

This calls `deletevspanpm` [backend/orglinks.c:145-152]:

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

Which calls `deletend` [backend/edit.c:31-61] — this operates on the **document's enfilade tree** only, removing nodes that map V-positions to I-positions. It does **not** touch the spanfilade.

#### 2. Document B's POOM (unaffected by DELETE in A)

Document B maintains its **own independent V→I mapping**. When B transcludes content via `vcopy`, it creates its own V-span entries that point to the same I-addresses [backend/do1.c:60-62]:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The `insertpm` call modifies document B's POOM. The `insertspanf` call registers the transclusion in the spanfilade.

#### 3. The Spanfilade (never modified by DELETE)

When `find_links` is called on document B, it:

1. **Converts B's V-span to I-span** via `specset2sporglset` [backend/spanf1.c:71]:
```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

This calls `vspanset2ispanset` [backend/orglinks.c:397-402]:
```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
  return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

The `permute` function walks **document B's enfilade** to resolve V→I addresses [backend/orglinks.c:404-422].

2. **Searches the spanfilade** via `sporglset2linkset` [backend/sporgl.c:222-237]:
```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset, typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
	for (; homeset; homeset = homeset->next) {
		sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
	}
}
```

Which calls `retrieverestricted` [backend/sporgl.c:259]:
```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

This searches the **global spanfilade** for links indexed by I-addresses.

### Key Insight

**DELETE never touches the spanfilade.** There is no `deletespanf` function. The spanfilade is only modified by:
- `insertspanf` — called during COPY [backend/do1.c:62,79] and CREATE_LINK [backend/do2.c:119-123]
- No deletion path exists

Therefore:
- Document A's DELETE removes entries from A's POOM (V→I mapping)
- Document B's POOM is unchanged — it still maps B's V-positions to the same I-addresses
- The spanfilade is unchanged — link endsets at those I-addresses remain discoverable
- `find_links` on B converts B's V-span → I-span (using B's POOM) → searches spanfilade → finds the link

### Conclusion

The architecture provides strong **transclusion isolation**: modifications to one document's V-stream (including DELETE) do not affect link discovery through other documents that transclude the same I-addresses. Links are stored by immutable I-addresses in the spanfilade, not by mutable V-addresses in individual POOMs.

---

## Question 7 [gregory]

> When FOLLOWLINK resolves a link whose source endset I-addresses have been deleted from every document's POOM, does `span2spanset` return an empty specset for that endset, or does it return the raw I-addresses without V-position mapping?

### Gregory's Answer

## KB Synthesis

# Answer: Empty Specset (Silent Filtering)

When FOLLOWLINK resolves a link whose source endset I-addresses have been deleted from every document's POOM, **`span2spanset` returns an empty specset**, not raw I-addresses. The I-addresses are silently filtered out during I-to-V conversion.

## Mechanism

The filtering occurs through this call chain `[SS-FOLLOWLINK]`:

1. `link2sporglset()` extracts I-addresses from the link orgl → succeeds (link orgl is permanent)
2. `linksporglset2specset()` converts I-addresses to V-addresses via the specified document's POOM
3. `span2spanset()` calls `retrieverestricted()` to search the POOM for each I-address
4. **When `retrieverestricted()` returns NULL (no POOM mapping), the I-address is silently dropped — no V-span is added to the result**

## Behavior

From `[INV-ITOV-FILTERING]`:
> "At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), the I-address is dropped from the result without error."

From `[EC-GHOST-LINK]`:
> "Three observable cases: (1) all endset I-addresses live → full result; (2) some unreferenced → partial result, only live addresses converted; (3) all unreferenced → empty result `[]`, operation still succeeds."

Concrete example from `[EC-GHOST-LINK]`:
```
- Before: Link L has to-endset I-address `a`, document D has `poom.D(1.5) = a`
- Delete all content from D: `poom.D` no longer maps any v to `a`
- After: FOLLOWLINK(L, TO, D) → `[]`, works=true
```

## Precondition

From `[PRE-FOLLOWLINK]`:
> "There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error."

This is **not an error condition** but the specified successful behavior for ghost links. The raw I-addresses are never exposed to the caller — the I-to-V conversion layer acts as a mandatory filter between the permanent layer (which stores I-addresses) and the query result (which returns V-addresses only).

## Code Exploration

Based on my analysis of the source code, I can now provide a definitive answer:

## Answer

**`span2spanset` returns an empty specset** when the source endset I-addresses have been deleted from every document's POOM. The returned vspanset is NULL (empty), not the raw I-addresses.

## Code Path Analysis

### 1. FOLLOWLINK Entry Point
`followlink` [fns.c:114-127] calls `dofollowlink` which extracts the link's endsets and converts them to specsets via `linksporglset2specset`.

### 2. I→V Conversion Setup
`linksporglset2specset` [sporgl.c:97-123] processes each sporgl:
- Line 105-114: If `sporgladdress` is zero (no home document), returns raw I-span
- Line 115-116: Otherwise calls `linksporglset2vspec` to convert to V-spans

`linksporglset2vspec` [sporgl.c:127-137] critically initializes:
```c
specptr->vspanset = NULL;  // Line 135
sporglset2vspanset (taskptr,homedoc, sporglsetptr, &specptr->vspanset,type);  // Line 136
```

### 3. Permutation Through POOM
The conversion chain proceeds:
- `sporglset2vspanset` [sporgl.c:141-176, line 157] → 
- `ispan2vspanset` [orglinks.c:389-394] → 
- `permute` [orglinks.c:404-422, line 415] → 
- `span2spanset` [orglinks.c:425-454]

### 4. The Critical Decision Point
`span2spanset` [orglinks.c:425-454] attempts to find the I-addresses in the POOM:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, 
                            (typespan*)NULL, targindex, (typeisa*)NULL);  // Line 435

for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, 
                                     (typeitemset*)targspansetptr);  // Lines 439-445
}

if(!context){
    return(targspansetptr);  // Lines 446-448 - Returns NULL if nothing found
}
```

### 5. POOM Retrieval
`retrieverestricted` [retrie.c:56-85] → `retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` [retrie.c:229-268]

In `retrieveinarea` [retrie.c:93]:
```c
context = NULL;  // Initialized to NULL
```

`findcbcinarea2d` [retrie.c:252-264] walks the enfilade tree:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1, 
                         span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
        continue;  // Skip crums that don't contain requested I-addresses
    }
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);  // Recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // Add to result list
    }
}
```

**When I-addresses don't exist in the POOM**, no crums qualify, so `context` remains NULL throughout.

### 6. Final Result
Back in `span2spanset`:
- `context` is NULL (no matching I-addresses found)
- Lines 446-448: Returns `targspansetptr` unchanged
- `targspansetptr` was initialized to NULL at [sporgl.c:135]
- Result: **Empty vspanset**, not raw I-addresses

## Conclusion

The V↔I conversion via `span2spanset` **returns an empty specset** when I-addresses don't exist in any document's POOM. The system does not fall back to returning raw I-addresses — it correctly reports that those I-addresses map to nothing in V-space for that document. This is the expected behavior: deleted content has no V-position mapping.

---

## Question 8 [gregory]

> If content at I-addresses [.0.1.3, .0.1.5] is deleted from document A, then later someone COPYs that same I-address range from document B (which still has it via transclusion) back into document A, does document A's POOM now contain entries pointing to the original I-addresses — effectively restoring the content identity that links and version comparisons depend on?

### Gregory's Answer

## KB Synthesis

Yes, COPY from document B back into document A **does restore the original I-addresses** in A's POOM, effectively recovering the content identity that links and version comparisons depend on. This is exactly the identity-preserving restoration mechanism the system is designed for.

Let me trace through the mechanics:

## Step-by-Step Analysis

**After DELETE from A:**
- Document A's POOM no longer contains V→I mappings for [.0.1.3, .0.1.5] `[ST-DELETE]`
- Document B's POOM still contains those mappings (DELETE only affects the target document) `[FC-DELETE-CROSS-DOC]`
- The I-addresses [.0.1.3, .0.1.5] still exist permanently in the granfilade `[INV-IADDR-IMMUTABILITY]`

**After COPY from B to A:**
- COPY reads B's POOM to find the V→I mappings (which point to the original I-addresses)
- COPY converts those to I-spans (preserving the original I-addresses [.0.1.3, .0.1.5])
- `insertpm` adds NEW V→I mappings in A's POOM pointing to the SAME original I-addresses `[ST-VCOPY]`

## The Key Distinction

From `[INV-DELETE-NOT-INVERSE]` Finding 0064:

> DELETE followed by INSERT of identical text does NOT restore the original document state. The V-space content is reconstructed (same characters at the same positions), but the I-space identity is entirely different. INSERT always allocates fresh I-addresses from the granfilade — it has no mechanism to reuse previously freed I-addresses.

But:

> The only identity-preserving restoration is VCOPY from a document (typically a version) that still references the original I-addresses. VCOPY shares existing I-addresses rather than allocating new ones.

The example explicitly shows:
```
State A: "Original text" at I(5.1)-I(5.13)
DELETE → INSERT same text:
  Result: "Original text" at I(5.14)-I(5.26) [NEW addresses]
  ❌ Transclusions broken
  ❌ compare_versions broken  
  ❌ Links broken

DELETE → VCOPY from version sharing I(5.1)-I(5.13):
  Result: "Original text" at I(5.1)-I(5.13) [ORIGINAL addresses]
  ✅ Identity restored
```

## Practical Consequences

After COPY from B to A restores the I-addresses:

1. **Links work again**: Any links referencing those I-addresses become discoverable from A `[INT-LINK-TRANSCLUSION]`
2. **Version comparison works**: `compare_versions(A, other_documents)` will find shared content `[ST-COMPARE-VERSIONS]`
3. **New V-position**: The content appears at whatever V-position the COPY targeted, but the I-addresses are the originals
4. **Provenance preserved**: The POOM crums will record the `homedoc` as the original allocating document (not B, not A) `[INV-IADDR-PROVENANCE]`

This is the fundamental mechanism that makes recovery via versions work in Xanadu — COPY preserves identity where INSERT would destroy it `[ST-COPY]`.

## Code Exploration

Let me first provide you with the complete analysis based on the source code I've read, then I can write and run the test if you'd like to verify.

## Answer: Yes, Content Identity Is Restored

When content at I-addresses [.0.1.3, .0.1.5] is deleted from document A, then later someone COPYs that same I-address range from document B (which still has it via transclusion) back into document A, **document A's POOM WILL contain entries pointing to the original I-addresses**, effectively restoring the content identity that links and version comparisons depend on.

### Detailed Trace Through the Code

#### 1. DELETE Operation Removes POOM Entries

When content is deleted from document A [`do1.c:158`]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();
	return (
	   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
	&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

This calls `deletevspanpm` [`orglinks.c:145-152`]:

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

Which calls `deletend` [`edit.c:30-75`] that **disowns and frees** the POOM entries [`edit.c:58-59`]:

```c
case 1:
	disown ((typecorecrum*)ptr);
	subtreefree ((typecorecrum*)ptr);
	break;
```

After deletion, document A's POOM **no longer contains any entries** for I-addresses [.0.1.3, .0.1.5].

#### 2. COPY Operation Extracts I-Addresses from Source

When someone COPYs from document B [`do1.c:45-65`]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
	return (
	   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
	&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
	&& acceptablevsa (vsaptr, docorgl)
	&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
	&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN));
}
```

The key step is `specset2ispanset` [`do2.c:14-46`], which looks at **document B's POOM** to extract the I-addresses:

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
  typeorgl docorgl;
	for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
		if (((typeitemheader *)specset)->itemid == VSPECID) {
			if (!(
			  findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)
			&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
			     ((typevspec *)specset)->vspanset, ispansetptr)))){
			       return (FALSE);  
			}
		}
	}
	return (TRUE);
}
```

It calls `vspanset2ispanset` [`orglinks.c:397-402`]:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, 
                                typeispanset *ispansetptr)
{
  typespanset *permute();
	return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

This uses `permute` and `retrieverestricted` [`retrie.c:55-84`] to walk document B's POOM and extract which I-addresses are at the requested V-positions. Since document B still has I-addresses [.0.1.3, .0.1.5] via transclusion, these **original I-addresses** are returned in the `ispanset`.

#### 3. INSERT Operation Creates New POOM Entries with Original I-Addresses

The extracted I-addresses are then inserted into document A via `insertpm` [`orglinks.c:75-134`]:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, 
              typesporglset sporglset)
{
  tumbler lstream, lwidth;
  type2dbottomcruminfo linfo;
  typewid crumorigin, crumwidth;
	for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
		unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
		movetumbler (&lstream, &crumorigin.dsas[I]);  // Original I-address!
		movetumbler (&lwidth, &crumwidth.dsas[I]);
		movetumbler (vsaptr, &crumorigin.dsas[V]);    // New V-address in doc A
		insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
		tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
	}
	return (TRUE);
}
```

**Key observation at [`orglinks.c:105-113`]**: The POOM entry created has:
- **I-dimension** = `lstream` (the **original I-address** [.0.1.3, .0.1.5] from the ispanset)
- **V-dimension** = `vsaptr` (the **new V-address** where content is being inserted in document A)

The `insertnd` function [`insertnd.c:15-111`] then inserts this new POOM entry. It only checks if entries are **adjacent extensions** [`insertnd.c:250, 301-309`], not if the same I-addresses already exist. Since the content was **deleted**, there are no existing entries, so new entries are created.

### Consequences: Identity Is Fully Restored

After the COPY operation, document A's POOM contains entries mapping (new) V-addresses to the (original) I-addresses [.0.1.3, .0.1.5]. This means:

1. **Links work**: Any links pointing to those I-addresses will now resolve when querying document A
2. **Version comparison works**: `compare_versions` between documents A and B will detect the shared I-addresses
3. **Find documents works**: `find_documents` queries for those I-addresses will return document A

The content identity is **completely restored** — it's as if document A never deleted the content, from an identity perspective. The content exists at a different V-position (different location in the document), but the **I-addresses** (the immutable content identity) are the same.

I've prepared a test scenario to verify this behavior empirically. Would you like me to add it to the test suite and run it?

---

## Question 9 [gregory]

> After DELETE shifts surviving POOM entries left via `tumblersub`, do the I-widths stored in those surviving bottom crums remain exactly unchanged — confirming that DELETE's V-space compaction never modifies any I-displacement or I-width field in a surviving crum?

### Gregory's Answer

## KB Synthesis

# Answer: YES — I-widths remain exactly unchanged

DELETE's V-space compaction via `tumblersub` modifies **only** the V-displacement field of surviving POOM bottom crums. The I-dimension fields (I-displacement and I-width) remain completely untouched.

## Evidence

### Direct code confirmation

[INT-DELETE-SUBSPACE-ASYMMETRY] Finding 0055 provides the explicit code:

```c
edit.c:63 — Case 2: tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])
```

The operation modifies `cdsp.dsas[V]` (V-displacement) in place. No I-dimension fields are referenced.

### POOM crum structure

[SS-POOM-BOTTOM-CRUM] Finding 0076 defines the structure:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler,  dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler,  dsas[V]: Tumbler }
}
```

DELETE's Case 2 (shift operation) modifies only `origin.dsas[V]`, leaving three fields unchanged:
- `origin.dsas[I]` — I-displacement ✓ unchanged
- `width.dsas[V]` — V-width ✓ unchanged  
- `width.dsas[I]` — I-width ✓ unchanged

### I-address immutability

[INV-IADDR-IMMUTABILITY] Finding 0064:

> The granfilade is append-only — `inserttextingranf` always allocates fresh addresses at the end. There is no mechanism to reuse, reassign, or deallocate I-addresses. DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally.

DELETE cannot modify I-addresses because they are permanent. The I-fields in POOM crums are references to immutable I-space locations.

### Frame condition

[FC-GRANF-ON-DELETE] Finding 0061:

> DELETE and REARRANGE are frame-condition-preserving with respect to the granfilade. These operations modify only the spanfilade (V-to-I mappings) and leave the granfilade (I-space content storage) completely unchanged.

DELETE operates exclusively on V-space structure. The I-dimension of the V→I mapping is read-only during DELETE.

## Scope Note

This answer applies specifically to **Case 2 crums** in `deletend()` — crums positioned entirely after the deletion that are shifted left via `tumblersub`. 

For **Case 1 crums** (those within the deletion range that are freed via `disown` + `subtreefree`), the question is moot — they are deallocated entirely.

For **crums split by Phase 1 cutting** (`slicecbcpm`), both V-widths and I-widths are modified to reflect the smaller post-split spans. However, these are not "shifted via tumblersub" — they are restructured via cutting operations. The question's phrasing "shifts surviving POOM entries left via tumblersub" specifically excludes cut crums and refers only to the Case 2 shift operation.

## Code Exploration

---

# Answer: DELETE Preserves I-Widths During V-Space Compaction

## YES — I-widths remain exactly unchanged.

After tracing through the DELETE implementation, I can confirm that V-space compaction via `tumblersub` **never modifies any I-displacement or I-width** in surviving crums. Only V-displacements are changed.

## Code Evidence

### Structure of POOM Crums

All crums store width and displacement separately [enf.h:85-107]:

```c
struct structcbc {  // Bottom crum
    typewid cwid;   // Width [line 102]
    typedsp cdsp;   // Displacement [line 103]
    // ... other fields ...
};
```

Both are defined as [wisp.h:50-54]:
```c
struct structwid {
    tumbler dsas[MAXLOXIZE];  // Array of 2 tumblers for POOM
};
```

For POOM, the indices are [wisp.h:19-20]:
- `I = 0` (I-dimension)
- `V = 1` (V-dimension)

So:
- `cwid.dsas[I]` = I-width
- `cwid.dsas[V]` = V-width
- `cdsp.dsas[I]` = I-displacement
- `cdsp.dsas[V]` = V-displacement

### DELETE Call Chain

1. `dodeletevspan` calls `deletevspanpm` [do1.c:165]
2. `deletevspanpm` calls `deletend` with **index = V** [orglinks.c:149]:
   ```c
   deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
   ```

### Core Deletion: Only V-Displacement Modified

In `deletend`, surviving crums after the deleted region (case 2) execute [edit.c:62-65]:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

Since `index = V`, this becomes:
```c
tumblersub (&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V]);
```

**This is the ONLY modification in case 2.**

### What Is NOT Modified

DELETE never touches:
- `ptr->cwid.dsas[I]` — **I-width unchanged**
- `ptr->cwid.dsas[V]` — V-width unchanged
- `ptr->cdsp.dsas[I]` — **I-displacement unchanged**

Only `ptr->cdsp.dsas[V]` is modified via `tumblersub`.

## Complete DELETE Behavior

For each crum, `deletecutsectionnd` [edit.c:235-248] classifies it:

- **Case 0**: Before deletion → no change
- **Case 1**: Inside deletion → `disown()` and `subtreefree()` [edit.c:58-61]
- **Case 2**: After deletion → shift V-displacement left [edit.c:63]

Only case 2 modifies surviving crums, and it modifies **only the V-displacement**.

## Semantic Implication

DELETE's V-space compaction is a **pure V-translation**:
- Crums after the deletion shift left in V-space
- Their I-widths remain unchanged → permascroll address ranges preserved
- Their I-displacements remain unchanged → I-space positions preserved
- Their V-widths remain unchanged → vertical extents preserved

This confirms that DELETE is purely a V-space operation that leaves all I-space information (addresses, widths, displacements) completely intact in surviving crums.

## Code Citations

- [backend/enf.h:85-107] — Bottom crum structure with `cwid` and `cdsp`
- [backend/wisp.h:19-20, 50-54] — POOM dimension indices and wid/dsp structure
- [backend/do1.c:158-167] — `dodeletevspan` entry point
- [backend/orglinks.c:145-152] — `deletevspanpm` calls `deletend(index=V)`
- [backend/edit.c:31-76] — `deletend` main loop
- [backend/edit.c:63] — **Critical line**: Only `cdsp.dsas[index]` modified
- [backend/edit.c:235-248] — `deletecutsectionnd` classifies crums

---

## Question 10 [gregory]

> When `FINDDOCSCONTAINING` is called with a specset whose I-addresses were deleted from document A but still exist in the spanfilade as stale DOCISPAN entries, does the query return document A as a result — and if so, is there any mechanism the caller can use to distinguish stale from current containment?

### Gregory's Answer

## KB Synthesis

# Answer: FINDDOCSCONTAINING Returns Stale Entries, Post-Filter via I-to-V Conversion

Yes, `FINDDOCSCONTAINING` returns document A as containing the I-addresses even after deletion, and there **is** a mechanism to distinguish stale from current containment.

## Why Stale Entries Persist

The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. When DELETE removes content from document A's POOM, it calls `deletevspanpm` → `deletend` which modifies only the granfilade POOM layer. There is no corresponding spanfilade deletion function — `insertspanf` exists but no `deletespanf` [INT-DELETE-SPANF-DIVERGENCE]. The DOCISPAN entries created during the original INSERT or COPY persist permanently.

This causes the POOM and spanfilade to diverge [EC-STALE-SPANF-REFERENCE]:
- Before DELETE: POOM says `poom.A(v) = i` AND spanf says `i ∈ doc_A`
- After DELETE: POOM has no mapping for `i`, but spanf still claims `i ∈ doc_A`

## Query Returns Stale Results

`FINDDOCSCONTAINING(i)` returns a **superset** of documents currently containing `i`:

```
actual_docs(i) ⊆ find_documents(i)
```

where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The reverse inclusion does NOT hold. Document A appears in results because the spanfilade entry persists, creating a "ghost reference" [EC-STALE-SPANF-REFERENCE].

**Concrete example** from [EC-STALE-SPANF-REFERENCE]:
```
Setup:
  Source S has content at I-addresses α₁..α₅
  Target T copies that content → spanf registers T for α₁..α₅

After DELETE from T:
  FINDDOCSCONTAINING(α₁..α₅) → {S, T}   (T is stale)
```

## Filtering Mechanism: I-to-V Conversion

The caller distinguishes stale from current containment via **I-to-V conversion** [INV-ITOV-FILTERING]. This is the same filtering mechanism used by FOLLOWLINK and RETRIEVEENDSETS:

**Conversion path:**
```
I-addresses → ispan2vspanset() → permute() → span2spanset() → retrieverestricted()
```

At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for each I-address. If the POOM has no mapping (returns NULL), the I-address is **silently dropped** from the result. No error is raised [INV-ITOV-FILTERING].

**Post-filter procedure:**
```
After FINDDOCSCONTAINING(α₁..α₅) → {S, T}:
  I-to-V(α₁, T) → ∅      (no V-position in T — stale)
  I-to-V(α₁, S) → v₁     (still live in S — current)
```

Empty results from I-to-V conversion indicate stale spanfilade entries. Non-empty results confirm current containment.

## Summary

1. **Does FINDDOCSCONTAINING return document A?** — YES, stale entries are included in results.
2. **Filtering mechanism** — I-to-V conversion: attempt to resolve I-addresses to V-addresses in each returned document; stale entries fail resolution (return empty), live entries succeed.

The system provides no automatic filtering — callers **must** post-process FINDDOCSCONTAINING results via I-to-V conversion to distinguish current from historical containment [EC-STALE-SPANF-REFERENCE].

## Code Exploration

Based on my code inspection, I can now provide a definitive answer to your question.

## Answer

**Yes, FINDDOCSCONTAINING returns document A as a result**, and **no, there is no mechanism for the caller to distinguish stale from current containment** at query time.

---

## Code Evidence

### 1. FINDDOCSCONTAINING Does Not Check Current POOM State

`finddocscontainingsp` [spanf1.c:151-188] queries the spanfilade directly:

```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
  tumbler docid;
  typecontext *context, *c;
  typecontext *retrieverestricted();
  // ...
  
  clear (&docspace, sizeof(typespan));
  tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // Line 168
  tumblerincrement (&docspace.width, 0, 1, &docspace.width);
  
  for (; ispanset; ispanset = ispanset->next) {
    // Line 171: Query spanfilade for DOCISPAN entries overlapping the I-addresses
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, 
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    
    for (c = context; c; c = c->nextcontext) {
      movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
      beheadtumbler (&docid, &document.address);  // Line 174: Extract document ID
      
      if (isinlinklist(*headptr, &document.address))
        continue;
      
      document.itemid = LINKID;
      document.next = NULL;
      addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, 
                                                  (typeitemset*)addresssetptr);
    }
    contextfree (context);
  }
  
  return (TRUE);
}
```

**Key observation [spanf1.c:171]**: This function calls `retrieverestricted` on the spanfilade to find ALL DOCISPAN entries that overlap the query, with **no filtering based on whether those I-addresses are still in any document's current POOM**.

### 2. DELETE Does Not Clean Up Spanfilade Entries

When content is deleted, `deletevspanpm` [orglinks.c:145-152] only removes the V→I mapping from the document's POOM:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // Line 149
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

**Line 149**: `deletend` operates only on the document's orgl (POOM) in the granfilade. There is **no corresponding call to remove spanfilade entries**.

Furthermore, **no deletion function exists for the spanfilade** — inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query operations:
- `insertspanf` ✓ [spanf1.c:15-54]
- `finddocscontainingsp` ✓ [spanf1.c:151-188]
- `deletespanf` ✗ **Does not exist**

### 3. COPY Creates the Stale Entries

When content is copied, both the POOM and spanfilade are updated [do1.c:45-65]:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  // ...
  return (
     specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
  && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && acceptablevsa (vsaptr, docorgl)
  
  /* the meat of docopy: */
  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)     // Line 60: Update POOM
  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // Line 62: Update spanfilade
  );
}
```

**Lines 60-62**: COPY updates both data structures. But DELETE [do1.c:158-167] only reverses line 60, not line 62.

---

## How Stale Entries Are Discovered

The caller cannot distinguish stale from current containment **at query time**. The distinction only becomes apparent when attempting to **retrieve content**:

### When Converting I→V Addresses

All retrieval operations convert I-addresses to V-addresses via the document's POOM. This conversion [orglinks.c:425-449] silently filters unreferenced addresses:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl,
                          typespanset restrictionspanptr, INT restrictionindex,
                          typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  
  // Try to find the I-span in the document's POOM
  context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                                restrictionindex, (typespan*)NULL,
                                targindex, (typeisa*)NULL);
  
  // Key line: if context is NULL, no V-spans are added
  if(!context){
    return(targspansetptr);  // Return without modification — I-address is silently dropped
  }
  // ...
}
```

**Lines 446-448**: If the I-address has no current POOM mapping (because the content was deleted), `retrieverestricted` returns NULL and the function returns without adding anything to the result.

### The User Experience

1. **FINDDOCSCONTAINING** returns: `[docA, docB]`
2. User attempts **RETRIEVEV** on docA with those I-addresses
3. Result: **Empty** (or partial, if only some content was deleted)
4. User attempts **RETRIEVEV** on docB with those I-addresses  
5. Result: **Full content** (docB still contains it)

The only way to distinguish is by attempting retrieval and observing empty results.

---

## Summary

| Question | Answer |
|----------|--------|
| Does FINDDOCSCONTAINING return document A? | **Yes** — stale DOCISPAN entries persist indefinitely |
| Can caller distinguish stale from current? | **No** — query returns document IDs only, with no staleness indicator |
| When is staleness discovered? | At **retrieval time** — I→V conversion returns empty for stale entries |
| Is this a bug? | **Uncertain** — may be intentional (see Finding 0057 architectural analysis) |

The spanfilade acts as a **historical journal** (documents that have **ever** contained these I-addresses) rather than a **current index** (documents that **currently** contain them).

This behavior is documented in **Finding 0057** and the filtering mechanism is documented in **Finding 0048**.

---

## Related Files

- `backend/spanf1.c:151-188` — `finddocscontainingsp` implementation
- `backend/do1.c:45-65` — `docopy` creates spanfilade entries
- `backend/do1.c:158-167` — `dodeletevspan` does not remove them
- `backend/orglinks.c:145-152` — `deletevspanpm` only updates POOM
- `backend/orglinks.c:425-449` — `span2spanset` filters unreferenced I-addresses
- `findings/0057-spanfilade-no-cleanup-on-delete.md` — Full analysis
- `findings/0048-followlink-returns-unreferenced-addresses.md` — Filtering mechanism
