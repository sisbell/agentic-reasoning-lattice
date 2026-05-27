## Question 7 [evidence]

> How does udanax-green handle a concurrent INSERT (or any concurrent allocation/arrangement transition) on the same document while another INSERT is in progress — does the implementation serialise at the document level, lock the allocator chain, or admit interleaving with a conflict-detection scheme?

## KB Synthesis

## Concurrency Handling in udanax-green

The implementation uses **total daemon-level serialization** — there is no document-level locking, no allocator chain lock, and no conflict-detection scheme. Interleaving is structurally prevented.

### Mechanism: Run-to-Completion Event Loop

The `bed.c` daemon runs a single-threaded `select()` loop. Each iteration calls `xanadu(&task)`, which executes the full operation — request parsing, state mutation (I-address allocation, granfilade insertion, spanfilade update, POOM update), response send, and memory cleanup — before returning to `select()`. There are no threads, no state-modifying signal handlers, and no preemption [INV-ATOMICITY].

Even when multiple frontends have requests simultaneously ready on their file descriptors, the loop iterates over them sequentially. Frontend i's operation completes entirely before frontend i+1's begins [INV-SEQUENTIAL-DISPATCH].

### Why the Allocator is Safe

I-address allocation in `findisatoinsertmolecule` queries the granfilade tree for the current maximum via `findpreviousisagr`, then increments by 1. There is no cached "next available" pointer — allocation is a pure function of current tree state [SS-ADDRESS-SPACE, Finding 0061]. This is safe precisely *because* of sequential dispatch: no other session can modify the tree between the query and the increment.

### What Would Break Without Serialization

[PRE-CONCURRENT-INSERT] makes the hazards explicit: the `adopt(new, RIGHTBRO, ptr)` call in `insertseq` modifies shared sibling pointers; `father->numberofsons` can suffer lost updates under concurrent writes; split and rebalance assume exclusive access. The implementation is not designed to be safe under interleaving — serialization is load-bearing.

### Logical Confluence

[INV-ENFILADE-CONFLUENCE] establishes that the choice of serialization order is a correctness non-issue: any two concurrent additions E1 and E2 produce the same queryable content regardless of execution order (though the physical tree shape differs). This means the single-thread architecture is also *sufficient* — no stronger ordering guarantee is needed for correctness.

### Summary

| Question | Answer |
|----------|--------|
| Document-level lock? | No |
| Allocator chain lock? | No |
| Conflict detection / OCC? | No |
| Serialization unit | Whole daemon (one operation at a time) |
| Mechanism | Single-threaded run-to-completion `select()` loop in `bed.c` |

---

## Code Exploration

I have all the confirmed source evidence I need. Here is my full answer.

---

## Concurrency in udanax-green: How Concurrent INSERTs Are Handled

**Short answer**: udanax-green serializes every operation at the process level via a single-threaded `select()` event loop. No two operations can physically interleave. The BERT table is a secondary, session-lifetime lease mechanism — not a lock in the traditional sense.

---

### 1. The Event Loop: Single-Threaded, Complete Serialization

`bed.c` is the authoritative source. The entire server runs as one process, one thread:

```c
/* bed.c:103-128 */
for (;;) {
    ...
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {   /* line 111 */
        ...
    } else {
        for (i = 0; i <= nfds; i++) {                        /* line 118 */
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];                         /* line 120 */
                task.inp  = player[user].inp;                 /* line 121 */
                task.outp = player[user].outp;                /* line 122 */
                task.account = player[user].account;          /* line 123 */
                xanadu(&task);                                /* line 128 */
```

`select()` (line 111) tells the loop which client FDs have data ready. For each ready FD, `xanadu(&task)` (line 128) is called **synchronously and runs to completion** before the loop advances to the next FD. This is classic select-multiplexed single-threading. There are no pthreads, no `fork()`, no mutexes, no atomics, no semaphores anywhere in the backend.

```c
/* bed.c:153-168 */
int xanadu(typetask *taskptr)
{
  typerequest request;
  ...
  } else if (getrequest(taskptr, &request)) {
      (*requestfns[request])(taskptr);   /* line 162 — one handler, runs to finish */
      sendresultoutput(taskptr);
  }
  tfree(taskptr);
}
```

**Implication**: Two clients issuing INSERT simultaneously are serialized by the OS's socket/select machinery. Client B's request bytes sit in a kernel buffer while Client A's `xanadu()` runs. B gets service only after A's call returns. There is no interleaving at the instruction level, no critical section, and no race condition possible.

---

### 2. The INSERT Execution Path

```
fns.c: insert()
  → do1.c:87  doinsert(taskptr, docisaptr, vsaptr, textset)
      → do1.c:118  inserttextingranf(...)  ← allocates content in global granf
      → do1.c:119  docopy(taskptr, docisaptr, vsaptr, ispanset)
          → do1.c:55  findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
              → bert.c:264  doopen(..., WRITEBERT, BERTMODECOPYIF, connection)
                  → bert.c:279  checkforopen(tp, WRITEBERT, connection)
          → do1.c:60  insertpm(...)   ← modifies the POOM tree
          → do1.c:62  insertspanf(...)  ← updates global spanf
```

`granf` and `spanf` are global allocator structures, accessed without any synchronization — which is safe precisely because the event loop guarantees single-threaded access.

---

### 3. The BERT Table: Session-Lifetime Document Leases

The BERT table (`bert.c`) is a hash table of open-document records per connection:

```c
/* bert.c:13-19 */
typedef struct {
    int connection;       /* which client */
    tumbler documentid;   /* which document */
    char created, modified;
    int type;             /* READBERT or WRITEBERT */
    int count;            /* reference count */
} bertentry;

static conscell *berttable[NUMBEROFBERTTABLE];  /* line 29 */
```

The table is consulted via `checkforopen()` (line 52). The access-control matrix is documented inline:

```
/* bert.c:43-50 */
    Open state -->
    type          Not Open      Open READ       Open WRITE
      |         !owned|owned  conn==|conn!=   conn==|conn!=
      v         ------+------  -----+-------  ------+------
    READ           0  |  0    READ  |   0    WRITE  | -1
    WRITE         -1  |  0     -1   |  -1    WRITE  | -1
```

When `checkforopen()` finds a document held as WRITEBERT by a **different** connection, it sets `foundnonread = TRUE` (line 75) and returns `-1`:

```c
/* bert.c:63-85 */
for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) {
        if (connection == bert->connection) {        /* line 66 — same client */
            ...return READBERT or WRITEBERT...
        } else {                                     /* line 73 — different client */
            if (bert->type != READBERT) {
                foundnonread = TRUE;                 /* line 75 */
            }
        }
    }
}
if (!foundnonread && ...) return 0;
else                       return -1;               /* line 84 */
```

`doopen()` acts on that `-1`:

```c
/* bert.c:288-298 */
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);  /* line 290 */
        addtoopen(newtp, connection, TRUE, type);                    /* line 291 */
    } else if (type != WRITEBERT && openState != WRITEBERT) {
        incrementopen(tp, connection);                               /* line 293 */
        ...
    } else {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);  /* line 296 */
        addtoopen(newtp, connection, TRUE, type);
    }
    return 1;
```

Conflict → new version, not a retry or wait. The arriving operation proceeds against a fresh version allocated from the same account's tumbler namespace.

---

### 4. When Does BERT Conflict Actually Fire?

Because `xanadu()` processes one request to completion before returning, BERT entries added by Client A during its request are normally removed (via `doclose` → `removefromopen`, line 154) **within the same request**. The BERT table conflict path (`-1` → `docreatenewversion`) therefore fires in two real scenarios:

1. **Abnormal disconnect**: Client A opened a document (BERT entry added) but the connection died before `doclose` was called. `exitbert` (line 195, called from `dobertexit` at line 339) cleans up on disconnect, but if that cleanup is missed, the BERT entry survives. The next client then hits the conflict path.

2. **Multi-operation sessions**: If the protocol supports a "hold document open across multiple request/response cycles" session model — which the `count` reference field (line 18) and `incrementopen` (line 112) suggest it does — then Client A can hold a WRITEBERT lease for the duration of a session. Client B arriving during that window gets a new version.

---

### 5. Summary

| Question | Answer |
|----------|--------|
| Serialized at document level? | **Yes — at the process level.** The event loop (`bed.c:128`) enforces strict request-by-request sequencing. No two operations run concurrently in any sense. |
| Lock the allocator chain? | **No explicit locks.** `granf`/`spanf` are global, accessed without synchronization. Single-threading makes this safe. |
| Conflict-detection with interleaving? | **No interleaving exists** to conflict-detect. The BERT table handles session-duration leases and abnormal-disconnect cleanup, not mid-request races. |
| What happens if two clients INSERT the same document? | They are serialized. The first completes entirely; the second then runs. If the first left a WRITEBERT BERT entry open (abnormal case), the second instead creates a new document version (`docreatenewversion`, `bert.c:290`) and operates on that. |

The concurrency model is identical to the classic UNIX `inetd`-style single-process server: simplicity is the lock.
