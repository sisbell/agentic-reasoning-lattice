## Question 8 [evidence]

> Does the backend serialize request processing such that no other operation can observe an intermediate state of docreatenewversion — for example, the new version document existing in the granfilade before its POOM has been populated?

## KB Synthesis

Yes, the backend fully serializes request processing, making it impossible for any other operation to observe an intermediate state of `docreatenewversion`.

**The mechanism: run-to-completion scheduling**

[INV-SEQUENTIAL-DISPATCH] and [INV-ATOMICITY] (both from Finding 0042) establish this at the architectural level. The `bed.c` event loop calls `xanadu(&task)` for each request, which executes the entire operation — request parsing, all state mutations, response sending, and memory cleanup — before returning to `select()`. There are no threads, no state-modifying signal handlers, and no preemption. Even when multiple frontends have requests simultaneously ready on their file descriptors, the loop iterates strictly sequentially: frontend i's request runs to completion before frontend i+1 begins.

**Applied to `docreatenewversion` specifically**

[INV-ATOMICITY] (Finding 0032) directly addresses your question:

> CREATENEWVERSION is atomic — the new document and its content appear together. There is no window where the version document exists without its content. This follows from the implementation: `docreatenewversion` creates the orgl, retrieves the source vspanset, and copies content in a single request handler invocation before returning the new address.

The three internal steps — `createorglingranf` (allocate new document address), `doretrievedocvspanfoo` (retrieve source vspan), `docopyinternal` (populate POOM) — all occur within one `xanadu()` invocation. No other request can interleave with them.

**Contrast with two-step CREATEDOCUMENT + COPY**

[INV-ATOMICITY] notes that this atomicity distinguishes `CREATENEWVERSION` from the alternative two-step sequence. With CREATEDOCUMENT followed by a separate COPY request, the intermediate state (empty document exists, POOM not yet populated) is observable by any other session between the two requests, since each request is a separate `xanadu()` invocation.

**Summary**

The single-threaded, run-to-completion event loop is the only concurrency mechanism — there are no threads that could read shared enfilade state mid-operation. The intermediate state you describe (version orgl allocated, POOM not yet populated) exists transiently in RAM during the handler, but no other `xanadu()` call can execute until that handler returns. The new version is effectively atomic from the perspective of any concurrent session.

---

## Code Exploration

I have all I need. Here is the complete answer.

---

## Serialization of `docreatenewversion` — Code Analysis

### Short Answer

**Yes.** The backend implicitly serializes all request processing through its single-threaded, run-to-completion event loop. No other operation can observe any intermediate state of `docreatenewversion` — including the window between granfilade registration and POOM population — because no other request dispatch can occur while one is in flight.

---

### The Event Loop Guarantee

**`bed.c:103–149` — the outer main loop:**

```c
for (;;) {
    ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                ...
                xanadu(&task);       // [bed.c:128]
                ...
            }
        }
    }
    leave(player, &n_players);
    new_players(...);
}
```

`select()` [bed.c:111] returns a snapshot of all ready file descriptors. The inner `for` loop then processes each one by calling `xanadu()` sequentially. `xanadu()` **must return** before the next ready descriptor is served.

**`bed.c:153–172` — `xanadu()`:**

```c
int xanadu(typetask *taskptr)
{
  typerequest request;
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // [bed.c:162]
        sendresultoutput(taskptr);
        ...
    }
    tfree(taskptr);
    ...
}
```

One request is read. The handler is dispatched via function pointer and runs to completion. `sendresultoutput` is called only after the handler returns. No threads, no cooperative yield, no `select()` nested inside a handler.

---

### `docreatenewversion` Step-by-Step

**`do1.c:260–299`:**

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {  // [do1.c:277] — allocates new ISA
        return (FALSE);
    }

    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {      // [do1.c:281] — reads original vspan
        return FALSE;
    }

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);
    vspec.vspanset = &vspan;

    addtoopen(newisaptr, user, TRUE, WRITEBERT);                  // [do1.c:292] — registers in bert table
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);    // [do1.c:293] — populates new POOM
    logbertmodified(newisaptr, user);                             // [do1.c:295]
    doclose(taskptr, newisaptr, user);                            // [do1.c:296]

    return (TRUE);
}
```

All six steps execute within a single `xanadu()` invocation. There is no I/O, no blocking, and no yield between them.

**`createorglingranf` is purely in-memory** [granf1.c:50–55]: it delegates to `createorglgr()`, which operates on the in-memory granfilade tree.

**`addtoopen` and `logbertmodified` are hash table operations** [bert.c:128–151, 97–108]: they insert or update a `bertentry` in the in-memory `berttable[NUMBEROFBERTTABLE]` array. No I/O.

**Disk I/O is deferred**: `diskflush()` [bed.c:105] is only called when `n_players < 1` (no connected clients). It is never called during active request handling.

---

### The One Caveat: Orphaned Granfilade Entries on Failure

If `doretrievedocvspanfoo` returns FALSE at [do1.c:281–283], the function returns early. The granfilade entry created at line 277 is not cleaned up. This leaves an empty document ISA allocated but never populated.

This is **not a concurrency/observability issue** — no other request can run during this window. It is a **cleanup/leak issue**: the orphaned entry exists in the granfilade with an empty POOM. Because `fns.c:createnewversion` calls `putrequestfailed` when `docreatenewversion` returns FALSE, no client ever receives the orphaned ISA. No client can reference it through normal operations.

The same failure path applies if `createorglingranf` itself fails (nothing to clean up), or if `docopyinternal` fails silently (it returns a bool that is not checked at [do1.c:293]).

---

### Summary

The backend provides **implicit serialization** through architecture rather than explicit locking:

| Property | Evidence |
|---|---|
| Single-threaded | One process, no threads anywhere in the codebase |
| Run-to-completion dispatch | `(*requestfns[request])(taskptr)` at `bed.c:162` — handler must return before event loop iterates |
| No in-handler yields | No `select()`, `read()`, or blocking I/O inside any handler or its callees |
| Deferred disk I/O | `diskflush()` only runs at `bed.c:105`, with zero connected clients |
| `docreatenewversion` is one handler | Called from `createnewversion()` via `requestfns[CREATENEWVERSION]` — one atomic event loop tick |

The intermediate state — *new ISA registered in granfilade, POOM not yet populated* — exists transiently between [do1.c:277] and [do1.c:293], but no other client's request can be dispatched during that interval. The serialization guarantee is architectural.
