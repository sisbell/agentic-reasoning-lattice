## Question 12 [gregory]

> Can two concurrent sessions race to baptize the same position, and if so, does the single-threaded event loop serialization fully prevent duplicate baptism, or is there additional guarding?

## KB Synthesis

**The single-threaded event loop fully prevents racing. No additional guarding exists or is needed.**

## Analysis

**What baptism is architecturally**

Baptism allocates a new tumbler address by writing an orgl entry to the granfilade via `createorglingranf` → `findisatoinsertnonmolecule`. The allocation queries the granfilade tree for the highest existing address under the parent, then increments — a stateless query-and-increment [SS-ADDRESS-ALLOC Finding 0061].

**Why two sessions cannot race**

[INV-SEQUENTIAL-DISPATCH] and [INV-ATOMICITY] are the decisive facts. The `bed.c` event loop calls `xanadu(&task)` for one request at a time. The entire operation — request parsing, all state mutations, response transmission, memory cleanup — runs to completion before `select()` returns for the next file descriptor. There are no threads, no preemptive signal handlers modifying shared state, and no yield points within an operation.

From Finding 0042:
> I-address allocation via `findisatoinsertgr()` uses a global search-and-increment to find fresh addresses. **This is safe without locking because the single-threaded event loop guarantees no concurrent allocations.**

**The allocation function is stateless with respect to sessions**

[SS-ADDRESS-SPACE Finding 0061] confirms the allocation function is `next_iaddr(granf) = max_iaddr(granf) + 1` — a pure function of granfilade state with no session-local counter. When session B executes after session A, `findpreviousisagr` will find A's newly allocated address in the tree and increment past it. There is no window between "find max" and "write new entry" because the entire operation is atomic.

**No additional guarding exists**

[PRE-CONCURRENT-INSERT] notes that *unsafe* concurrent insertions *would* corrupt shared pointers and `numberofsons` counters — confirming that the serialization is the *sole* protection mechanism, not one layer among several. There are no mutexes, no optimistic concurrency checks, no address reservations. The architecture trusts the event loop entirely.

**Summary**

| Concern | Answer |
|---|---|
| Can two sessions race to baptize the same position? | No — sequential dispatch prevents any interleaving |
| Is the event loop serialization sufficient? | Yes — it is the only mechanism and it is complete |
| Is there additional guarding (locks, reservations, etc.)? | No — none exists, none is needed given single-threaded dispatch |

---

## Code Exploration

Now I have everything I need. Let me compile the full answer.

---

## Can Two Sessions Race to Baptize the Same Position?

### The Event Loop: Run-to-Completion Serialization

`bed.c:103–148` is the entire event loop:

```c
for (;;) {
    // ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {           // bed.c:118
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                // ...
                xanadu(&task);                   // bed.c:128
            }
        }
    }
```

`xanadu()` at `bed.c:153–172` is fully synchronous:

```c
int xanadu(typetask *taskptr) {
    // ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);         // bed.c:162 — dispatch to handler
        sendresultoutput(taskptr);
    }
    tfree(taskptr);
}
```

The process is **single-threaded**. `select()` is the only inter-session switch point, and it only switches **between complete requests** — never within one. When `xanadu()` returns at `bed.c:128`, the entire request handler has finished.

---

### The "Baptism" Sequence: Read-Compute-Write

The term "baptism" does not appear in the source code. The concept maps directly to tumbler address assignment during object creation. The canonical path is:

**`docreatenewdocument()` → `createorglingranf()` → `createorglgr()` → `findisatoinsertgr()` → `findisatoinsertnonmolecule()` → `insertseq()`**

#### Step 1: Hint seeding

`do1.c:239`:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

The caller's account tumbler becomes the address-space hint.

#### Step 2: Address computation

`granf2.c:203–242`, `findisatoinsertnonmolecule()`:

```c
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // granf2.c:217 — READ
// ...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);               // granf2.c:237 — COMPUTE (first child)
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);            // granf2.c:239 — COMPUTE (next sibling)
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0,1,isaptr); // granf2.c:240
}
```

This is a **read-highest / increment / return** pattern — a classic check-then-act.

#### Step 3: Atomic insertion

`granf2.c:117–126`, `createorglgr()`:

```c
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))          // granf2.c:117 — READ+COMPUTE
    return FALSE;
// ...
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);                      // granf2.c:125 — WRITE
```

The computed address is immediately committed to the granfilade in the same synchronous call. There is no intermediate "pending" state.

---

### Can Two Sessions Collide?

**No, and here is why.**

In a multi-threaded or async system, the sequence at `granf2.c:217–240` would be a TOCTOU hazard: session A reads the highest address, session B reads the same highest address, both compute the same next address, both write.

But this system has no threads and no async yields. The call chain:

```
xanadu() [bed.c:162]
  → (*requestfns[request])(taskptr)      // e.g. docreatenewdocument
    → createorglingranf()                // granf1.c
      → createorglgr() [granf2.c:111]
        → findisatoinsertgr() [granf2.c:130]
          → findisatoinsertnonmolecule() [granf2.c:203]   // READ
        → insertseq() [granf2.c:125]                      // WRITE
```

…runs to completion without ever returning to the `select()` loop. Session B cannot be scheduled until `xanadu()` for session A has returned at `bed.c:128`. By that time, session A's address is already inserted in the granfilade.

One subtlety: the inner `for` loop at `bed.c:118–142` iterates over **all fds ready in one `select()` pass**. If sessions A and B are both ready simultaneously, they are processed one after the other within the same loop iteration — A's `xanadu()` completes before B's begins. This is still fully serialized.

---

### Is There Additional Guarding?

**No additional guarding exists, and none is needed.**

- There are no mutexes, semaphores, or atomic compare-and-swap operations anywhere in the baptism path.
- There is no duplicate-address check after insertion.
- There is no "did someone else take this address between my read and write?" guard.

The design places **total reliance** on the single-threaded event loop as the sole serialization primitive. This is correct by construction — the invariant "only one request executes at a time" is enforced structurally by the `select()`-then-sequential-dispatch loop at `bed.c:103–148`.

If the process were ever made multi-threaded or given async handlers that could yield mid-request, `findisatoinsertnonmolecule`'s read-compute-write would become a genuine race with no protection.

---

### Summary

| Property | Evidence |
|---|---|
| Single-threaded process | `bed.c:47` `int main(void)` — one process, no `fork`/`pthread` |
| Single-threaded event loop | `bed.c:128` `xanadu(&task)` called synchronously in inner for-loop |
| Address assignment is synchronous | `granf2.c:117–125`: `findisatoinsertgr` + `insertseq` in one call, no I/O between them |
| No additional guards | No mutex/semaphore in `granf2.c`, `granf1.c`, or `do1.c` |
| Edge case: two fds ready simultaneously | Still serialized by `bed.c:118–142` inner for-loop — A completes before B starts |

**Two concurrent sessions cannot race to baptize the same position. The single-threaded event loop provides complete serialization. There is no additional guarding because none is required by the architecture.**
