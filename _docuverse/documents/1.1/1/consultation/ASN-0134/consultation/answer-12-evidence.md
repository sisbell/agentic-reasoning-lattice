## Question 12 [evidence]

> Can a RETRIEVEDOCVSPANSET or other Observe ever execute against a POOM that `makegappm` has shifted but into which `insertpm` has not yet inserted the new bottom crum — or does the single-threaded loop make every intermediate `insertnd` state unobservable?

## KB Synthesis

No. The intermediate state is unobservable by construction.

[INV-ATOMICITY] (Finding 0042) establishes the mechanism: the `bed.c` event loop processes each FEBE operation via a blocking `xanadu(&task)` call that runs the entire operation — request parsing, all state mutations, response emission, and memory cleanup — before returning to `select()`. There are no threads, no preemptible signals, and no cooperative yield points within `xanadu`.

[INV-SEQUENTIAL-DISPATCH] (Finding 0042) makes this explicit for the concurrent case: even when multiple frontend file descriptors are ready simultaneously, the loop iterates sequentially. Frontend 2's operation cannot begin until Frontend 1's `xanadu()` has returned.

The consequence for your specific question: the window between `makegappm` shifting existing POOM entries and `insertnd` placing the new bottom crum is entirely intra-`xanadu`. No `select()` call happens in that window, so no other FEBE request — including RETRIEVEDOCVSPANSET — can be dispatched. [ST-INSERT] (Finding 0054) documents that the shift and the crum insertion are both part of the same `insertnd → makegappm` call tree, all executing synchronously within one `xanadu` invocation.

The intermediate POOM state (shifted entries, no new crum) is physically real in memory but temporally invisible: it exists only for the duration of a few C function calls within a single event-loop iteration. Any observation operation can only see pre-INSERT state or post-INSERT state, never the gap between.

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## Observability of the `makegappm` / `doinsertnd` Gap

**The intermediate state is unobservable. The single-threaded event loop makes it physically impossible for any Observe to execute against the POOM between those two calls.**

---

### 1. The event loop is strictly single-threaded and cooperative

`bed.c:main()` [line 103–149] is the sole execution thread. Its structure:

```c
for (;;) {
    inputfds2 = inputfds;                          // [bed.c:110] snapshot ready fds
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {              // [bed.c:118] process each ready fd
            if ((1<<i) & inputfds2) {
                ...
                xanadu(&task);                     // [bed.c:128] one complete request
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`select()` is called only at the top of the outer loop. The `inputfds2` snapshot is fixed once per outer iteration. The inner loop drains each ready fd by calling `xanadu()` **to completion** before moving to the next `i`. There is no preemption, no threading, no re-entrant dispatch.

---

### 2. `xanadu()` runs one entire request atomically

```c
int xanadu(typetask *taskptr)        // [bed.c:153]
{
    typerequest request;
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);  // [bed.c:162] handler runs to completion
        sendresultoutput(taskptr);        // [bed.c:163] flush socket AFTER handler
        ...
    }
    tfree(taskptr);
    ...
}
```

`(*requestfns[request])(taskptr)` at [bed.c:162] is a single synchronous call. `sendresultoutput` is not reached until the handler returns. No other frontend's request is dispatched while this is executing.

---

### 3. The `makegappm` → `doinsertnd` sequence inside `insertnd`

```c
case POOM:                                         // [insertnd.c:53]
    makegappm (taskptr, fullcrumptr, origin, width); // [insertnd.c:54]
    checkspecandstringbefore();                      // [insertnd.c:55]
    setwispupwards(fullcrumptr,0);                   // [insertnd.c:56]
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index); // [insertnd.c:57]
    setwispupwards(fullcrumptr,1);                   // [insertnd.c:58]
    break;
```

`makegappm` [insertnd.c:124–172] displaces the V-offsets of nodes after the insertion point via `insertcutsectionnd` [insertnd.c:152], then updates widths with `setwidnd(father)` [insertnd.c:170] and `setwispupwards` [insertnd.c:171].

`doinsertnd` [insertnd.c:185–197] then inserts (or extends) the bottom crum.

Between these two calls: `checkspecandstringbefore()` is a stub that unconditionally returns 0 [do1.c:125–129] — the debug body is commented out. `setwispupwards(fullcrumptr,0)` is a pure in-memory tree traversal. **Neither makes any blocking I/O call, no `fflush`, no `write`, no `read`, no `select`.**

---

### 4. The "optimistic acknowledgment" in `insert()` does not flush the socket before `doinsertnd`

`fns.c:insert()` [line 84–98] sends the acknowledgment *before* calling `doinsert`:

```c
void insert(typetask *taskptr)       // [fns.c:84]
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);             // [fns.c:91] — writes to output buffer
    if (!doinsert (taskptr, &docisa, &vsa, textset))
        ...
}
```

`putinsert` [putfe.c:243–246] only writes a number into the stdio `FILE*` buffer:

```c
int putinsert(typetask *taskptr)     // [putfe.c:243]
{
    putnumber (taskptr->outp, INSERT);
}
```

The actual socket flush is `fflush(taskptr->outp)` inside `sendresultoutput` [putfe.c:85], which is called at [bed.c:163] — **after the entire handler returns**. Even if the output `FILE*` were unbuffered and the bytes reached the frontend immediately, the backend's single-threaded loop cannot call `select()` again until the current `xanadu()` call returns. The frontend's RETRIEVEDOCVSPANSET would sit in the kernel's receive buffer until the backend re-enters `select()` in the next outer iteration.

---

### 5. Signals cannot inject another player's request mid-handler

The only signals registered [bed.c:70–73]:

| Signal | Handler |
|--------|---------|
| `SIGPIPE` | `crash` — terminates |
| `SIGHUP` | `crash` — terminates |
| `SIGXCPU` | `SIG_IGN` |
| `SIGINT` | `flagquitting` — sets `quitafteruser = TRUE` [bed.c:187], does not dispatch a request |

No signal handler calls `xanadu()`, reads a new request, or observes the POOM.

---

### 6. Call chain for reference

```
bed.c:xanadu()
  → fns.c:insert()
      → do1.c:doinsert()
          → do1.c:docopy()
              → orglinks.c:insertpm()   [iterates over sporglset]
                  → insertnd.c:insertnd()   [POOM branch]
                      → insertnd.c:makegappm()    ← shifts addresses
                      → do1.c:checkspecandstringbefore()  ← no-op stub
                      → setwispupwards(fullcrumptr,0)     ← in-memory only
                      → insertnd.c:doinsertnd()   ← inserts new bottom crum
```

`insertpm` is defined in `orglinks.c` (not `granf2.c`) and calls `insertnd` in a loop over sporglset entries. Each `insertnd` call is itself an atomic unit within the larger atomic `xanadu()` invocation.

---

### Conclusion

Every FEBE request — INSERT, RETRIEVEDOCVSPANSET, REARRANGE, DELETEVSPAN, any Observe — is processed by exactly one call to `xanadu()`, which itself is a sequential, non-preemptible, non-reentrant function running in a single thread. The `select()` call that could discover a new request from any frontend is not reached until the current `xanadu()` returns. Therefore the shifted-but-not-yet-inserted intermediate POOM state that exists between `makegappm` [insertnd.c:54] and `doinsertnd` [insertnd.c:57] is entirely invisible to any other Observe or any other request from any frontend. Every external observer sees only the states that exist at `select()` boundaries — that is, only the states that exist between complete, committed handler executions.
