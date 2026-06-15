## Question 1 [evidence]

> Does udanax-green's allocator guarantee that a single insertion's content-address run is minted as one contiguous, uninterrupted chain segment — i.e., that no concurrent allocator (same-document or cross-document) can interleave a K.α step into that run and split it — or is contiguity only guaranteed under serialized/isolated execution?

## KB Synthesis

## Contiguity Guarantee: Serialized Execution, Not Concurrent-Safe Allocator

The short answer: contiguity within a single INSERT's content-address run is guaranteed, but **solely because the event loop is single-threaded with run-to-completion semantics** — not because the allocator has any inherent interleaving protection.

---

### Within a Single INSERT Call

`inserttextgr` allocates the entire run in one step [ST-INSERT / Finding 0031]:

```
tumblerincrement(&lsa, 0, textset->length, &lsa)
```

This mints `[prev_max + 1, prev_max + len]` as a single atomic operation within the function. There is no per-character loop, no yielding between characters. The run is contiguous by construction within the call.

### Why No Concurrent Allocator Can Interleave

The event loop in `bed.c` enforces total serialization [INV-ATOMICITY / Finding 0042, INV-SEQUENTIAL-DISPATCH / Finding 0042]:

- `xanadu(&task)` executes the entire operation — request parsing, all state mutations, response dispatch, memory cleanup — before returning to `select()`
- Even when multiple frontends have requests ready simultaneously, they are iterated strictly in order; frontend *i* completes before frontend *i+1* begins
- There are no threads, no preempting signal handlers, no coroutines

This is **stronger than per-document serialization** — it is global total ordering over all sessions and all enfilades. A K.α step from any other document's INSERT cannot slip in during a running INSERT because there is no mechanism by which it could be scheduled.

### The Allocator Itself Has No Inherent Protection

[PRE-CONCURRENT-INSERT / Finding 0041] is explicit: concurrent unsynchronized insertion into the same enfilade is unsafe. The `adopt(new, RIGHTBRO, ptr)` call modifies shared pointers, `father->numberofsons` would suffer lost updates under concurrent access, and split/rebalance operations assume exclusive access.

The allocator is stateless query-and-increment [SS-ADDRESS-SPACE / Finding 0061]:

```
findpreviousisagr → max current address → tumblerincrement by 1
```

No lock, no atomic reservation, no cached counter. It is safe only because the event loop ensures it is never called concurrently.

### The Instructive Cross-Type Case

[INV-MONOTONIC / Finding 0063] and [ST-CRUM-BOUND / Finding 0063] show what *sequential* interleaving looks like: INSERT "ABC" → CREATELINK → INSERT "DEF" breaks text-address contiguity because the CREATELINK operation's orgl allocation consumes I-address space between the two text runs. But CREATENEWVERSION does *not* break it [INV-MONOTONIC / Finding 0077] because version allocation draws from a separate tumbler subrange and does not touch the content allocation region.

This confirms the allocator makes no reservation that protects a text run from non-text allocations that occur in intervening operations. Contiguity within a run is an intra-call guarantee; isolation from other operations' allocations is a property of serialized scheduling.

### Summary

| Claim | Status | Basis |
|---|---|---|
| Single INSERT mints its run in one step | **Yes** | `tumblerincrement` over full length in `inserttextgr` [ST-INSERT] |
| No concurrent allocator can split the run | **Yes, but…** | …only because the event loop is single-threaded [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH] |
| The allocator has an inherent concurrency guard | **No** | [PRE-CONCURRENT-INSERT] explicitly states concurrent access is unsafe |
| Same-exponent, same-document allocations are isolated across operations | **No** | Sequential CREATELINK breaks text contiguity [INT-LINK-INSERT] |

The guarantee is real and unconditional under the current architecture, but it is entirely load-bearing on the serialized event loop. Remove that serialization and the allocator offers no protection at all.

---

## Code Exploration

I now have the complete call chain. Here is my full answer.

---

## Contiguity of the Content-Address Run in a Single Insertion

### Short answer

**Yes, contiguity is unconditionally guaranteed — but the mechanism is not a lock or atomic primitive. It is the single-threaded, run-to-completion architecture of the event loop.** The scenario the question describes (a concurrent allocator interleaving a K.α step into an in-progress run) cannot physically occur in this implementation.

---

### The allocation path, traced from source

#### 1. Entry: `doinsert` → `inserttextingranf`

`doinsert` [do1.c:87–123]:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` [granf1.c:43–47] is a thin wrapper:
```c
return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
```

#### 2. The allocation loop: `inserttextgr` [granf2.c:83–109]

This is the heart of the question.

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{
  tumbler lsa, spanorigin;
  ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))  // ← ONE call
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string,...);
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);           // ← tree write
        tumblerincrement (&lsa, 0, textset->length, &lsa);           // ← local arithmetic
    }
    ispanptr->stream = spanorigin;
    tumblersub (&lsa, &spanorigin, &ispanptr->width);                // ← width = total run
    ...
```

Two facts define the contiguity:

**Fact A — `findisatoinsertgr` is called exactly once** [granf2.c:92], before the loop begins. It is the only call that reads the granfilade tree to determine a new ISA.

**Fact B — All subsequent ISA values are pure local arithmetic.** The `lsa` cursor is a local stack variable. `tumblerincrement(&lsa, 0, textset->length, &lsa)` [granf2.c:100] is integer arithmetic on that variable — no tree read, no external state, no callback.

The final ispan returned is `[spanorigin, lsa − spanorigin]` — exactly the contiguous prefix minted by this one call.

#### 3. How `findisatoinsertgr` finds the starting K.α

`findisatoinsertgr` [granf2.c:130–156] dispatches to `findisatoinsertmolecule` for ATOM/text content [granf2.c:142].

`findisatoinsertmolecule` [granf2.c:158–181]:
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);   // ← lowerbound + 1
```

For a TEXTATOM insertion, when there is already content, the starting ISA is `lowerbound + 1` — immediately adjacent to the highest existing address. The run then continues contiguously for the length of the insertion.

#### 4. `insertseq` does NOT re-allocate an ISA

`insertseq` [insert.c:17–70] takes the caller-supplied `address` and inserts into the enfilade tree at that position. It never calls `findisatoinsertgr` or `findpreviousisagr`. The only arithmetic on `address` inside `insertseq` is in `fillupcbcseq` [insert.c:89,94], which packs text into an existing crum and advances a local copy of the cursor — but that local copy (`nextaddress`) is separate from `lsa` in `inserttextgr`. After `insertseq` returns, `inserttextgr` advances `lsa` by the full `textset->length` regardless.

---

### The concurrency model: `bed.c`

The event loop [bed.c:103–149]:

```c
for (;;) {
    ...
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];          // pick exactly one fd
                task.inp  = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                xanadu(&task);                 // process ONE request, run to completion
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`xanadu` [bed.c:153–172]:
```c
int xanadu(typetask *taskptr)
{
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);       // one FEBE dispatch, no yield
        sendresultoutput(taskptr);
        ...
    }
    tfree(taskptr);
    ...
}
```

The server is a **single Unix process with no threads**. Multiple frontends are multiplexed by `select()`, but exactly one is dispatched per outer loop iteration. `xanadu()` calls one FEBE handler — for INSERT, that resolves to `doinsert → inserttextingranf → inserttextgr → [loop] → return`. There is no preemption, no async I/O, no callback, no suspension point between loop iterations.

The entire call chain from `doinsert` to the final `return(ret)` [do1.c:122] is a single synchronous stack frame. No other frontend's request can begin executing until `xanadu()` returns and the outer loop picks the next `select()` winner.

---

### The definitive answer

| Claim | Verdict | Evidence |
|---|---|---|
| ISA for the run is queried from the tree exactly once | **True** | `findisatoinsertgr` called once before the loop [granf2.c:92]; not called inside the loop |
| All subsequent ISAs are pure local arithmetic | **True** | `tumblerincrement(&lsa, 0, len, &lsa)` [granf2.c:100] — stack variable, no external read |
| `insertseq` can allocate a new ISA mid-loop | **False** | `insertseq` [insert.c:17] takes the ISA as a parameter; it never calls back into `findisatoinsertgr` |
| Another session's INSERT can interleave into the run | **False** | Single-threaded event loop [bed.c:118–129]; `xanadu()` runs one request to completion before the next `select()` |
| Contiguity relies on an explicit mutex or atomic | **False** | There is no mutex; the guarantee is the serialized architecture |

**Contiguity is guaranteed unconditionally.** It is not a matter of "serialized vs. concurrent execution" because there is no concurrency — the architecture precludes it. The same single-threaded dispatch that protects cross-session ordering also protects the intra-insertion loop from interleaving. Within the loop, `lsa` is a private stack cursor advanced by arithmetic. The resulting ispan is always a single, uninterrupted chain from `spanorigin` to `spanorigin + Σ(textset lengths)`.
