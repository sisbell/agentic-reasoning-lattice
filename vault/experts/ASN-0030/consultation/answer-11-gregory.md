## Question 11 [gregory]

> Once a byte is stored in the granfilade at a given I-address, is there any code path — including error handling or cache eviction via `grimlyreap` — that can overwrite or remove that byte from its I-address slot?

## KB Synthesis

No. Once a byte is written to the granfilade at a given I-address, no code path in the system overwrites or removes it.

**The allocation model is append-only by construction**

`inserttextingranf` allocates fresh I-addresses by querying the granfilade tree via `findpreviousisagr` to find the current maximum, then incrementing by one. New content always lands beyond all prior allocations. There is no free-list, no gap-filling, and no reuse mechanism. [INV-NO-IADDR-REUSE], [INV-MONOTONIC]

**DELETE and REARRANGE don't touch the granfilade**

DELETE (`deletevspanpm` → `deletend`) modifies only the document's POOM — it disowns and frees the B-tree crums that *map* V-positions to I-addresses. The I-addresses themselves, and the content bytes at those I-addresses in the granfilade, are untouched. `dodeletevspan` makes no call to any granf removal function. [FC-GRANF-ON-DELETE], [ST-DELETE], [INV-IADDR-IMMUTABILITY]

Same for REARRANGE: it calls `tumbleradd` on `cdsp.dsas[V]` (V-space displacement only). The granfilade is not consulted at all. [FC-GRANF-ON-DELETE]

**`grimlyreap` is write-back, not replacement**

When memory pressure triggers the grim reaper, it scans for crums with `age >= OLD` and `modified == TRUE`, writes them to disk via `orglwrite()`, then frees the in-memory structs. This is a write-back flush — the crum's content is written to *its own assigned disk block*, then the in-memory copy is released. The on-disk content at any previously written I-address block is never overwritten by this path. [SS-CACHE-MECHANISM]

The only wrinkle is [EC-CRASH-MID-WRITE]: if a crash occurs mid-write during `subtreewriterecurs` (which writes bottom-up: children before parents), structural pointers in the root may reference old blocks while new leaf blocks are orphaned. But this affects *tree navigation structure*, not the content bytes at leaf nodes. Leaf granf atoms that were already flushed to disk remain intact at their block addresses; no content byte is overwritten.

**The invariant is explicit throughout the KB**

> "The granfilade is append-only — `inserttextingranf` always allocates fresh addresses at the end. There is no mechanism to reuse, reassign, or deallocate I-addresses." — [INV-IADDR-IMMUTABILITY] (Finding 0064)

> "∀ i, t₁ < t₂ : i ∈ granfilade(t₁) ⟹ i ∈ granfilade(t₂) ∧ content(i, t₁) = content(i, t₂)" — [INV-IADDR-IMMUTABILITY]

This is the foundational Xanadu principle: bytes never die, addresses never change. The implementation honors it completely — there is no back door through error handling, cache pressure, or any other code path.

---

## Code Exploration

I now have everything I need. Here is my answer, with all claims grounded in the actual source code.

---

## Answer: I-Address Immutability in the Granfilade

**Short answer: No.** There is no code path — including `grimlyreap` — that can overwrite or remove a byte from its I-address slot. The granfilade is a strictly append-only, write-once store at the I-address level. Here is the full citation trail.

---

### 1. Insertion always moves forward — no I-address is ever reused

`inserttextgr` (`backend/granf2.c:83`):

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // line 100
}
```

`tumblerincrement` at line 100 advances `lsa` by `textset->length` after every segment. Since insertions always start from the **current high-water mark** (via `findisatoinsertgr`/`findpreviousisagr`) and always increment forward, no I-address is ever targeted twice.

---

### 2. `fillupcbcseq` appends — it never touches existing bytes

When a text crum has room, `insertseq` (`backend/insert.c:34-42`) tries to extend it in-place by calling `fillupcbcseq`:

```c
// insert.c:82-88
crumlength    = ptr->cinfo.granstuff.textstuff.textlength;
remainingroom = GRANTEXTLENGTH - crumlength;
textlength    = info->granstuff.textstuff.textlength;

if (remainingroom > textlength) {
    movmem(&info->granstuff.textstuff.textstring,
           (char*)(&(ptr->cinfo.granstuff.textstuff)) + crumlength,
           textlength);
    ptr->cinfo.granstuff.textstuff.textlength = crumlength + textlength;
```

The destination pointer is `+crumlength` bytes into the buffer — writing strictly **after** the existing bytes. Bytes at positions 0..crumlength-1 are never touched. The overflow path (lines 92-101) similarly writes at `+crumlength` up to `GRANTEXTLENGTH`, then renormalizes the *remaining* bytes in `info` (not in the crum). No overwrite of existing crum content occurs on either branch.

---

### 3. `grimlyreap` is a write-through cache flush, not destruction

When `falloc` fails, `ealloc` (`backend/credel.c:70-76`) calls `grimlyreap()`:

```c
if (grimreaper == NULL) {
    xgrabmorecore();
    continue;
}
grimlyreap();
```

`grimlyreap` (`credel.c:106-162`) iterates the circular `grimreaper` list looking for evictable crums:

```c
// credel.c:144-152
if (grimreaper->age == RESERVED) {
    continue;                    // skip — never evict reserved crums
}
if (isreapable (&eh, grimreaper)) {
    reap (grimreaper);
    ...
    break;
}
```

`reap` (`credel.c:292-330`) does one of two things:

- **Apex (orgl) crums** (line 309): `orglwrite((typecbc*)temp)` — serializes the orgl to disk via `orglwritepart2` (`corediskout.c:300`), then `orglfree` frees the in-core tree.
- **Non-apex crums** (line 329): `subtreewrite(temp)` — serializes the subtree to disk via `subtreewriterecurs` (`corediskout.c:426`), which for unmodified crums calls `loaffree(father)` (line 448) to release the in-memory copies.

The data is **written to disk before the memory is freed**. The I-address → data mapping survives in the disk representation. When the crum is needed again, `corediskin.c` reads it back.

---

### 4. RESERVED crums are immune to `grimlyreap`

`createorglgr` (`backend/granf2.c:111-128`) explicitly reserves every orgl it creates:

```c
// granf2.c:120-121
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
```

`reserve` (`credel.c:364-379`) sets `ptr->age = RESERVED`. The `grimlyreap` loop (`credel.c:144`) hits a `continue` for any such crum. `freecrum` (`credel.c:434-453`) also hard-errors if called on a RESERVED crum. Orgls can only be freed via `orglfree` (`credel.c:470`), which requires a valid disk pointer first — ensuring the content is on disk before the in-core tree is released.

`isreapable` (`credel.c:164-289`) has additional guards that propagate this protection upward: if any child is RESERVED or in-core with an open orgl, the parent is not considered reapable (e.g., lines 198-207, 244-257).

---

### 5. No compaction or slot relabeling exists

`split.c` and `recombine.c` restructure the enfilade tree (adopting and disowning crums, adjusting `cwid.dsas[WIDTH]` widths), but they never move byte content from one I-address to another. The I-address namespace is preserved through all splits and recombinations — they only partition and rebalance the tree topology.

---

### Summary

| Path | Effect on I-address bytes |
|---|---|
| `fillupcbcseq` | Appends after existing bytes; never overwrites bytes 0..crumlength-1 |
| `grimlyreap` → `reap` → `subtreewrite`/`orglwrite` | Flushes to disk, frees in-core; data is preserved at original I-addresses on disk |
| `grimlyreap` + `RESERVED` crums | Skipped entirely (`continue` at `credel.c:144`) |
| `recombine` / `split` | Tree topology only; no I-address relabeling |
| `createorglgr` | Always calls `reserve` before inserting — immune to reaping |

Once a byte is stored at a given I-address in the granfilade, that byte is immutable at that address for the lifetime of the data store.
