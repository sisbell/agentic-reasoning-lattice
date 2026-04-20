## Question 20 [gregory]

> When multiple FEBE sessions are active and one session's INSERT allocates new I-addresses, does the run-to-completion scheduling guarantee that no other session can observe the granfilade in a state where the I-address exists but the content bytes are not yet stored?

## KB Synthesis

Yes, the guarantee holds. The answer follows from the interaction of three KB facts.

**Run-to-completion scheduling is total serialization**

[INV-SEQUENTIAL-DISPATCH] / [INV-ATOMICITY] (Finding 0042): The `bed.c` event loop calls `xanadu(&task)` and blocks until it returns before calling `select()` again. Even when multiple frontends have pending requests, they are dispatched one at a time. No two operations ever interleave.

**INSERT is a single `xanadu()` call**

[ST-INSERT] (Finding 0036) describes the full call chain within one invocation:

```
doinsert → inserttextingranf   (allocates I-addresses AND stores content bytes into a crum)
         → docopy → insertpm   (updates POOM)
                  → insertspanf (creates DOCISPAN)
```

All four steps complete before `xanadu()` returns. There is no yield point between I-address allocation and content storage.

**The in-memory state is shared globally**

[SS-SESSION-STATE] (Finding 0022): The granfilade is global state, not per-session. All sessions read from the same in-memory enfilade. Because run-to-completion ensures no other session runs during an INSERT, the first moment any other session can read the granfilade is after the inserting session's full `xanadu()` call completes — at which point both the I-address and its content bytes are already present in the in-memory crum (marked `modified = TRUE` per [SS-CACHE-MECHANISM] / Finding 0059).

**The disk durability question is separate and does not affect this**

[EC-CRASH-MID-WRITE] (Finding 0059) establishes that crums may not be on disk, but the question concerns observable state between live sessions, not crash recovery. Both the I-address and content bytes reside in the shared in-memory grim-reaper cache immediately after INSERT completes.

**Answer**: The run-to-completion guarantee is sufficient and complete. A session S2 can only observe the granfilade after S1's INSERT has finished executing, at which point the I-address and its content bytes are atomically present together in the in-memory state. The partial state — I-address allocated but content not yet stored — exists transiently within S1's `xanadu()` call and is invisible to all other sessions.

---

## Code Exploration

Now I have everything I need. Let me trace the complete picture across all relevant files.

---

## Answer

The run-to-completion scheduling **does guarantee** that no other session can observe the granfilade in a state where an I-address exists but its content bytes are not yet stored. The guarantee is structural — it flows from the event loop architecture, not from any explicit locking. Here is the evidence, layer by layer.

---

### Layer 1 — The event loop is single-threaded (bed.c)

```c
// bed.c:103-141
for (;;) {
    // ...
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];           // bed.c:120 — set global user
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                // ...
                xanadu(&task);                  // bed.c:128 — runs to completion
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

One request is handled at a time. `xanadu()` is called for session `i`, and only after it **returns** does the loop advance to the next ready file descriptor [bed.c:118–141]. The grep for `pthread`, `mutex`, `semaphore`, `fork`, and `SIGIO` across all backend `.c` files returns nothing. There are no threads, no async I/O signals, and no way for another session's code to run while `xanadu()` is executing.

`xanadu()` itself is equally simple [bed.c:153–172]:

```c
int xanadu(typetask *taskptr)
{
    // ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // bed.c:162 — full handler runs here
        sendresultoutput(taskptr);         // bed.c:163 — then flush output
    }
    tfree(taskptr);
    // ...
}
```

The request handler (e.g. `insert()`) runs to completion — including all data-structure mutations — before `sendresultoutput()` flushes and before control returns to the `select()` loop.

---

### Layer 2 — The INSERT handler (fns.c:84–98)

```c
void insert(typetask *taskptr)
{
    (void) getinsert(taskptr, &docisa, &vsa, &textset);  // fns.c:90
    putinsert(taskptr);                                   // fns.c:91 — buffers response
    if (!doinsert(taskptr, &docisa, &vsa, textset))      // fns.c:92 — does the work
        fprintf(stderr,"requestfailed in insert\n");
}
```

`putinsert()` buffers the response; `doinsert()` then mutates the granfilade. Both happen inside the same `xanadu()` invocation. stdout is explicitly buffered with `setbuf(stdout, outputbuffer)` [bed.c:90], and player output is flushed only via `sendresultoutput()` [bed.c:163] after `insert()` returns. Another session cannot receive the reply and act on it before `doinsert()` has completed.

---

### Layer 3 — doinsert's call sequence (do1.c:87–123)

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // do1.c:118
        && docopy(taskptr, docisaptr, vsaptr, ispanset));                 // do1.c:119
    return(ret);
}
```

`inserttextingranf` [granf1.c:44–47] is a thin wrapper: it calls `inserttextgr` [granf2.c:83–109], which is where the I-address is allocated and content is stored.

---

### Layer 4 — inserttextgr: address allocation and content storage (granf2.c:83–109)

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    typegranbottomcruminfo locinfo;

    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, &lsa))  // granf2.c:92
        return (FALSE);
    movetumbler(&lsa, &spanorigin);
    for (; textset; textset = textset->next) {          // granf2.c:95
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring,  // granf2.c:98
               locinfo.granstuff.textstuff.textlength);
        insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);  // granf2.c:99
        tumblerincrement(&lsa, 0, textset->length, &lsa);  // granf2.c:100
    }
    // build and return ispanset ...
}
```

`findisatoinsertgr` computes the next available I-address but does **not** write anything to the granfilade — it only reads. The address is held in local variable `lsa`.

`insertseq` [insert.c:17–70] then creates a new bottom crum and writes both the address metadata and the content bytes before returning:

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
{
    // ...
    new = createcrum(0, (INT)ptr->cenftype);          // insert.c:44
    reserve((typecorecrum*)ptr);
    reserve(new);
    adopt(new, RIGHTBRO, (typecorecrum*)ptr);         // insert.c:46 — link into tree
    ivemodified(new);
    splitsomething = splitcrumupwards(findfather(new));
    // ...
    moveinfo(info, &((typecbc*)new)->cinfo);          // insert.c:52 — write content bytes
    // then set width (address range) at lines 54–59
    ivemodified((typecorecrum*)ptr);
    setwispupwards(...);
    // ...
}
```

The new crum enters the tree via `adopt` [insert.c:46], and its content (`moveinfo` [insert.c:52]) and its width (I-address range, lines 54–59) are both set inside the same `insertseq` call. There is no yield point, no blocking I/O, and no other code that could run between these steps.

---

### Layer 5 — The multi-chunk case

If `textset` contains multiple chunks [granf2.c:95], `insertseq` is called once per chunk. After the first chunk's `insertseq` returns and before the second begins, the granfilade logically has an I-address for the first chunk but not the second. This is a real intermediate state — but it is **invisible to all other sessions** because the single-threaded event loop prevents any other `xanadu()` call from running until the entire `insert()` handler returns.

---

### Summary

| Guarantee | Mechanism | Evidence |
|---|---|---|
| No concurrent sessions | Single-process, no threads | No `pthread`/`fork` in backend; single `select()` loop |
| No preemption | Cooperative run-to-completion | `xanadu()` returns only after full handler completes [bed.c:128, 162–163] |
| No async interruption | No SIGIO, only SIGPIPE/SIGHUP/SIGINT | Signal handlers either crash or set a flag; no I/O occurs |
| I-address + content are co-installed | `insertseq` writes both in one call | `adopt` + `moveinfo` + width-setting in [insert.c:46–59] |
| Reply not flushed until after mutation | `putinsert` buffers; `sendresultoutput` flushes | [fns.c:91–92, bed.c:162–163] |

The run-to-completion guarantee is total: the granfilade is a purely in-memory enfilade structure, and the only observation point is a `retrievecrums()` call inside a future `xanadu()` invocation, which can only begin after the INSERT's `xanadu()` invocation has already returned and all crum insertions are complete.
