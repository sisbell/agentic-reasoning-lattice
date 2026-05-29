## Question 1 [evidence]

> Does udanax-green commit baptisms through a single serialized path (one persistent-store writer), so that no two baptismal commits can occur on divergent branches from the same state?

## KB Synthesis

**Yes — udanax-green commits baptisms through a single fully serialized path, making divergent baptismal branches structurally impossible.**

## The Serialization Guarantee

The backend daemon's `bed.c` event loop dispatches operations via run-to-completion scheduling: a single `xanadu(&task)` call executes an entire operation — request parsing, all state mutations, response sending, memory cleanup — before returning to `select()`. There are no threads, no preempting signal handlers, and no coroutines [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]. Even when multiple frontend file descriptors are simultaneously ready, the loop iterates over them sequentially; request `i` completes entirely before request `i+1` begins.

## How Baptism Works

A baptism (I-address allocation) is performed by `findisatoinsertmolecule` in `granf2.c`, which:
1. Calls `findpreviousisagr` to traverse the single shared granfilade tree and return the current maximum I-address
2. Calls `tumblerincrement` to produce `max + 1` as the next allocation

There is **no session-local counter** and no cached "next available" pointer — allocation is a pure function of the single shared granfilade state at the moment of execution [SS-ADDRESS-ALLOC, Finding 0061]. Two back-to-back baptisms will always produce strictly ordered, non-overlapping I-addresses [INV-MONOTONIC].

## Why Divergence Is Impossible

A divergent-branch scenario requires two writes to separate histories forked from a common state — i.e., concurrent execution. The architecture rules this out at every level:

- **Single in-memory state**: all enfilades (granf, spanf, POOMs) share a single in-process memory image [SS-CACHE-MECHANISM, SS-UNIFIED-STORAGE]
- **Single-threaded dispatch**: operations are strictly sequenced; the event loop cannot interleave two baptisms [INV-SEQUENTIAL-DISPATCH]
- **Stateless allocation**: each baptism reads the current tree maximum, so a second baptism sees the first's I-address already committed and allocates above it [Finding 0061]
- **Append-only granfilade**: once an I-address is committed, it is never freed or reallocated, so there is no "slot" that could be filled by two competing writers [INV-NO-IADDR-REUSE, FC-GRANF-ON-DELETE]

The only multi-session concern is CONFLICT_COPY [EC-CONFLICT-COPY-NO-MERGE], but that operation shares existing I-addresses rather than baptizing new ones — no new allocation occurs.

## Durability Caveat

While logical serialization is total, disk durability is session-scoped: baptisms are in-memory until `writeenfilades()` at clean exit. A crash may lose recent baptisms, but a crashed-and-restarted system resumes from a consistent (if stale) on-disk state, with the allocation counter derived from whatever the granfilade contains [INV-DURABILITY-BOUNDARY, EC-CRASH-MID-WRITE]. This does not create divergent branches — it discards uncommitted baptisms uniformly.

**Bottom line**: The run-to-completion single-threaded event loop combined with a stateless query-and-increment allocator over a single shared granfilade ensures that baptisms form a strict linear sequence. No two baptisms can fork from the same state.

---

## Code Exploration

Now I have enough to write a complete, precise answer. Let me trace the full serialization path:

---

## Does udanax-green commit baptisms through a single serialized path?

**Yes — definitively.** But the guarantee is structural rather than explicit: it derives from the single-process, non-threaded, cooperative scheduling of the event loop. There is no lock, mutex, or semaphore anywhere in the baptism path.

---

### What "baptism" means in this codebase

Baptism is tumbler-address assignment to a new object — document, node, text atom, or link. It happens in two functions in `granf2.c`:

- `findisatoinsertnonmolecule()` [granf2.c:203-242] — for documents, nodes, accounts
- `findisatoinsertmolecule()` [granf2.c:158-181] — for text and link content

Both work the same way: call `findpreviousisagr()` to find the highest existing tumbler under the hint, then compute the next one by increment. This is a **read-then-write on the in-memory enfilade tree** with no locking.

```c
// granf2.c:217
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// ... compute next address ...
// granf2.c:237 (first child case)
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
// granf2.c:239-240 (subsequent child case)
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, ..., 1, isaptr);
```

### The three backend entry points

The `NOTES` [backend/NOTES:5-8] describes three backends:

| File | Mode |
|------|------|
| `be.c` | stdio backend — used by the test harness |
| `xumain.c` | interactive standalone |
| `bed.c` | multi-user daemon (socket) |

All three are **single-process, single-thread**. None use `fork()`, `pthread_create()`, or any OS concurrency primitive.

### The serialization mechanism in `bed.c`

The multi-user daemon event loop [bed.c:103-149]:

```c
for (;;) {
    if (n_players < 1) {
        diskflush();   // bed.c:105 — only writes when nobody connected
        ...
    }
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];        // bed.c:120
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                xanadu(&task);               // bed.c:128 — processes one full request
                ...
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`select()` returns a set of ready file descriptors. The inner loop picks each one and calls `xanadu(&task)` **synchronously to completion before the next `select()` iteration**. There is no preemption.

`xanadu()` [bed.c:153-172] dispatches to the handler, sends the result, and frees task memory:

```c
int xanadu(typetask *taskptr) {
    if (setjmp(frontendeof)) { ... }
    else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // bed.c:162 — full handler runs here
        sendresultoutput(taskptr);
    }
    tfree(taskptr);                        // bed.c:168
}
```

While `xanadu()` executes, no other request can begin. The `select()` loop cannot advance. A second client waiting on its file descriptor will sit until `xanadu()` returns.

### The baptism call chain

```
fns.c handler (e.g., createnode_or_account)
  → do1.c:docreatenewdocument() or docreatenode_or_account()
      → granf2.c:createorglgr()
          → granf2.c:findisatoinsertgr()
              → granf2.c:findisatoinsertnonmolecule()  ← BAPTISM HERE
                  → granf1.c:findpreviousisagr()         (reads current max tumbler)
                  → tumble.c:tumblerincrement()           (computes next address)
              → granf2.c:insertseq()                      (writes to in-memory tree)
```

Every step is synchronous, in-process, with no yield points. The baptism is atomic with respect to other requests because no other request can interleave with it.

### The persistent-store writer

The disk is a **lazily updated checkpoint** — not a per-request commit log.

`actuallywriteloaf()` [disk.c:300-338] is the single write path:

```c
void actuallywriteloaf(typeuberrawdiskloaf *loafptr, INT diskblocknumber)
{
    if (lseek(enffiledes, (long)diskblocknumber*NUMBYTESINLOAF, 0) < 0)
        gerror("lseek failed\n");
    if (write(enffiledes, (char*)loafptr, sizeof(*loafptr)) <= 0)
        qerror("write\n");
}
```

`enffiledes` [disk.c:32] is a single file descriptor, opened once in `initenffile()` [disk.c:340-383]. There is only one writer, one file, one process.

Writes are triggered by:
- `diskflush()` [corediskout.c:58-64] → called at `bed.c:105` **only when `n_players < 1`** (all users disconnected)
- `writeenfilades()` [corediskout.c:68-88] → called from `diskflush()`, `flagquitting()`, and `diskexit()`
- `uniqueoutloaf()` [corediskout.c:511-548] → called during subtree write on individual modified nodes

In the test harness backend (`be.c`), there is exactly one frontend connection and `diskexit()` writes on quit.

### Answer to the specific question

**No two baptismal commits can occur on divergent branches from the same state**, because:

1. **Single process, no threads.** There is only one process, no concurrent execution. The `select()` loop [bed.c:103-149] picks one ready fd per iteration, calls `xanadu()` synchronously, returns, and only then can another fd be served.

2. **Baptism is a read-modify-write on shared mutable in-memory state.** The granfilade is one tree in memory. `findpreviousisagr()` reads the current maximum tumbler; `tumblerincrement()` and `insertseq()` write the new address into that same tree. The second client to be baptized always sees the result of the first — there is no snapshot, no isolated copy.

3. **One persistent-store writer.** `enffiledes` is one file descriptor. `actuallywriteloaf()` is called synchronously, without concurrent access possible (single-process, no threads).

4. **No MVCC, no WAL, no transaction isolation.** The disk is not written per-request; it is written lazily at flush time. Within a session, the in-memory enfilade is the authoritative state, and it is mutated sequentially by each request.

### The one structural caveat

The guarantee is **implicit**, not enforced by locks. If someone refactored the event loop to use threads or forked child processes, the baptism path would have a race condition — `findpreviousisagr` + `tumblerincrement` + `insertseq` is not atomic under preemption. The design depends entirely on cooperative scheduling remaining intact.

---

**Summary:** Yes, udanax-green commits baptisms through a single serialized path — not by explicit locking, but because the entire system is one process, one thread, one file descriptor, and one event loop that processes requests one at a time to completion. Two baptisms cannot diverge from the same state because the second baptism always runs after the first has already mutated the shared in-memory granfilade.
