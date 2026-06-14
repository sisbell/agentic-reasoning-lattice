## Question 17 [evidence]

> Within a single INSERT, `insertpm` writes the POOM before `insertspanf` writes the DOCISPAN entry — can any reader (including a concurrent session) observe POOM content whose I-span has no corresponding spanfilade entry yet, and is that ordering relied upon anywhere?

## KB Synthesis

## POOM-before-DOCISPAN ordering within INSERT

**No live reader can observe the intermediate state.** The ordering has crash-recovery implications but no concurrency implications.

### Why no concurrent reader sees the gap

[INV-ATOMICITY] (Finding 0042) and [INV-SEQUENTIAL-DISPATCH] (Finding 0042) together establish that the backend event loop is single-threaded and run-to-completion. Every FEBE request executes entirely — including the full `doinsert` → `inserttextingranf` → `docopy` chain — before `select()` is called again for the next session's request. Even if two sessions have requests simultaneously ready on their file descriptors, the loop services them one-at-a-time.

Within `docopy` itself, `insertpm` and `insertspanf(..., DOCISPAN)` execute back-to-back in the same call frame (`do1.c:45-65` per [ST-INSERT], Finding 0036). No context switch, no yield point, no signal handler can interpose between them.

**A concurrent session cannot ask `find_documents` (which reads spanfilade) and get a "hit" on I-addresses whose POOM entry was already written but whose DOCISPAN entry has not yet been written**, because the other session's request cannot run until the inserting session's `docopy` returns and the entire `xanadu()` call completes.

### Where the ordering IS load-bearing: crash recovery

[EC-CRASH-MID-WRITE] (Finding 0059) identifies the real vulnerability. `docopy` writes POOM first, then DOCISPAN. A crash between them leaves:

- **POOM updated**: `retrieve_contents` on the new V-span returns the inserted bytes.
- **DOCISPAN absent**: `find_documents` does not include this document for the freshly allocated I-addresses.

This directly violates [INV-DUAL-ENFILADE-CONSISTENCY] (Finding 0012), which requires every document whose content lives in the granf to be indexed in the spanfilade. Because [EC-NO-STARTUP-VALIDATION] (Finding 0059) confirms there is no consistency check on startup, the system will silently reload the diverged state.

The diverged state after such a crash is structurally identical to the already-documented post-DELETE divergence: POOM and spanfilade out of sync, with [INT-DELETE-SPANF-DIVERGENCE] (Finding 0057) describing it as the normal post-delete condition and [EC-STALE-SPANF-REFERENCE] noting the weaker invariant that spanfilade is a superset (not equal to) current POOM associations. A crash-mid-INSERT would produce the inverse: POOM has entries the spanfilade doesn't, meaning `retrieve_contents` succeeds but `find_documents` misses the document.

### Is the ordering itself relied upon by any code?

Not explicitly. The code does not assert or test that POOM precedes DOCISPAN. The ordering is an artifact of `docopy`'s call sequence. No downstream code reads POOM state and assumes DOCISPAN is in sync immediately after (the sequential dispatch guarantee makes this a non-issue for live queries). The only implicit reliance is the assumption embedded in [INV-DUAL-ENFILADE-CONSISTENCY] that after any complete operation both layers agree — a property that holds under normal execution and is violated only by crashes between the two sub-writes.

---

## Code Exploration

I now have everything I need. Let me write the full answer.

---

## Answer

### The Call Chain

The INSERT path traces:

**`fns.c:84-98`** — `insert()`:
```c
(void) getinsert (taskptr, &docisa, &vsa, &textset);
putinsert (taskptr);          // queues response BEFORE work
if (!doinsert (taskptr, &docisa, &vsa, textset))
    fprintf(stderr,"requestfailed in insert\n");
```

**`do1.c:117-122`** — `doinsert()`:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset));
```

**`do1.c:54-64`** — `docopy()`:
```c
return (
   specset2ispanset (...)
&& findorgl (...)
&& acceptablevsa (...)
&& asserttreeisok (docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // ← POOM write
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // ← spanfilade write
&& asserttreeisok (docorgl));
```

So `insertpm` always precedes `insertspanf` in a `&&`-chained sequence. The question is whether any reader can see the POOM updated but the spanfilade not yet.

---

### What These Writes Actually Do

**`insertpm` [`orglinks.c:75-134`]** calls `insertnd` on the document's per-document POOM enfilade (`orgl`), which is an in-memory B-tree-like structure. It calls `logbertmodified` (marks the document dirty in the access-control table) and terminates every modified node with `ivemodified`.

**`insertspanf` [`spanf1.c:15-53`]** calls `insertnd` on the global `spanf` enfilade, writing the DOCISPAN entry that maps the new I-span back to the document's ISA.

**`ivemodified` [`genf.c:522-544`]** does only this:
```c
ptr->modified = TRUE;
```
It sets a boolean flag in memory. There is no disk write, no `write()`, no `fsync()`, no blocking syscall anywhere inside either `insertpm` or `insertspanf`. All state lives in the in-memory enfilade tree.

**Disk writes are deferred entirely** to idle time or shutdown: `diskflush()` is called at `bed.c:105` when no players remain, and `writeenfilades()` at `bed.c:134` and `bed.c:183` on quit. There is no disk checkpoint inside any request handler.

---

### The Event Loop Is Strictly Sequential

**Single-user backend (`be.c:90-95`)**:
```c
for (;;) {
    ntaskorcommand++;
    xanadu (&task);      // one request, runs to completion
    logfile = nulllog;
}
```

**Multi-user backend (`bed.c:103-143`)**:
```c
for (;;) {
    inputfds2 = inputfds;
    select(nfds+1, &inputfds2, 0, 0, &timeout);
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];
            xanadu(&task);     // ← runs user i's request TO COMPLETION
            ntaskorcommand++;
        }
    }
    leave(...); new_players(...);
}
```

The inner `for` loop iterates across all ready file descriptors, but each `xanadu()` call runs to completion before `i` advances. There is no preemption, no thread, no cooperative yield inside any handler. Even if 10 users have pending input at the moment `select()` returns, their requests are dispatched one at a time in sequence.

**`xanadu()` in `be.c:99-118`** (same structure in `bed.c:153-172`):
```c
if (getrequest (taskptr, &request)) {
    (*requestfns[request]) (taskptr);   // calls insert() → doinsert()
    sendresultoutput (taskptr);          // ← fflush() happens here
}
tfree (taskptr);
```

`sendresultoutput` is simply `fflush(taskptr->outp)` [`putfe.c:85`]. It fires **after** the handler returns — which means after `doinsert()` completes. The `putinsert()` call at `fns.c:91` that precedes `doinsert()` only writes bytes into stdio's user-space output buffer. Those bytes do not reach any client's socket until `sendresultoutput()` flushes them, which only happens after `insertpm` and `insertspanf` have both completed.

---

### Can a Reader Observe the Partial State?

**No — for in-session concurrent readers.**

The sequence `insertpm() → insertspanf()` inside `docopy()` runs atomically from any other session's perspective:

1. Both functions are pure in-memory computations with no blocking I/O or yield points.
2. The event loop processes one `xanadu()` call to completion before the next begins.
3. Even in the multi-user `bed.c`, user B's request cannot start until user A's `xanadu()` returns.
4. The `putinsert()`-before-`doinsert()` pattern in `fns.c:91` does not create a race window: the queued response bytes stay in stdio's buffer until `sendresultoutput()` flushes them after `doinsert()` finishes.

**For disk-recovery (crash) scenarios:** Because all enfilade writes are in-memory until `writeenfilades()`, a crash between `insertpm` and `insertspanf` would not be observed by a reader, but it would leave the on-disk image with either both changes or neither — depending on exactly when the crash hit a `writeenfilades()` call. This is the only scenario where the two-step ordering could matter for persistent correctness. The code provides no recovery mechanism for this.

---

### Is the Ordering Relied Upon Anywhere?

Not for concurrent-reader safety — the single-threaded event loop makes the ordering irrelevant for that concern.

The ordering does carry a subtle semantic preference for the **error/crash partial-failure case**:

- **POOM-first (current)**: If something fails after `insertpm` but before `insertspanf` succeeds (e.g. `insertspanf` returned `FALSE`, though in practice `spanf1.c:53` always returns `TRUE`), the document retains V→I retrievability (the POOM maps virtual positions to I-addresses) but appears absent from the inverse I→doc lookup (`finddocscontainingsp`/DOCISPAN). This is a degraded-but-safe state: content is retrievable from the document, just not discoverable by content-identity search.

- **Spanfilade-first (hypothetical)**: If `insertspanf` succeeded but `insertpm` failed, the DOCISPAN entry would claim an I-span belongs to this document, but the POOM would have no mapping to serve retrieval requests from. That would cause retrieval failures — strictly worse.

The comment at `do1.c:29-31` also captures the coupling explicitly:
```c
return (appendpm (taskptr, docptr, textset)/*&&
   appendpm includes insertspanf!  insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
);
```
`appendpm` calls `doinsert()` → `docopy()`, so `insertspanf` is always invoked inside `appendpm`'s recursion, not separately. The design treats them as a pair, not as independently schedulable operations.

---

### Conclusion

No reader — concurrent session or otherwise — can observe POOM content whose I-span has no corresponding spanfilade entry. The backend is single-threaded with a non-preemptive request loop (`bed.c:103-143`, `be.c:90-95`). Both `insertpm` and `insertspanf` are pure in-memory operations with no blocking calls, and `sendresultoutput()` (the network flush) fires only after the entire handler returns. The window between the two writes is invisible to any other request.

The POOM-before-spanfilade ordering is not relied upon for concurrency safety — it doesn't need to be. Its only practical significance is that it chooses the less-destructive failure mode: an orphaned POOM entry (invisible to content-identity search) rather than an orphaned DOCISPAN entry (causing active retrieval failures). The code at `do1.c:60-62` expresses this through short-circuit `&&`: `insertspanf` is never called if `insertpm` fails.
