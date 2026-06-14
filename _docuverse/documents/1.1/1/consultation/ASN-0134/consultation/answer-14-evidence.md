## Question 14 [evidence]

> Because `findisatoinsertmolecule` is a stateless query-and-increment against the current granfilade maximum, can two sessions inserting into the same document's I-range ever both compute the same `max+1`, or does run-to-completion guarantee the first insert is committed before the second queries?

## KB Synthesis

Run-to-completion guarantees exclusive safety here — two sessions cannot race on `findisatoinsertmolecule`.

The backend's `bed.c` event loop is strictly single-threaded with no preemption. `xanadu(&task)` executes the complete operation sequence — allocation, granfilade write, POOM update, response — before returning to `select()`. Even when multiple frontend file descriptors are ready simultaneously, the loop iterates over them sequentially: session A's INSERT runs to completion before session B's begins [INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH].

The stateless allocation design works precisely because of this serialization. `findisatoinsertmolecule` queries the in-memory granfilade tree for the current maximum via `findpreviousisagr`, then increments by 1 [SS-ADDRESS-SPACE, Finding 0061]. By the time session B reaches its `findpreviousisagr` call, session A's newly allocated I-address is already present in the in-memory tree — so B observes `A_max + 1` as the new floor and allocates `A_max + 2`. There is no window in which both sessions hold the same `max` reading simultaneously.

The key quote from [INV-SEQUENTIAL-DISPATCH]:

> Frontend i's request completes entirely before frontend i+1's request begins.

This is unconditional. The multi-step nature of INSERT (allocate → write granfilade → write spanfilade → update POOM) is invisible to other sessions because the entire sequence is one atomic dispatch [INV-ATOMICITY]. No partial-INSERT state is ever exposed.

One caveat worth noting: [PRE-CONCURRENT-INSERT] flags that the *permanent layer B-tree operations themselves* (pointer modifications, `father->numberofsons` updates, split/rebalance) are not concurrency-safe in a threading sense. But this is moot because the event loop never creates threads — the serialization guarantee comes from the architecture, not from locks. If the daemon were ever modified to use threads, the stateless query-and-increment pattern would immediately become a race.

---

## Code Exploration

I now have everything needed. Here is the full answer with all code citations.

---

## Answer: Run-to-Completion Guarantees No ISA Collision

**Short answer:** Two sessions inserting into the same document's I-range can never both compute the same `max+1`. The guarantee is structural: the backend is a **single-threaded, synchronous event loop** with no interleaving between requests. By the time the second session's `findisatoinsertmolecule` runs, the first session's `insertseq` has already mutated the granfilade in memory.

---

### 1. The Event Loop Is Single-Threaded (`bed.c`)

The entire backend runs in one process, one thread. The main loop in `bed.c:103-149`:

```c
for (;;) {
    ...
    inputfds2 = inputfds;                          // [bed.c:110] snapshot ready fds
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                ...
                xanadu(&task);                     // [bed.c:128] handle one request
                ...
            }
        }
    }
    ...
}
```

Two critical points:

- **`inputfds2` is snapshotted at line 110** before the inner `for` loop starts. Even if sessions A and B are both ready, they are visited sequentially: A at `i=3`, B at `i=7`, etc.
- **`xanadu(&task)` at line 128 is a blocking, synchronous call.** Session B's `xanadu()` cannot begin until session A's `xanadu()` returns.

There are no threads, no `fork`, no coroutines anywhere in `bed.c`.

---

### 2. `xanadu()` Runs a Full Request to Completion (`bed.c:153-172`)

```c
int xanadu(typetask *taskptr)
{
    ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // [bed.c:162] dispatch handler
        sendresultoutput(taskptr);         // [bed.c:163] send response
        ...
    }
    tfree(taskptr);
    ...
}
```

The dispatch at line 162 invokes `insert()` from `fns.c`, which calls all the way down the stack synchronously. `xanadu()` does not return until `insert()` and `sendresultoutput()` have both finished.

---

### 3. The Full Insert Call Chain Is Synchronous

Tracing the call chain for an insert request:

| Caller | Callee | File |
|--------|--------|------|
| `xanadu()` | `insert()` | `bed.c:162` → `fns.c:84` |
| `insert()` | `doinsert()` | `fns.c:92` |
| `doinsert()` | `inserttextingranf()` | `do1.c:118` |
| `inserttextingranf()` | `inserttextgr()` | `granf1.c:46` |
| `inserttextgr()` | `findisatoinsertgr()` | `granf2.c:92` |
| `findisatoinsertgr()` | `findisatoinsertmolecule()` | `granf2.c:142` |

`inserttextgr` at `granf2.c:83-109` shows exactly the query-then-mutate sequence:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, ...)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))   // [granf2.c:92] find max+1
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);            // [granf2.c:99] mutate granfilade
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    ...
}
```

And `findisatoinsertmolecule` at `granf2.c:158-181` is where the `max+1` is computed:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // [granf2.c:164] find current max
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);          // [granf2.c:166] compute max+1
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if ...
}
```

`findpreviousisagr` at `granf2.c:255-278` traverses the granfilade tree to find the current maximum ISA below `upperbound`. It reads the **live in-memory enfilade state**.

---

### 4. The In-Memory Mutation Happens Before the Loop Advances

The sequence for session A:

1. `findpreviousisagr` traverses the granfilade → finds current max M [`granf2.c:164`]
2. `findisatoinsertmolecule` computes `M+1` and writes it into `lsa` [`granf2.c:165-176`]
3. `insertseq` mutates the in-memory granfilade at address `M+1` [`granf2.c:99`]
4. `inserttextingranf` returns → `doinsert` returns → `insert` returns → `xanadu` returns [`bed.c:162`]
5. Only now does the `for` loop in `main` advance to session B's fd [`bed.c:118`]
6. Session B's `xanadu()` begins; its `findpreviousisagr` traverses the granfilade and sees the node at `M+1` already present

Session B cannot call `findpreviousisagr` until step 6. By then, the mutation from step 3 is in memory. So session B computes `(M+1)+1 = M+2`.

---

### 5. Signals Do Not Preempt In-Progress Requests

The only signal registered that could interrupt processing is `SIGINT`, handled at `bed.c:175-188`:

```c
void flagquitting()
{
    signal(SIGINT, SIG_IGN);
    if (mightbeblocked) {
        ...exit(0);
    } else
        quitafteruser = TRUE;   // [bed.c:187] set flag, check after current request
}
```

`mightbeblocked` is only `TRUE` when the server is blocked in `new_players()` waiting for connections [`bed.c:99,107,146`], never during request dispatch. During `xanadu()`, `SIGINT` only sets `quitafteruser`, checked at `bed.c:129` after `xanadu()` returns. It does not interrupt the running request.

---

### Conclusion

`findisatoinsertmolecule` is indeed a stateless query-and-increment against the live granfilade. But collision is structurally impossible because:

1. There is **exactly one thread of execution** in the entire backend.
2. The `for` loop over ready fds in `main()` calls `xanadu()` **one at a time, synchronously**.
3. **`insertseq` commits the mutation to the in-memory enfilade** before `xanadu()` returns — well before the next session's `findpreviousisagr` could traverse the tree.

The "run-to-completion" guarantee is not a locking protocol — it is a consequence of the architecture. The backend is to concurrent access what a single register file is to concurrent CPU writes: there is only ever one writer, and the write is always visible before the next reader begins.
