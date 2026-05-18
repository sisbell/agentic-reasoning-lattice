## Question 12 [evidence]

> Do udanax-green's compound document operations (e.g., `docreatenewversion` followed by content insertion and provenance recording, or `docreatelink` which combines link allocation with placement) execute as transactional atoms with no externally-observable intermediate state, or can concurrent operations observe states where allocation has occurred but placement or provenance recording has not?

## KB Synthesis

## Atomicity of Compound Operations in udanax-green

The answer splits cleanly into two dimensions: **concurrency atomicity** (observable by other sessions) and **crash atomicity** (survivable across process failure).

---

### Concurrency Atomicity: Full Isolation Guaranteed

No concurrent operation can observe a partial state of `docreatenewversion` or `docreatelink`.

The mechanism is the `bed.c` event loop, which uses run-to-completion scheduling via a sequential `select()` → `xanadu(&task)` dispatch [INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY]. Each FEBE request is processed to completion — including all internal sub-steps — before the loop returns to `select()` to accept the next request. There are no threads and no state-modifying signal handlers.

Concretely:
- `docreatenewversion`: orgl allocation, vspanset retrieval, and content copy all execute before any other session's request is serviced [INV-ATOMICITY, ST-VERSION-CREATE]
- `docreatelink`: the three-step sequence (create link orgl in granf → place V→I mapping in document POOM → index endpoints in spanf) executes entirely before any other operation runs [ST-CREATE-LINK]

This is stronger than per-document serialization — all sessions globally serialize.

---

### Crash Atomicity: No Guarantee

Neither operation is transactional with respect to process failure.

`docreatelink` is the critical case. The three-step write sequence [ST-CREATE-LINK, SS-DUAL-ENFILADE-CONSISTENCY]:
1. `createorglingranf()` — allocates link orgl in granf
2. `docopy()` → `insertpm()` — places link reference in document POOM
3. `insertendsetsinspanf()` — indexes endpoints in spanf

There is no rollback mechanism. If the process crashes between steps 1 and 3, a link orgl exists in granf but is not discoverable via `find_links` (spanf not updated). [INV-DUAL-ENFILADE-CONSISTENCY] explicitly notes this: "partial failures during `docreatelink` could violate this invariant."

`docreatenewversion` also lacks crash atomicity. The granf write for the new document address and the spanf copy of DOCISPAN entries are separate. A crash between them leaves a document address allocated but with no indexed content [SS-DURABILITY-BOUNDARY, FC-GRANF-ON-VERSION].

The underlying storage layer writes crums lazily via grim reaper eviction or on clean session exit — there is no `fsync`, no transaction log, and no startup validation [SS-DURABILITY-BOUNDARY, EC-CRASH-MID-WRITE, EC-NO-STARTUP-VALIDATION].

---

### Summary

| Dimension | `docreatenewversion` | `docreatelink` |
|-----------|---------------------|----------------|
| Concurrent observability | Fully atomic [INV-SEQUENTIAL-DISPATCH] | Fully atomic [INV-SEQUENTIAL-DISPATCH] |
| Crash safety | None [SS-DURABILITY-BOUNDARY] | None [INV-DUAL-ENFILADE-CONSISTENCY] |

The formal spec should model these as atomic state transitions in the concurrent execution model, but must document that the atomicity guarantee is conditional on no process failure during execution — crash scenarios leave the system in potentially inconsistent states with no recovery path.

---

## Code Exploration

I have all the code I need. Let me now compose the full answer with precise citations.

---

## Transactional Atomicity of Compound Operations in udanax-green

### Short answer

Compound operations like `docreatenewversion` and `docreatelink` are **effectively atomic with respect to other FEBE clients**, but not because of any explicit locking, journaling, or rollback mechanism. They are atomic by architectural accident: the backend is a **single-threaded, cooperative event loop** that processes one complete FEBE request to completion before servicing the next. No intermediate state is ever externally observable under normal operation.

---

### The Event Loop: Single-Threaded, Non-Preemptive

The entire concurrency architecture lives in `bed.c`. The `main()` function runs a single `select()` loop [bed.c:103-149]:

```c
for (;;) {
    ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ...
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                ...
                xanadu(&task);    /* [bed.c:128] */
            }
        }
    }
```

`xanadu()` [bed.c:153-172] processes exactly one FEBE request per call:

```c
int xanadu(typetask *taskptr)
{
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    /* [bed.c:162] */
        sendresultoutput(taskptr);          /* [bed.c:163] */
    }
    tfree(taskptr);
}
```

The critical structural facts are:

1. There are **no threads** — no `pthread_create`, no `fork` during request handling.
2. The `for (i = 0; i <= nfds; i++)` inner loop [bed.c:118] iterates over all ready FDs, but calls `xanadu()` to completion for each before moving to the next.
3. `xanadu()` never calls `select()` itself, never yields, and never calls `new_players()` mid-request. There are no preemption points within a request handler.

This means: **the entire call chain of any compound operation runs uninterrupted between one `xanadu()` entry and its `tfree()` at [bed.c:168]**.

---

### `docreatelink`: Sub-Steps Are Not Individually Committable

`docreatelink` [do1.c:194-220] chains ten sub-operations via short-circuit `&&` evaluation:

```c
return (
    createorglingranf (taskptr, granf, &hint, linkisaptr)        /* [do1.c:209] — allocate link ISA */
 && tumbler2spanset (taskptr, linkisaptr, &ispanset)             /* [do1.c:210] — ISA → spanset */
 && findnextlinkvsa (taskptr, docisaptr, &linkvsa)               /* [do1.c:211] — find placement VSA */
 && docopy (taskptr, docisaptr, &linkvsa, ispanset)              /* [do1.c:212] — place link in document */
 && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED) /* [do1.c:213] — find link's own orgl */
 && specset2sporglset (taskptr, fromspecset, &fromsporglset, …)  /* [do1.c:214] */
 && specset2sporglset (taskptr, tospecset,   &tosporglset,   …)  /* [do1.c:215] */
 && specset2sporglset (taskptr, threespecset,&threesporglset,…)  /* [do1.c:216] */
 && setlinkvsas (&fromvsa, &tovsa, &threevsa)                    /* [do1.c:217] */
 && insertendsetsinorgl (taskptr, linkisaptr, link, …)           /* [do1.c:218] — write endpoints to link orgl */
 && insertendsetsinspanf (taskptr, spanf, linkisaptr, …)         /* [do1.c:219] — index endpoints in spanf */
);
```

Conceptually, allocation [line 209] is fully complete and the ISA (`*linkisaptr`) has an address in the granfilade before placement [line 212] or endpoint registration [lines 218-219] occur. But **no other client can observe this intermediate state** because `xanadu()` has not returned. The entire `docreatelink` chain is a single C expression evaluated sequentially within one request dispatch.

---

### `docreatenewversion`: Sequential Steps, No Error Recovery

`docreatenewversion` [do1.c:259-298] is the compound operation with the most visible sub-step structure:

```c
/* Step 1: allocate the new document ISA in granf */
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
    return (FALSE);                                              /* [do1.c:277-279] */
}

/* Step 2: retrieve the source document's vspan */
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;                                               /* [do1.c:281-283] */
}

/* Step 3: open, copy, mark modified, close */
addtoopen(newisaptr, user, TRUE, WRITEBERT);                    /* [do1.c:292] */
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);      /* [do1.c:293] */
logbertmodified(newisaptr, user);                               /* [do1.c:295] */
doclose(taskptr, newisaptr, user);                              /* [do1.c:296] */

return (TRUE);
```

Between steps 1 and 2 — after the new ISA exists but before content is copied — the system is in a logically inconsistent state: the document address is allocated but the document is empty. This intermediate state is **never visible to another FEBE client** because the event loop at [bed.c:128] will not dispatch any other `xanadu()` call until this one has returned.

However, there is a **failure-handling vulnerability that is distinct from concurrency**: after `addtoopen()` at [do1.c:292], the return values of `docopyinternal()` and `logbertmodified()` are **not checked**. If `docopyinternal` fails silently, `doclose()` will still be called, potentially closing an empty document that was registered in the bert table. This is not a concurrency exposure — no concurrent client will see the in-progress empty state — but it does mean a partially-constructed version can be silently committed as the final state.

---

### Summary Table

| Compound Operation | Intermediate states externally observable? | Why not |
|---|---|---|
| `docreatelink` [do1.c:194] | No | Single-threaded event loop; all 10 sub-steps run within one `xanadu()` call [bed.c:162] |
| `docreatenewversion` [do1.c:259] | No | Same: steps 1-6 complete before `xanadu()` returns [bed.c:162-168] |
| `doinsert` [do1.c:86] | No | Calls `inserttextingranf` then `docopy` [do1.c:117-118] within a single request dispatch |

**The backend has no rollback, no journal, and no MVCC.** Its "atomicity" is purely structural: the C program is single-threaded, the event loop at [bed.c:103-149] serializes all requests, and no preemption points exist within a request handler. Atomicity is guaranteed only for the normal case. Partial failure mid-compound-operation (specifically in `docreatenewversion` after [do1.c:292]) can leave logically inconsistent committed state, but that inconsistency will never be the result of a race between two FEBE clients.
