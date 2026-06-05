## Question 11 [evidence]

> When a contiguous V-span is read via `retrieverestricted`, does the returned content reflect the POOM's V→I mapping as it exists at that instant, or can cached enfilade nodes return a stale arrangement after a prior INSERT/DELETE in the same session?

## KB Synthesis

`retrieverestricted` always reflects the current POOM state. Three KB properties jointly guarantee this.

**Sequential dispatch eliminates interleaving** [INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY]. The event loop processes each FEBE operation run-to-completion via `xanadu(&task)` before returning to `select()`. A RETRIEVE call cannot interleave with a preceding INSERT—the INSERT's POOM modifications are fully committed before RETRIEVE begins.

**The in-memory tree IS the cache with no separate buffer** [SS-CACHE-MECHANISM]. INSERT marks modified crums via `ivemodified()` but leaves them in the grim reaper circular list. A subsequent `retrieverestricted` walking the same POOM tree reads those in-memory crums directly—no disk round-trip, no staleness.

**Write-before-evict maintains coherence across eviction** [SS-CACHE-MECHANISM]. When the grim reaper frees a crum under memory pressure, it calls `orglwrite()` first. The on-disk state is always current state. If a crum is evicted during an INSERT (say, to make room for new leaf nodes) and later needed by a RETRIEVE, the reload from disk yields the post-INSERT content. The cache invariant is: every crum is either in the grim reaper list (current) or on disk at its assigned block (written when last evicted, also current)—never neither.

**The one coherence risk is cross-enfilade eviction** [EC-CROSS-ENFILADE-EVICTION]. A large link search loading spanfilade crums can evict modified granfilade text atoms. But write-before-evict still holds—the evicted crum is on disk with its current content before being freed. The RETRIEVE reloads it correctly.

**Summary**: `retrieverestricted` sees the POOM exactly as the last completed INSERT/DELETE left it. No stale arrangement is possible within a session because [INV-SEQUENTIAL-DISPATCH] prevents interleaving and [SS-CACHE-MECHANISM]'s write-before-evict ensures disk state tracks in-memory state.

---

## Code Exploration

I now have enough to give a complete, cited answer.

---

## Answer: `retrieverestricted` and V→I Mapping Freshness

**Short answer: `retrieverestricted` always reflects the POOM's V→I mapping as it exists at the instant of the call. There is no cache; it reads live in-memory node fields. The design guarantees freshness through two complementary mechanisms: relative addressing and eager in-place mutation.**

---

### 1. How `retrieverestricted` traverses the POOM

`retrieverestricted` [retrie.c:56-85] computes tumbler endpoints and delegates to `retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` [retrie.c:229-268].

`findcbcinarea2d` walks the live in-memory POOM tree:
- At each internal node it reads `crumptr->cdsp` and `crumptr->cwid` directly to qualify or skip the subtree [retrie.c:253, `crumqualifies2d`].
- Offset accumulates top-down: `dspadd(offsetptr, &crumptr->cdsp, &localoffset, ...)` [retrie.c:258].
- At leaf nodes it calls `makecontextfromcbc` and adds to the result list [retrie.c:262-263].

There is no separate result cache, memoisation table, or snapshot. Every call to `retrieverestricted` traverses the tree reading `cdsp`/`cwid` from the in-memory nodes exactly as they stand.

---

### 2. How INSERT mutates the V→I mapping

`doinsert` [do1.c:87-123] → `docopy` [do1.c:45-65] → `insertpm` [orglinks.c:75-134] → `insertnd` [insertnd.c:15-111].

For the POOM enfilade, `insertnd` calls `makegappm` first [insertnd.c:54]:

```c
/* insertnd.c:51-61 */
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);
    setwispupwards(fullcrumptr,0);
    bothertorecombine = doinsertnd(fullcrumptr,origin,width,infoptr,index);
    setwispupwards(fullcrumptr,1);
    break;
```

`makegappm` [insertnd.c:124-172] finds the intersection father, then walks its **immediate children** and shifts any crum that lies to the right of the insertion point:

```c
/* insertnd.c:151-165 */
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 1:  /* crum is to the right of insertion */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
        ivemodified(ptr);
        break;
    }
}
setwidnd(father);
setwispupwards(findfather((typecorecrum*)father), 1);
```

**Only immediate children are updated.** This is correct by design (see §4 below).

---

### 3. How DELETE mutates the V→I mapping

`dodeletevspan` [do1.c:158-167] → `deletevspanpm` [orglinks.c:145-152] → `deletend` [edit.c:31-76].

`deletend` makes cuts, then walks the father's children and subtracts the deleted width from any crum to the right:

```c
/* edit.c:62-63 */
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

Then propagates upward: `setwispupwards(father, 1)` [edit.c:74].

---

### 4. Why only immediate children need updating (relative addressing)

The POOM enfilade stores **relative** displacements. Each crum's `cdsp` is relative to the accumulated offset of its parent context, not an absolute V address. Retrieval in `findcbcinarea2d` accumulates context as it descends:

```c
/* retrie.c:258 */
dspadd(offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...);
```

So when `makegappm` adds `width->dsas[V]` to an immediate child's `cdsp`, every node in that child's subtree automatically inherits the shift through the accumulated offset — their own `cdsp` values (relative to their parent) are unchanged and remain correct. There is no need to touch grandchildren.

This is also why `setwispupwards` → `setwispnd` [wisp.c:171-228] only needs to recompute bounding boxes going upward, not the child offsets going downward.

---

### 5. `setwispupwards` is synchronous and eager

`setwispupwards` [wisp.c:83-111] walks from the modified node up to the fullcrum, calling `setwisp` → `setwispnd` at each level:

```c
/* wisp.c:95-101 */
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather((typecorecrum*)ptr);
    changed = setwisp((typecorecrum*)ptr);
    ...
}
```

`setwispnd` [wisp.c:171-228] recomputes both `cdsp` (minimum bounding origin) and `cwid` (bounding extent) across all children, updating the node in place. This completes **before `insertnd`/`deletend` returns**, so by the time any subsequent `retrieverestricted` call begins, all interior node bounding boxes are fresh.

---

### 6. No stale state from disk eviction

`findleftson` [genf.c:206-232] may load a subtree from disk if `ptr->leftson == NULL`:

```c
/* genf.c:212-229 */
if (ptr->leftson == NULL) {
    if (ptr->sonorigin.diskblocknumber == DISKPTRNULL) return (NULL);
    reserve((typecorecrum*)ptr);
    inloaf(ptr);
    rejuvinate((typecorecrum*)ptr);
}
```

But disk eviction is safe because every `cdsp` modification calls `ivemodified(ptr)` [insertnd.c:163, edit.c: via setwispupwards] which sets `ptr->modified = TRUE` up the chain [genf.c:522-544]. On eviction, `subtreewriterecurs` [corediskout.c:426-494] checks `modified` and writes the node to disk with its current `cdsp`/`cwid` before freeing memory [corediskout.c:438, 489]. On reload, `inloaf` [corediskin.c:152-170] reads the current disk version (which has the post-mutation values) and sets `modified = FALSE` [corediskin.c:148].

There is no window in which a node with a stale `cdsp` could be on disk and then reloaded, because `ivemodified` + the write-before-free discipline prevents it.

---

### 7. Historical note on `setwispupwards` completeness

Commented-out `#ifdef UNdeFINed` blocks in `insertnd.c` [lines 32, 98] include `fixincoresubtreewids` described as "a brute force kluge till we find where setwispupwards isn't called." This is historical developer uncertainty — these blocks are entirely disabled (`UNdeFINed` is never defined) and were presumably debug scaffolding. They indicate that at some point during development there were concerns about `setwispupwards` coverage, but the production code paths in `insertnd.c:56-58` and `edit.c:74` call it explicitly.

---

### Summary

| Concern | Verdict | Key evidence |
|---|---|---|
| Does `retrieverestricted` read a snapshot or live state? | Live state — reads `cdsp`/`cwid` from in-memory nodes | retrie.c:252-263, `crumqualifies2d` reads fields directly |
| Does INSERT update the tree before returning? | Yes — `makegappm` shifts children and `setwispupwards` propagates to root | insertnd.c:162-163, insertnd.c:56-58, wisp.c:83-111 |
| Does DELETE update the tree before returning? | Yes — `deletend` shifts children and `setwispupwards` propagates to root | edit.c:62-63, edit.c:74 |
| Do deeper descendants (not immediate children) need updating? | No — relative addressing means child-relative `cdsp` values stay correct | retrie.c:258 accumulation design |
| Can disk-reloaded nodes return stale `cdsp`? | No — `ivemodified` + write-before-evict ensures disk has current values | corediskout.c:438-489, genf.c:539 |

**`retrieverestricted` returns content that fully reflects the POOM's V→I mapping as mutated by all prior INSERTs and DELETEs in the session. There is no staleness mechanism.** The only scenario where results could appear surprising is a bug where `setwispupwards` is not called after a mutation — but the standard code paths call it unconditionally.
