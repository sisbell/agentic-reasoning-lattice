## Question 11 [evidence]

> In `bed.c`'s event loop, is the unit of run-to-completion a single FEBE request, and does a multi-span SpecSet operation (e.g., a COPY that `vspanset2sporglset` splits into several sporgls) fully complete all its POOM, granfilade, and spanfilade writes before the next request is dequeued?

## KB Synthesis

Yes to both questions. The evidence is unambiguous.

## The run-to-completion unit is a single FEBE request

[INV-ATOMICITY] (Finding 0042) is explicit: the `xanadu(&task)` call in `bed.c` executes the entire pipeline — request parsing, all state mutations, response sending, and memory cleanup — before returning to `select()`. The event loop then iterates to the next ready file descriptor. There are no threads, no preemptible signal handlers, and no yielding mid-operation.

From `bed.c:103-150` / `bed.c:153-172`: `select()` → iterate FDs → `xanadu(&task)` (blocks until complete) → next FD.

[INV-SEQUENTIAL-DISPATCH] reinforces this: even when multiple FDs are simultaneously ready, the loop services them one at a time. Frontend i's request runs to completion before frontend i+1's begins.

## Multi-span SpecSet operations complete all writes before the next request is dequeued

The COPY / vcopy path is: `docopy` → `vspanset2ispanset` (V-to-I conversion, which calls `vspanset2sporglset` internally) → `insertpm` (POOM write, one crum per contiguous I-span) → `insertspanf(..., DOCISPAN)` (spanfilade write).

[SS-DOCISPAN] (Finding 0047) confirms that `insertspanf` loops over the entire `ispanset` linked list — one `insertnd` call per `typeispan` struct — before returning. All iterations happen within the single `docopy` call. Whether `vspanset2sporglset` produces one sporgl or many (e.g., when the source V-span maps to non-contiguous I-address regions due to prior transclusion, per [ST-LINK-CREATE] Finding 0037), all `insertnd` calls complete inside the same `docopy` invocation, inside the same `xanadu` invocation.

For CREATE-LINK specifically, [ST-CREATE-LINK] (Finding 0012) shows the three-step sequence — create orgl in granf, update document POOM via `docopy`, index endpoints in spanf via `insertendsetsinspanf` — all runs within a single `docreatelink` call, itself within a single `xanadu` invocation.

## One nuance: response ordering does not affect write completeness

[EC-RESPONSE-BEFORE-CHECK] (Finding 0050) notes that for INSERT, DELETEVSPAN, and REARRANGE, `putXXX()` (the response) is sent *before* `doXXX()` executes. So the frontend sees a success response before the internal writes have occurred within that same `xanadu` call. However, all internal writes (granfilade, POOM, spanfilade) still complete before `xanadu` returns and the next `select()` iteration begins. The run-to-completion guarantee holds for all writes; the anomaly is only in when within the handler the response is emitted.

**Summary:** The unit of atomicity is the single `xanadu` dispatch. A multi-span COPY that splits into N sporgls completes all N POOM inserts and all N DOCISPAN spanfilade inserts before the event loop dequeues the next request. [INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH], [SS-DOCISPAN], [ST-CREATE-LINK].

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Is a Single FEBE Request the Run-to-Completion Unit?

**Yes, unambiguously.** The `bed.c` multi-user daemon is a cooperative, single-threaded event loop. There is no threading, no preemption, and no yield points inside any handler.

### The Event Loop

`bed.c:103–149`:

```c
for (;;) {
    /* ... */
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        /* ... */
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                /* ... */
                xanadu(&task);         /* ← one request, runs to completion */
                ntaskorcommand++;
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`select()` identifies which file descriptors have data. For each ready fd, `xanadu()` is called once and must return before the inner `for` loop advances to the next fd.

### `xanadu()` Runs One Request Atomically

`bed.c:153–172`:

```c
int xanadu(typetask *taskptr)
{
  typerequest request;

    logstuff = FALSE;
    if (setjmp(frontendeof)) {
        dobertexit(user);
        player[user].wantsout = TRUE;
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   /* handler runs to completion */
        sendresultoutput(taskptr);         /* response flushed after handler returns */
        /* ... */
    }
    tfree(taskptr);                        /* task memory freed */
    /* ... */
}
```

The sequence is strictly: read request → run handler → send response → free task memory → return. The `select()` loop cannot re-enter `xanadu()` until the previous call returns.

---

## Does a Multi-Span COPY Complete All Writes Before the Next Request?

**Yes.** Every write is inside synchronous C loops with no yield points. Here is the complete trace.

### Step 1 — Dispatch: `fns.c:copy()`

`fns.c:35–47`:

```c
void copy(typetask *taskptr)
{
    if (
       getcopy (taskptr, &docisa, &vsa, &localspecset)
    && docopy (taskptr, &docisa, &vsa, localspecset))
        putcopy (taskptr);
      else
        putrequestfailed (taskptr);
}
```

`putcopy` (sending the response) is called **after** `docopy` returns, so the client ACK is also only sent after all writes complete.

### Step 2 — Core logic: `do1.c:docopy()`

`do1.c:45–65`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* all POOM writes */
    &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) /* all spanfilade writes */
    && asserttreeisok(docorgl)
    );
}
```

The `&&` chain is C short-circuit evaluation: left to right, synchronous. `insertspanf` cannot begin until `insertpm` fully returns.

### Step 3 — V→I translation: `sporgl.c:vspanset2sporglset()`

When the SpecSet contains virtual spans, `specset2ispanset` (called at `do2.c:14–46`) resolves V-addresses to I-addresses via the permutation matrix. The relevant path for a VSpec goes through `sporgl.c:35–65`:

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
            sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
            /* ... populate sporglset ... */
            *sporglsetptr = (typesporglset)sporglset;
            sporglsetptr = (typesporglset *)&sporglset->next;
        }
    }
    return (sporglsetptr);
}
```

Each vspan may map to multiple ispans (one per POOM crum the vspan crosses). All sporgls are built into a linked list in the task-allocated region before `specset2ispanset` returns. This is pure computation — no writes happen here, and no control ever returns to the outer loop.

### Step 4 — POOM writes: `orglinks.c:insertpm()`

`orglinks.c:75–134`:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    /* ... */
    logbertmodified(orglisa, user);
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        /* ... compute crumorigin, crumwidth ... */
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
    }
    return (TRUE);
}
```

For a multi-span input, this `for` loop calls `insertnd()` once per sporgl. Each `insertnd` call modifies the in-core POOM tree synchronously (via `makegappm`, `doinsertnd`, `setwispupwards` in `insertnd.c`). The loop runs to completion — all N POOM nodes are inserted — before `insertpm` returns.

### Step 5 — Spanfilade writes: `spanf1.c:insertspanf()`

`spanf1.c:15–53`:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    /* ... */
    for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
        /* ... extract crumorigin, crumwidth from each sporgl ... */
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    }
    return (TRUE);
}
```

Identical pattern: one `insertnd()` call per sporgl, all synchronous, into the in-core spanfilade. All N spanfilade nodes are inserted before `insertspanf` returns.

### What About the `ntaskorcommand%100` Check in `insertnd.c`?

`insertnd.c:23–28`:

```c
#ifdef UndEfInEd
if((ntaskorcommand%100) == 0){  /* do only 1/n of the time */
    fprintf(stderr,"entering insertnd\n");
    asserttreeisok(fullcrumptr);
}
#endif
```

This is inside `#ifdef UndEfInEd` — it is dead code, disabled at compile time. It is a debug probe only; it never executes.

### When Are Writes Flushed to Disk?

`diskflush()` is called only at `bed.c:105`, inside the `if (n_players < 1)` branch — that is, only when the last user disconnects. `writeenfilades()` is called in signal handlers (`flagquitting`, `crash`). Neither is called from within a request handler. All writes during a COPY are in-core modifications to the enfilade tree; they are durable to disk only at connection teardown or shutdown.

---

## Summary

| Question | Answer | Key evidence |
|---|---|---|
| Is a single FEBE request the unit of run-to-completion? | **Yes** | `bed.c:128`: `xanadu()` called once per ready fd; `bed.c:162–168`: handler→response→tfree are sequential with no re-entry |
| Does a multi-span COPY complete all POOM writes before spanfilade writes begin? | **Yes** | `do1.c:60–62`: `insertpm && insertspanf` — `&&` is sequential; `insertpm` must return before `insertspanf` starts |
| Does `insertpm` complete all per-sporgl POOM nodes before returning? | **Yes** | `orglinks.c:100–132`: synchronous `for` loop over the sporglset, no yield |
| Does `insertspanf` complete all per-sporgl spanfilade nodes before returning? | **Yes** | `spanf1.c:25–52`: identical synchronous `for` loop, no yield |
| Can any other request be dequeued during these loops? | **No** | No threading; `select()` is only called after `xanadu()` returns to `bed.c:103` |

The backend is strictly single-threaded and cooperative. A COPY that `vspanset2sporglset` expands into N sporgls writes all N POOM nodes (via `insertpm`'s loop), then all N spanfilade nodes (via `insertspanf`'s loop), then sends the client ACK, then returns to `xanadu()`, which returns to the outer `select()` loop — only then can the next request be dequeued from any frontend connection.
