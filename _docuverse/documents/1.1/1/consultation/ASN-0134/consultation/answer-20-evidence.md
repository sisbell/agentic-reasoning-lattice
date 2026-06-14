## Question 20 [evidence]

> Is ordering globally serialized by the one event loop with no per-document independence, or could the design support per-home-document independent commit — and does any code path assume a single total order over operations touching distinct POOMs?

## KB Synthesis

## Global Serialization in udanax-green

The answer is unambiguous: **the implementation imposes a single total order over all operations, and multiple code paths structurally assume this**.

---

### The Event Loop Is the Single Serialization Point

[INV-SEQUENTIAL-DISPATCH] / [INV-ATOMICITY] (Finding 0042): `bed.c` processes FEBE requests via a run-to-completion event loop. `select()` may return multiple ready file descriptors simultaneously, but the loop iterates through them one-by-one, calling `xanadu(&task)` to completion before advancing. There are no threads, no reentrant handlers, and no preemption. Multi-step operations — INSERT involves I-address allocation, granfilade insertion, DOCISPAN indexing, and POOM update — execute as a single uninterruptible unit. The total order over all operations touching any POOM is the file-descriptor iteration order of `bed.c`.

---

### Three Structural Reasons Per-Document Independence Is Not Supported

**1. Shared B-tree ancestor nodes**

[PRE-CONCURRENT-INSERT] (Finding 0041): Concurrent unsynchronized insertion into the same enfilade is unsafe. `adopt(new, RIGHTBRO, ptr)` modifies shared pointers, `father->numberofsons` is subject to lost updates, and `splitcrumupwards` / `setwispupwards` assume exclusive access. Critically, operations on *different* document subtrees still share ancestors: when a height-1 fullcrum splits, [SS-ENFILADE-TREE] (Finding 0058/0060) shows `levelpush` modifies the shared root. Two INSERTs into different documents race on shared upper tree nodes whenever splits propagate.

**2. Shared cache and block allocator**

[SS-UNIFIED-STORAGE] / [SS-CACHE-MECHANISM] (Finding 0059): All enfilades — granfilade, spanfilade, and all document POOMs — live in a single `enf.enf` file with a single block allocator (`ealloc`). The grim reaper cache is a single global circular list across all enfilade types. [INT-CROSS-ENFILADE-EVICTION] confirms memory pressure from one document's operations can evict modified crums from another document's POOM. This is a global resource, not per-document.

**3. Cross-enfilade operations require global coordination**

[ST-CREATE-LINK] (Finding 0012): CREATELINK writes to *both* granf (new link orgl + document modification) and spanf (endpoint I-address index) in a single operation. [INV-DUAL-ENFILADE-CONSISTENCY] requires these two writes to be atomic — no observation can occur between them. Per-document commit granularity cannot satisfy this, since the two enfilades are distinct global structures.

---

### The Confluence Property Does Not Rescue Per-Document Ordering

[INV-ENFILADE-CONFLUENCE] (Finding 0041): The permanent layer is *logically* confluent — the queryable content is independent of the order in which entries are added. This means IF per-document parallelism were safe at the physical level, the logical results would commute. But the finding is explicit: confluence holds at the abstraction boundary (query results) but **NOT at the physical level**. Tree shapes, sibling ordering, and split points all depend on insertion order, and shared ancestor nodes would conflict.

---

### I-Address Allocation Is Bounded Per-Document But Queries the Global Tree

[SS-ADDRESS-ALLOC] / [INV-MONOTONIC] (Findings 0061, 0065, 0077): Text I-address allocation is bounded to a document's address namespace via the `upperbound` parameter in `findisatoinsertmolecule`. This is not a single global counter — [SS-ADDRESS-SPACE] (Finding 0077) confirms allocation is a family of independent functions partitioned by tumbler range. However, all allocations still call `findpreviousisagr` against the **same shared granfilade tree**. Two concurrent allocations in different document namespaces would still race on B-tree traversal and the shared in-memory representation. The namespace partitioning provides logical isolation, not physical concurrency safety.

---

### Summary

The design assumes a single total order over all operations:

| Property | Where it holds | Why per-document ordering fails |
|----------|---------------|-------------------------------|
| Run-to-completion dispatch | `bed.c` event loop [INV-SEQUENTIAL-DISPATCH] | Single queue for all sessions |
| B-tree split safety | `splitcrumupwards` [SS-ENFILADE-TREE] | Shared root and ancestor nodes |
| Cache coherence | Grim reaper [SS-CACHE-MECHANISM] | Global eviction pool, no POOM isolation |
| Cross-enfilade atomicity | CREATELINK [ST-CREATE-LINK] | granf + spanf must update together |
| Logical confluence | [INV-ENFILADE-CONFLUENCE] | Holds logically, not physically |

The event loop serialization is not an incidental implementation choice that could be swapped for per-document locking — it is load-bearing for every multi-step operation in the system.

---

## Code Exploration

I have enough to write a thorough, cited answer.

---

## Serialization in udanax-green: Event Loop, Global Commit, and Total Order

### 1. The Event Loop Is a Single-Threaded Total Serializer

`bed.c` implements a classic multiplexed single-process event loop. The outer `select()` call wakes on any ready file descriptor, then the inner `for` iterates ready descriptors and calls `xanadu()` **synchronously** for each one before moving to the next:

```c
// bed.c:103-141
for (;;) {
    inputfds2 = inputfds;                               // line 110
    if (select(nfds+1, &inputfds2, 0, 0, &timeout)...) // line 111
        ...
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];                       // line 120 — global mutable
            task.inp = player[user].inp;
            task.outp = player[user].outp;
            task.account = player[user].account;
            xanadu(&task);                              // line 128 — blocks until done
            ntaskorcommand++;                           // line 140 — global counter
        }
    }
}
```

There is no threading. `xanadu(&task)` at `bed.c:153` processes exactly one FEBE request — calls into `fns.c`, down through `do1.c`/`do2.c`, mutates the in-memory trees, and returns — before the loop can touch the next fd. This imposes a **strict total order over all operations from all users touching any document or POOM**.

The global `user` variable at `bed.c:28` is reassigned on every iteration and is read deep inside operations — e.g., `do1.c:292` passes it directly to `addtoopen(newisaptr, user, TRUE, WRITEBERT)`. This is not safe under any concurrency model; the design assumes serial access as a precondition.

---

### 2. There Is One Shared Commit Point for All Documents

All document content lives inside two process-wide globals declared at `corediskout.c:21-22`:

```c
typegranf granf;   // The master document index — all POOMs are subtrees here
typespanf spanf;   // The master link/span index
```

Every mutating operation reaches these globals through the same path:
- `doinsert` → `inserttextingranf(taskptr, granf, ...)` — `do1.c:118`
- `docopy` → `findorgl(taskptr, granf, docisaptr, ...)` — `do1.c:55`
- `dodeletevspan` → `findorgl(taskptr, granf, docisaptr, ...)` — `do1.c:164`
- `docreatelink` → `createorglingranf(taskptr, granf, ...)` — `do1.c:209`

`granf` and `spanf` are not per-document. A document's content is a **subtree within** the single global granfilade, addressed by its ISA tumbler. When `findorgl` fetches `docorgl`, it returns a pointer into this shared in-memory tree — not a copy, not an isolated snapshot.

The sole disk commit function is `writeenfilades()` at `corediskout.c:68-88`:

```c
int writeenfilades(void) {
    // Write ALL of granf to GRANFDISKLOCATION
    temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
    temporgl.cinfo.granstuff.orglstuff.orglptr = (typecuc *)granf;
    ((typecuc *)granf)->leftbroorfather = (typecorecrum *)&temporgl;
    orglwrite(&temporgl);                          // line 79
    
    // Write ALL of spanf to SPANFDISKLOCATION
    temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
    temporgl.cinfo.granstuff.orglstuff.orglptr = (typecuc *)spanf;
    ((typecuc *)spanf)->leftbroorfather = (typecorecrum *)&temporgl;
    orglwrite(&temporgl);                          // line 87
}
```

Both trees are always written together. `writeenfilades` is called:
- At process exit: `indiskexit()` → `writeenfilades()` — `corediskout.c:44`
- When all users leave: `diskflush()` → `writeenfilades()` + `initkluge(granf, spanf)` — `corediskout.c:62-63`; triggered from `bed.c:105`
- At SIGINT: `flagquitting()` → `writeenfilades()` — `bed.c:183`

It is **never** called between individual FEBE requests. Accumulated mutations from document A and document B coexist in the shared in-memory `granf`/`spanf` trees until one of those three shutdown events occurs. There is no mechanism to commit document A's changes to disk while leaving document B's in-memory state uncommitted.

---

### 3. Code Paths That Explicitly Assume a Single Total Order

**a. The BERT table has no locking.** `bert.c:29` declares:
```c
static conscell *berttable[NUMBEROFBERTTABLE];
```
The hash table mutation functions `addtoopen`, `removefromopen`, `exitbert` use linked-list surgery with no synchronization primitive. They are correct only because the event loop guarantees serial execution. `checkforopen()` at `bert.c:52-87` checks `bert->connection == connection` to distinguish your open from another user's — this assumes no two operations run simultaneously and no BERT state changes mid-check.

**b. The global `user` variable is written in the event loop and read inside operations.** At `bed.c:120`, `user = fdtoplayer[i]` sets the current connection. At `do1.c:292`, `addtoopen(newisaptr, user, TRUE, WRITEBERT)` reads it. There is no per-operation capture of `user` before passing it into the call chain — it is read directly from the global. Any concurrent request would overwrite `user` before the inner call reads it.

**c. The GC reference counter `reservnumber` is a single global.** `credel.c:23` declares `INT reservnumber = 0;`. The `reserve()` function at `credel.c:370` does `++reservnumber` to protect tree nodes from the garbage collector during a traversal. This is a global, not per-document-subtree. If two operations ran concurrently and both called `reserve()`, the count would not correctly guard either one's subtrees independently.

**d. `ntaskorcommand` is a global sequence number used for maintenance scheduling.** `common.h:123` declares `long ntaskorcommand;`. `insertnd.c:25` (inside `#ifdef UndEfInEd`, so compiled out in current form but architecturally revealing) uses it as `(ntaskorcommand%100) == 0` to throttle `asserttreeisok` calls. The design concept is: a single monotonically increasing counter represents global system progress. There is no per-document progress counter.

---

### 4. Could the Design Be Extended to Per-Document Independent Commit?

The POOM structure makes this *theoretically reachable* but structurally non-trivial. Each document lives as a named subtree inside `granf`, identified by its ISA. `orglwrite()` (called from `writeenfilades`) operates at the subtree level — it takes a single `typecbc *` root and writes its subtree. So the serialization granularity of the *write path* is already per-subtree.

What would need to change:

1. **`writeenfilades` would need a per-document variant.** Currently it always writes both the full `granf` and the full `spanf`. A per-document commit would need to know which orgls inside `granf` and which spans inside `spanf` are dirty and belong to a given home document, then write only those. No such mapping exists in the current code.

2. **The spanfilade (`spanf`) is cross-document by design.** Links span across documents. The spanf records endpoint sets that may touch multiple home documents. There is no clean partition of `spanf` by home document; a link from document A to document B creates entries in `spanf` under the link's ISA. Per-document commit of `spanf` would require either splitting it by home document or accepting that a link commit touches two documents' subtrees.

3. **The `user` global and BERT table would need to become operation-local.** These are simple refactors — pass connection ID as a parameter rather than reading a global — but they are pervasive.

4. **The disk block allocator (`diskalloc.c:117`) references a global bitmap.** A shared disk bitmap means concurrent allocation by two per-document commit paths would race. This too would need per-document or per-allocation locking.

---

### Conclusion

**Yes, ordering is globally serialized.** The single `select()` event loop in `bed.c:103-149` processes one FEBE request at a time across all users and all documents. There is one global in-memory state (`granf`, `spanf`), one global commit point (`writeenfilades`), and several code paths — the `user` global, the lockless BERT table, and the single `reservnumber` GC counter — that would produce incorrect behavior under any concurrency. The design assumes, without encoding it explicitly, that a single total order covers all operations on all POOMs.

**The POOM subtree structure would permit per-document commit in principle**, since `orglwrite` works at subtree granularity. But the current code has no partitioning of dirty state by home document, no per-document commit entry point, no isolation of the cross-document spanfilade, and several globals that would need to become operation-local before independent commits could be attempted.
