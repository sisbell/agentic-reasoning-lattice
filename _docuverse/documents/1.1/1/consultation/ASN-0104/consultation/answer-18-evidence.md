## Question 18 [evidence]

> Does a read that triggers cache eviction via the grim reaper ever return stale or partially-flushed bytes, or is operation-level atomicity (INV-ATOMICITY) sufficient to guarantee the read reflects current committed granfilade state?

## KB Synthesis

## Grim Reaper, Reads, and Atomicity

The KB provides enough to answer the cross-operation part of the question clearly, but leaves the within-operation part unresolved.

---

### What INV-ATOMICITY covers

[INV-ATOMICITY / Finding 0042] guarantees that the `xanadu(&task)` call in `bed.c` runs each FEBE operation to completion before `select()` is re-entered. No other session's writes can interleave with a read. So there is no staleness from concurrent modification — the in-memory enfilade IS the authoritative state [SS-CACHE-MECHANISM / Finding 0059], and no other operation can mutate it while a read is in flight.

---

### What INV-ATOMICITY does NOT cover

The grim reaper fires *within* the current operation's execution, triggered by `ealloc` during any memory allocation — including allocations that occur during read traversal (e.g., allocating a context list entry in `incontextlistnd`). When it fires, it scans the entire circular crum list and frees victims [SS-CACHE-MECHANISM / Finding 0059].

The protection mechanism documented in the KB is the `age == RESERVED` check in `ishouldbother` / `isreapable` [FC-RESERVED-CRUM / Finding 0071]. **But FC-RESERVED-CRUM is documented only in the context of rebalancing (`recombinend`).** The KB does not state whether crums actively being traversed by a read path (`findcbcinarea2d`, `retrieverestricted`, `permute`) are marked RESERVED or have their age reset to prevent eviction.

[EC-CROSS-ENFILADE-EVICTION / Finding 0059] explicitly confirms that memory pressure from one subsystem (e.g., a large link search loading spanfilade crums) can evict modified crums from another (e.g., recently-inserted granfilade text atoms). This is a within-operation hazard — not a cross-session hazard, but a consequence of the shared single-cache design.

---

### Conclusion

For **cross-operation read safety**, INV-ATOMICITY is sufficient: no concurrent writer can produce stale data visible to a reader, since the in-memory cache is the sole authoritative state and no other operation runs concurrently.

For **within-operation safety** (grim reaper evicting a crum while the same read traversal still holds a pointer to it), the KB cannot confirm correctness. The RESERVED mechanism protects crums during structural operations [FC-RESERVED-CRUM], but whether read traversals similarly protect their live crums is not documented. If they do not, memory pressure during a read could evict an in-use crum, producing a use-after-free — returning garbage bytes or crashing rather than stale-but-valid data.

**INV-ATOMICITY is necessary but, per the KB, not demonstrably sufficient for within-operation grim reaper safety during reads.**

---

## Code Exploration

The code is confirmed. Now I have everything I need for a precise, citation-backed answer.

---

## Does Grim Reaper Eviction Produce Stale or Partially-Flushed Reads?

**Short answer: No.** The reserve/rejuvinate protocol ensures node-level read safety during eviction, and write-before-free ensures disk always reflects committed state. INV-ATOMICITY at the operation level is sufficient — not because it prevents concurrent eviction, but because the underlying node-protection mechanism makes eviction-during-read structurally impossible.

---

### 1. When the Grim Reaper Runs

The grim reaper is not a background thread. It is invoked synchronously from `ealloc()` — only when `falloc()` returns NULL and the queue is exhausted:

```c
// credel.c:54-76
INT *ealloc(unsigned nbytes)
{
    for (;;) {
        if (ret = allocfromqueue(...)) return (INT *) ret;  // fast path
        ret = (char *)falloc(...);
        if (ret) return (INT *)(ret+sizeof(tagtype));
        if (grimreaper == NULL) { xgrabmorecore(); continue; }
        grimlyreap();  // credel.c:75 — only reached on allocation failure
    }
}
```

A read operation that causes a cache miss calls `inloaf()` [genf.c:225], which allocates memory for the newly-loaded children — this is the vector by which a read can trigger reaping.

---

### 2. The Node-Protection Protocol During Reads

`findleftson()` is the gateway for all demand-paging of on-disk nodes. It uses a strict bracket:

```c
// genf.c:206-232
typecorecrum *findleftson(register typecuc *ptr)
{
    INT oldage;
    oldage = ptr->age;              // save original age
    if (ptr->leftson == NULL) {
        if (ptr->sonorigin.diskblocknumber == DISKPTRNULL)
            return (NULL);
        reserve ((typecorecrum*)ptr);   // genf.c:216 — SET age=RESERVED
        inloaf (ptr);                   // genf.c:225 — read children from disk
        /* THIS IS A REAL REJUVINATE FOR A RESERVE */
        if (oldage != RESERVED)
            rejuvinate ((typecorecrum*)ptr);  // genf.c:227-228 — RESTORE age
    }
    rejuvinateifnotRESERVED (ptr->leftson);   // genf.c:230 — mark children young
    return (ptr->leftson);
}
```

If `inloaf()` must allocate and triggers `grimlyreap()`, the node being read has `age == RESERVED`. The reaper explicitly skips it:

```c
// credel.c:144-145
if (grimreaper->age == RESERVED) {
    continue;
}
```

`isreapable()` has a redundant guard at [credel.c:176]:

```c
if (localreaper->age < OLD || localreaper->age == RESERVED) {
    *fuckinap = 1;
    return (FALSE);
}
```

The node cannot be evicted mid-read by any path.

---

### 3. Write-Before-Free: No Partially-Flushed State on Disk

When a node **is** evictable (not RESERVED, old enough, not modified with loaded children), `reap()` always flushes before freeing:

```c
// credel.c:292-330
int reap(typecorecrum *localreaper)
{
    if (localreaper->isapex) {
        temp = (typecuc *)localreaper->leftbroorfather;
        grimreaper = grimreaper->nextcrum;
        if (!temp) return(0);
        orglwrite((typecbc*)temp);   // credel.c:309 — flush ORGL to disk first
        return(0);
    }
    temp = weakfindfather(localreaper);
    if (!temp->leftson) {
        grimreaper = grimreaper->nextcrum;
        return(0);
    }
    subtreewrite(temp);              // credel.c:329 — flush subtree to disk first
}
```

`isreapable()` also blocks eviction of any node with `modified == TRUE` [credel.c:185-195, 261-286] and any node with loaded children that are modified [credel.c:193-207]. This means the reaper never touches a dirty node that hasn't been fully written down — the invariant is: **a node is only freed after its subtree is durably flushed**.

---

### 4. Tree Traversal Keeps the Entire Read Path Young

Every navigation accessor calls `rejuvinateifnotRESERVED()` on nodes it touches:

```c
// genf.c:24-41
typecorecrum *getleftson(typecuc *ptr) {
    rejuvinateifnotRESERVED((typecorecrum *)ptr);  // marks visited node as age=NEW
    ptr = (typecuc *)ptr->leftson;
    if (ptr) rejuvinateifnotRESERVED((typecorecrum *)ptr);
    return ((typecorecrum *)ptr);
}

typecorecrum *routinegetrightbro(typecorecrum *ptr) {
    rejuvinateifnotRESERVED((typecorecrum *)ptr);  // genf.c:36
    ptr = ptr->rightbro;
    if (ptr) rejuvinateifnotRESERVED((typecorecrum *)ptr);
    return(ptr);
}
```

The reaper ages nodes incrementally — `grimreaper->age++` at [credel.c:159], only one node is reaped per `grimlyreap()` call. Any node touched during the current read path gets reset to `age=NEW` and won't age to `OLD` before the read completes.

---

### 5. No Explicit Locking — Design Relies on Single-Threaded Execution

There are no mutexes, semaphores, or CPU atomic ops. The `ingrimreaper` flag [credel.c:112,161] prevents allocation from calling `grimlyreap()` recursively from within a reap. The `reaplevel` counter [credel.c:113] detects and warns on reentrancy. The design is single-threaded: one FEBE operation runs to completion before the next, and within that operation, the reserve protocol handles the reentrancy case where allocation during `inloaf()` triggers the reaper.

---

### Conclusion

**INV-ATOMICITY is sufficient**, but not because it directly prevents eviction. It works because:

1. **RESERVED blocks eviction** [credel.c:144-145, credel.c:176] — any node in the demand-paging path of a read is bracketed by `reserve()`/`rejuvinate()` in `findleftson()` [genf.c:216,228], making it invisible to the reaper.

2. **Write-before-free** [credel.c:309, 329] — eviction always flushes modified data to disk before releasing the node. The disk always reflects the latest committed granfilade state.

3. **Modified-flag guard** [credel.c:185-207] — the reaper cannot evict dirty nodes or subtrees with dirty children, so partial flushes cannot reach disk in an inconsistent state.

A read that triggers grim reaper eviction will not return stale or partially-flushed bytes. The node being read is RESERVED and unreapable; nodes already evicted were flushed complete before release; and the entire traversal path is kept young by `rejuvinateifnotRESERVED()` at every step.
