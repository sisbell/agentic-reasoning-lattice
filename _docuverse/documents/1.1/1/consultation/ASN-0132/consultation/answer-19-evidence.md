## Question 19 [evidence]

> Since count and enumeration are separate FEBE operations and atomicity is per-operation only, can another session's MAKELINK or edit land between a count call and a subsequent enumeration call, breaking count = length-of-enumeration, or is there any snapshot mechanism tying the two results together?

## KB Synthesis

No snapshot mechanism exists. The count and enumeration are two independent FEBE round-trips against shared mutable state, and another session's write can land between them.

## Why each call is individually atomic but not cross-call consistent

[INV-ATOMICITY] establishes that the backend event loop processes each FEBE operation to completion before returning to `select()` — the `xanadu(&task)` call is run-to-completion. [INV-SEQUENTIAL-DISPATCH] strengthens this: even when multiple frontends have requests pending, they are drained one-at-a-time in fd-iteration order. So within a single count call or a single enumeration call, no interleaving occurs.

But "per-operation atomicity" is the entire guarantee. There is no transaction, no snapshot, no read-lock held across calls.

## The count operation itself is not optimized

[ST-FIND-LINKS] (Finding 0035) makes this concrete: FINDNUMOFLINKSFROMTOTHREE is a trivial wrapper that calls `findlinksfromtothreesp()` to materialize the full result list, then walks it counting nodes. It returns an integer, not a snapshot. The result set is discarded after counting; no state persists.

## Links are shared global state

[ST-LINK-GLOBAL-VISIBILITY] (Finding 0022): links created by any session are immediately visible to all other sessions without any synchronization step. [SS-SESSION-STATE] (Finding 0022) confirms that the enfilades — including the spanfilade that backs link search — are globally shared. A MAKELINK in session B updates the spanfilade that session A's subsequent FINDLINKSFROMTOTHREE will query.

## Enumeration is explicitly stateless and re-executes from scratch

[SS-PAGINATE-LINKS] (Finding 0035) is the clearest statement of the design: FINDNEXTNLINKSFROMTOTHREE "re-executes the full `findlinksfromtothreesp()` search" on every call. There is no server-side cursor. The cursor is a link ISA the caller passes back; the server searches fresh each time and scans forward to that ISA. [EC-CURSOR-INVALIDATION] documents the consequence: if the cursor link disappears from results between paginated calls, the cursor walk falls off the end and returns an empty set — not an error, just silent inconsistency.

## Concrete race scenarios

| Interleaving | Observable effect |
|---|---|
| MAKELINK lands between count and FINDLINKSFROMTOTHREE | Enumeration returns more items than count |
| DELETE makes a link undiscoverable between count and enumeration | Enumeration returns fewer items than count |
| MAKELINK lands between two FINDNEXTNLINKSFROMTOTHREE pages | New link appears mid-page or is missed depending on its ISA position in the result ordering |
| Cursor link deleted between pages | [EC-CURSOR-INVALIDATION]: returns `[]`, count=0 |

## Summary

`count = length(enumeration)` holds only if both operations execute atomically as a single unit, which this system does not support. The only consistency scope is the single FEBE request. Any application needing a consistent count-then-enumerate must account for the race — the system provides no mechanism to prevent it.

---

## Code Exploration

---

## Answer: Count/Enumeration Consistency Across FEBE Operations

### Short Answer

**Yes, another session's MAKELINK or edit can land between a COUNT call and a subsequent enumeration call.** There is no snapshot mechanism tying them together. However, the as-shipped backends **disable** COUNT and PAGINATE in all multi-session configurations, making the race unreachable through normal FEBE usage.

---

### The Event Loop: Where the Window Exists

`bed.c` runs a single-threaded cooperative event loop. Each call to `xanadu()` runs **one request to completion** — no preemption, no threads. The structure is:

```c
// bed.c:118-142
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        user = fdtoplayer[i];
        ...
        xanadu(&task);   // one request, runs to completion
    }
}
```

`xanadu()` calls `getrequest()`, the handler, `sendresultoutput()`, and then `tfree(taskptr)` [bed.c:153-168]. All within one non-preemptable call. There is no interleaving **within** a request.

But a COUNT call from Session A and a subsequent FINDLINKS call from Session A are **two separate requests**. Between them, the outer `for(;;)` loop at `bed.c:103` calls `select()` again and can service Session B's fd. Session B's MAKELINK or INSERT runs to completion — mutating the global `spanf` — before Session A's next request is dispatched. That is the window.

---

### Why There Is No Snapshot

Both count and enumeration invoke `findlinksfromtothreesp` independently, re-reading the spanfilade from scratch each time.

**Count path** (`spanf1.c:105-115`):
```c
bool findnumoflinksfromtothreesp(...) {
  typelinkset linkset;
  INT n;
  if (!findlinksfromtothreesp (taskptr, spanfptr, fromvspecset, tovspecset, threevspecset, orglrange, &linkset))
    return(FALSE);
  for (n = 0; linkset; linkset = linkset->next, ++n);
  *numptr = n;
  return (TRUE);
}
```

`findlinksfromtothreesp` reads the spanfilade, materializes a linked list into **task-local** heap (`taskalloc`/`talloc`), and the result is immediately counted and discarded. After `sendresultoutput()` returns, `tfree(taskptr)` at `bed.c:168` frees every byte of that list [task.c:75-88]. No cursor, no saved state, nothing persists to the next request.

**Enumeration path** (`spanf1.c:56-103`):
```c
bool findlinksfromtothreesp(...) {
  ...
  sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
  ...
  intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
  return (TRUE);
}
```

Same function, same fresh traversal of the same global `spanf`. If Session B added a link between the two calls, `fromlinkset` now contains it.

**Pagination path** (`spanf1.c:117-149`):
```c
bool findnextnlinksfromtothreesp(...) {
  ...
  if (!findlinksfromtothreesp (taskptr, spanf, ..., &linkset))
    return (FALSE);
  if (iszerotumbler (lastlinkisaptr)) {
    *nextlinksetptr = linkset;
  } else {
    for (; linkset; linkset = linkset->next) {
      if (tumblereq (&linkset->address, lastlinkisaptr)) {  // seeks by tumbler address
        *nextlinksetptr = linkset->next;
        break;
      }
    }
  }
```

The pagination cursor is a client-supplied tumbler address (`lastlinkisaptr`) matched by `tumblereq`. It is not a stable server-side position. If Session B inserted a link with a tumbler address that sorts before `lastlinkisaptr`, the new link will appear in a subsequent page that wasn't counted — the cursor walks forward by identity, not by a position frozen at count time.

---

### No Lock on the Spanfilade

The spanfilade is a single global mutable structure:

```c
// xanadu.h:16
extern typespanf spanf;
```

BERT (`bert.c`) provides per-document open/lock tracking (READ vs WRITE), but the link-find operations explicitly **bypass it**. At `spanf1.c:71-75`:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset (taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
```

`NOBERTREQUIRED` means no access check and no lock acquisition [bert.c:59-61: `if (type == NOBERTREQUIRED) { return 1; }`]. BERT guards individual document writes; it provides no query isolation across operations on `spanf`.

---

### The Deployed Safeguard: COUNT and PAGINATE Are Disabled in All Multi-Session Configurations

`init.c:71-76`:
```c
if (safe) {
    requestfns[SOURCEUNIXCOMMAND] = nullfun;
    requestfns[NAVIGATEONHT] = nullfun;
    requestfns[FINDNUMOFLINKSFROMTOTHREE] = nullfun;    // COUNT disabled
    requestfns[FINDNEXTNLINKSFROMTOTHREE] = nullfun;    // PAGINATE disabled
}
```

Both `be.c` (single-connection backend used by the test harness) and `bed.c` (multi-user daemon) call `init(1)` — safe mode — at `be.c:83` and `bed.c:92` respectively. Calling `FINDNUMOFLINKSFROMTOTHREE` or `FINDNEXTNLINKSFROMTOTHREE` against either backend returns `putrequestfailed` immediately.

`xumain.c` calls `init(0)` at line 40, leaving COUNT and PAGINATE live — but `xumain` is a single-user interactive shell with no socket listener. Session B cannot exist in that configuration.

Additionally, `init.c:63` shows `FINDLINKSFROMTOTHREE` is never in the `safe`-disabled set. The full enumeration is available in all configurations; only the count and paginator are gated off.

---

### Summary Table

| Operation | be.c (test harness) | bed.c (daemon) | xumain.c (standalone) |
|---|---|---|---|
| FINDLINKSFROMTOTHREE (enumerate all) | enabled | enabled | enabled |
| FINDNUMOFLINKSFROMTOTHREE (count) | **disabled** | **disabled** | enabled |
| FINDNEXTNLINKSFROMTOTHREE (paginate) | **disabled** | **disabled** | enabled |
| Multiple sessions possible? | no (1 connection) | yes | no (1 user) |

**The race is real in the code**, but the system prevents it from being triggered: the only deployment where COUNT is live (`xumain`) cannot have a second session, and the only deployment where a second session exists (`bed.c`) has COUNT disabled.

If someone were to patch `bed.c:92` to call `init(0)`, Session B's MAKELINK could land between Session A's COUNT and enumeration with no protection — the count would be stale, the enumeration would reflect the new state, and `count != length-of-enumeration` would hold.
