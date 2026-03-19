## Question 11 [gregory]

> Once a byte is stored in the granfilade at a given I-address, is there any operation — including internal maintenance, cache eviction, or disk compaction — that can change the byte value at that I-address, or is the mapping truly write-once-read-forever?

## KB Synthesis

## Yes — the granfilade mapping is write-once-read-forever for byte content.

The KB confirms this across multiple independent lines of evidence, with a few important caveats about durability vs. immutability.

### What never changes

**[INV-IADDR-IMMUTABILITY]** (Findings 0030, 0031, 0064) states it plainly: "I-addresses, once assigned to content, never change." The granfilade is append-only — `inserttextingranf` always allocates fresh addresses at the end and never overwrites existing entries. The Xanadu principle "bytes never die, addresses never change" is cited explicitly in **[FC-GRANF-ON-DELETE]**.

No documented operation mutates content bytes at an existing I-address:

- **DELETE** — operates exclusively on POOM V-to-I mappings via `deletend`. The granfilade is untouched: `dodeletevspan` has no call to any granf insertion or deletion function [FC-GRANF-ON-DELETE, ST-DELETE].
- **REARRANGE** — modifies V-address displacements only (`cdsp.dsas[V]`). I-addresses are never touched [ST-REARRANGE, INV-REARRANGE-IDENTITY].
- **CREATELINK** — allocates a new I-address for the link orgl; does not modify any existing I-address [ST-CREATE-LINK].
- **Tree rebalancing (split/recombine)** — `splitcrumseq`, `recombinend`, `levelpush` all restructure parent-child linkage and displacements; they do not modify bottom crum content bytes [ST-REBALANCE-2D, ST-SPLIT-2D].
- **Cache eviction (grim reaper)** — writes the in-memory crum faithfully to its assigned disk block via `orglwrite()`, then frees it. The write is a direct copy; no byte transformation occurs. The `modified` flag is cleared after the write and is only re-set by insert operations [SS-CACHE-MECHANISM].
- **Disk compaction** — the KB documents no compaction mechanism. `enf.enf` uses fixed-block allocation with no GC [SS-UNIFIED-STORAGE].
- **[INV-NO-IADDR-REUSE]** — deleted I-addresses are never reallocated. Even if content is removed from every document's V-stream, the I-address persists in the granfilade tree and the next allocation increments past it.

### The durability caveat (loss, not mutation)

**[INV-DURABILITY-BOUNDARY]** and **[SS-CACHE-MECHANISM]** note that in-memory content is not written to disk until `writeenfilades()` is called (session exit) or the grim reaper evicts the crum. A crash before either event loses the content — the I-address was allocated in memory but the bytes were never persisted. This is **loss**, not **mutation**: no byte at any I-address changes value; the address simply has no on-disk representation yet.

**[EC-CRASH-MID-WRITE]** describes a structural corruption scenario: the bottom-up write order (`subtreewriterecurs`) can leave the on-disk root pointing to stale subtree data while newly written children are orphaned. But again, this corrupts tree traversal — it does not change the byte values in any written block.

### Summary

Once a byte sequence is persisted to disk at an I-address, it is immutable. The only mechanisms that affect I-address content are:
1. Pre-persistence loss (crash before `writeenfilades()`) — bytes never reach disk
2. Post-crash tree corruption — previously written bytes become unreachable, but are unchanged on disk

There is no insert-update, no in-place edit, no compaction, and no eviction logic that overwrites existing content bytes. The granfilade is strictly append-only at every level of the storage stack.

---

## Code Exploration

I have now read all the relevant code. Here is my full answer.

---

## Is the Granfilade Truly Write-Once-Read-Forever?

**Yes. The I-address → byte mapping is write-once-read-forever.** No operation in the codebase — including insertion, deletion, cache eviction, disk block recycling, or enfilade restructuring — can change the byte value at a previously-assigned I-address. Every relevant code path was checked. Here is the evidence.

---

### 1. New Insertions Always Claim Fresh I-Addresses

The entry point for storing text bytes is `inserttextgr()` [`granf2.c:83`], which calls `findisatoinsertgr()` [`granf2.c:130`] to compute where to insert.

For text content (`ATOM` hint), `findisatoinsertmolecule()` is called [`granf2.c:158`]:

```c
// granf2.c:162-176
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr()` [`granf2.c:255`] walks the enfilade tree to find the **highest existing I-address** below the upper bound. The result is then incremented further to produce a strictly-greater address:

```c
// granf2.c:166-169
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);
```

The resulting `isaptr` is the start of the new allocation. It is **never equal to any existing I-address** — it always lands past everything already in the granfilade. Collision with existing content is structurally prevented.

---

### 2. The Only In-Memory Append Is Safe

Within `insertseq()` [`insert.c:17`], if the last bottom crum already holds GRANTEXT and has room, `fillupcbcseq()` is called to pack the new bytes in rather than allocating a new crum:

```c
// insert.c:34-42
if (info->infotype == GRANTEXT
 && ptr->cinfo.infotype == GRANTEXT
 && ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {
```

`fillupcbcseq()` [`insert.c:75`] writes **only at offset `crumlength`** — after the existing bytes:

```c
// insert.c:87
movmem(&info->granstuff.textstuff.textstring,
       (char*)(&(ptr->cinfo.granstuff.textstuff))+crumlength,
       textlength);
```

Bytes at offsets `0..crumlength-1` (the original content, at their original I-addresses) are **never touched**. The new bytes land at the immediately following I-addresses, which were freshly allocated by `findisatoinsertgr()`.

---

### 3. Cache Eviction Is Byte-Faithful

When memory pressure triggers the grim reaper, `grimlyreap()` [`credel.c:106`] calls `reap()` [`credel.c:292`], which calls `subtreewrite()` → `subtreewriterecurs()` [`corediskout.c:426`]. For each modified parent, `uniqueoutloaf()` [`corediskout.c:511`] packs the subtree to disk via `packloaf()` → `hputinfo()`.

For GRANTEXT crums, `hputinfo()` serializes:

```c
// corediskout.c:237-244
if (ptr->cinfo.infotype == GRANTEXT) {
    humberput(ptr->cinfo.granstuff.textstuff.textlength, ...);
    movmem(ptr->cinfo.granstuff.textstuff.textstring, (*loafptrptr),
           ptr->cinfo.granstuff.textstuff.textlength);
    *loafptrptr += ptr->cinfo.granstuff.textstuff.textlength;
```

And `hgetinfo()` reads it back verbatim:

```c
// corediskin.c:257-262
ptr->cinfo.granstuff.textstuff.textlength = intof((humber)*loafptrptr);
(*loafptrptr) += lengthof((humber)*loafptrptr);
movmem((*loafptrptr), ptr->cinfo.granstuff.textstuff.textstring,
       ptr->cinfo.granstuff.textstuff.textlength);
(*loafptrptr) += ptr->cinfo.granstuff.textstuff.textlength;
```

The round-trip is a literal `memcpy` of the `textstring` array. No transformation, no loss. The `textlength` is serialized as a prefix, so the reader knows exactly how many bytes to restore.

After eviction, the next access to those I-addresses triggers `findleftson()` [`genf.c:206`], which detects `ptr->leftson == NULL` and calls `inloaf()` [`corediskin.c:152`] to page the disk copy back in. The bytes returned are identical to what was stored.

---

### 4. `deletevspan` Does Not Touch the Granfilade

```c
// do1.c:158-167
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`findorgl()` retrieves the document's POOM orgl from the granfilade, then `deletevspanpm()` operates solely on that POOM (the virtual address tree), removing the V→I mapping entries. The granfilade itself — the 1D enfilade of I-addresses and their byte content — is **never written to** by this path.

Deleted content's bytes remain in the granfilade at their I-addresses. They are simply unreachable via V-space navigation from that document, but `ispan2vstuffset()` [`granf2.c:286`] would still retrieve them if given the I-span directly.

---

### 5. Disk Block Recycling Is Safe

When an enfilade parent crum is rewritten to a new disk block, the old block's reference count is decremented via `deletewithgarbageddescendents()` [`corediskout.c:388`]:

```c
// corediskout.c:397
if (!deletefullcrumflag || !changerefcount(diskptr,-1)) {
```

`changerefcount()` [`disk.c:60`] calls `diskfree()` when the count reaches zero, returning the block number to the free bitmap. `diskalloc()` [`diskalloc.c:27`] can then hand that number out for a new purpose.

However, by the time a block is freed, the live enfilade tree **no longer contains any pointer to that block**. The `sonorigin` fields in parent crums point to the new disk block (written before the old one was freed). Any lookup for the content that was once in the freed block will now follow the new block pointer and find the same bytes (since the content didn't change — only the tree structure around it was rewritten). The freed block may be reused for entirely new content at new I-addresses, and old I-addresses that previously lived in that block are no longer in scope from the tree's perspective.

There is no disk compaction pass. `diskfree()` / `diskalloc()` operate purely on block-number availability; bytes in old blocks are simply abandoned, not zeroed or compacted.

---

### 6. Enfilade Restructuring (Split) Moves Crums, Not Bytes

`splitcrumseq()` [`split.c:70`] triggers when a parent crum has too many children. It creates a new sibling parent and moves the rightmost half of the existing children to it:

```c
// split.c:83-89
for (i = 0, ptr = findrightmostson(father); i < halfsons && ptr; ++i, ptr = next) {
    next = findleftbro(ptr);
    disown(ptr);
    adopt(ptr, LEFTMOSTSON, new);
    rejuvinate(ptr);
    ivemodified(ptr);
}
```

Entire bottom crums (cbcs) — including their `textstring` — move as atomic units. No byte inside a crum's `textstring` is touched. The I-address ranges (`cwid`) of the moved crums are recomputed at the parent level via `setwispupwards()`, but the bytes remain exactly as stored.

`recombine()`, called from `insertseq()` at `insert.c:68`, triggers `splitcrumseq()` when the tree becomes unbalanced. Same property holds.

---

### 7. No Mechanism Exists for In-Place Overwrite

Surveying all write paths to `cinfo.granstuff.textstuff.textstring`:

- **`inserttextgr()`** → `insertseq()` → `moveinfo()`: copies a fresh info block into a freshly created crum. New crum, new I-address range.
- **`fillupcbcseq()`**: appends to existing crum at offset `crumlength`, never below it.
- **`hgetinfo()`** (`corediskin.c:257`): restores `textstring` from disk during page-in. This is a read-back, not a mutation.

There is no `memset`, no targeted overwrite, no `memmove` within an existing crum's byte buffer that could change a byte already placed at a given I-address. The source was checked completely.

---

### Conclusion

The granfilade's I-address space is **strictly append-only and immutable**:

| Operation | Effect on existing bytes at I-addresses |
|---|---|
| New text insertion | None — new I-addresses always beyond existing content |
| `fillupcbcseq()` append optimization | None — writes only past existing `textlength` offset |
| `deletevspan` | None — operates on POOM only, granfilade untouched |
| Cache eviction (reap) | None — faithful `memcpy` round-trip through disk |
| Disk block free/realloc | None — freed blocks are no longer tree-reachable |
| `splitcrumseq()` restructuring | None — moves whole crums atomically |
| No compaction exists | — |

**Once a byte is stored at I-address X, every future read of I-address X through the granfilade will return that same byte value, for the lifetime of the data store.** The mapping is truly write-once-read-forever.
