## Question 8 [evidence]

> Does the udanax-green back-end serialize entity-allocation events (K.δ-equivalent operations) at a single point — e.g., a global lock around the granfilade query-and-increment — or do multiple protocol commands process concurrently with a finer-grained discipline?

## KB Synthesis

## Allocation Serialization in udanax-green

All entity-allocation events are serialized at the coarsest possible granularity: the **event loop itself**. There is no finer-grained discipline.

### The Mechanism: Run-to-Completion Dispatch

[INV-ATOMICITY] and [INV-SEQUENTIAL-DISPATCH] (both from Finding 0042) establish the definitive answer. The `bed.c` event loop calls `xanadu(&task)` for each ready file descriptor, and that call executes the entire protocol command — including all granfilade tree queries, I-address allocations, POOM insertions, and spanfilade updates — before returning to `select()`. There are no threads, no preemptable signal handlers, and no concurrent execution of any kind. Even when multiple frontends have requests ready simultaneously, the loop iterates sequentially: frontend *i* completes entirely before frontend *i+1* begins.

### The Allocation Function Is Stateless, Not Locked

[SS-ADDRESS-SPACE] Finding 0061 confirms that I-address allocation has no session-local counter. Each INSERT calls `findpreviousisagr` to find the current granfilade maximum, then applies `tumblerincrement(..., 0, 1, isaptr)`. There is no shared atomic counter, no mutex, and no lock around this query-and-increment. It is safe **only because** the event loop guarantees exclusive execution. If two allocations ran concurrently, both would observe the same maximum and produce the same address — a collision. [PRE-CONCURRENT-INSERT] (Finding 0041) explicitly flags this: concurrent unsynchronized insertion into the same enfilade is unsafe, and `father->numberofsons` would suffer lost updates.

### Implication for K.δ-Equivalent Operations

A K.δ allocation event (granfilade query-and-increment) is serialized at the protocol-command boundary, not at a finer internal point. The "lock" is the event loop itself — the entire command is the critical section. [INV-ENFILADE-CONFLUENCE] (Finding 0041) notes that the permanent layer is *logically* confluent under concurrent additions (any serialization order produces identical query results), but the physical tree shape is not. The implementation exploits this by choosing the simplest possible serialization: total, command-level ordering.

**Summary:** udanax-green serializes at a single point — the run-to-completion event loop — with no internal per-operation or per-structure locking. The allocation function is stateless and safe only because parallelism is structurally excluded.

---

## Code Exploration

Now I have everything needed. Let me compile the full answer.

---

## Answer: udanax-green Serializes All Entity Allocation at the Event-Loop Boundary

There is no fine-grained locking, no mutexes, no semaphores, and no threads anywhere in the backend. The entire backend is a **single-process, single-threaded cooperative multiplexer**. Every K.δ-equivalent operation is implicitly serialized because only one protocol command ever runs at a time.

---

### The Concurrency Model: `select()`-Based Run-to-Completion

`bed.c` is the entry point. The main loop (`bed.c:103–149`) uses a single Unix `select()` call to watch all connected frontend sockets:

```c
// bed.c:111
if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
```

When `select()` reports that a frontend has data, the loop picks one ready file descriptor, sets the global `user` variable, and calls `xanadu()`:

```c
// bed.c:118–128
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        user = fdtoplayer[i];
        task.inp = player[user].inp;
        ...
        xanadu(&task);
```

`xanadu()` (`bed.c:153–172`) is fully synchronous — it reads one request, dispatches it, and sends the response before returning:

```c
// bed.c:161–163
} else if (getrequest(taskptr, &request)) {
    (*requestfns[request])(taskptr);
    sendresultoutput(taskptr);
```

The loop does **not** advance to the next ready socket until `xanadu()` returns. There is no threading, no fork, no async I/O for in-progress operations. The multiplexing is purely at the request boundary.

The `mightbeblocked` flag (`bed.c:45`) exists only for SIGINT handling — to distinguish "we're blocked in `select()` waiting for a new connection" from "we're inside a request" — not for concurrency control between requests.

---

### Entity Allocation Path: `findisatoinsertnonmolecule` / `findisatoinsertmolecule`

Every K.δ-equivalent entity allocation (new document, new version, new link, new text span) flows through `granf2.c`:

**`docreatenewdocument`** (`do1.c:234–241`) calls:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
createorglingranf(taskptr, granf, &hint, isaptr);  // do1.c:240
```

**`createorglingranf`** (`granf2.c:111–128`) calls `findisatoinsertgr`, then does `insertseq`.

**`findisatoinsertgr`** (`granf2.c:130–156`) branches on `hintptr->subtype`:
- `ATOM` (text, links) → `findisatoinsertmolecule` (`granf2.c:158–181`)
- Non-ATOM (documents, accounts, nodes) → `findisatoinsertnonmolecule` (`granf2.c:203–242`)

Both functions execute the **query-then-increment** sequence:

```c
// granf2.c:217 — for non-molecule allocations
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// ... then compute new ISA by incrementing lowerbound
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // granf2.c:237
```

```c
// granf2.c:164 — for molecule allocations  
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// ... then increment to find next slot
tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // granf2.c:166
```

These are **pure in-memory tree walks** with no locking primitives. They are safe only because the event loop guarantees no other command is executing concurrently.

---

### Summary

| Question | Answer |
|---|---|
| Is there a global lock? | No explicit lock exists |
| Is there fine-grained locking? | No — no mutex/semaphore anywhere |
| How is safety achieved? | Run-to-completion: `select()` loop dispatches one request at a time (`bed.c:118–128`) |
| Can two clients interleave at the granfilade level? | **No.** `findpreviousisagr` → `tumblerincrement` → `insertseq` runs atomically within one `xanadu()` call |
| Threading model | Single process, single thread — confirmed by absence of `pthread`, `fork`, or any concurrency primitive across the entire backend |

The architecture is equivalent to a **single global lock at the FEBE request boundary**, implemented structurally rather than through any explicit synchronization object. Multiple frontends connect simultaneously (tracked in `player[]` via `players.h`), but they share one backend process and one event loop. No command overlaps with another — not even read operations. This is cooperative multiplexing, not concurrent execution.
