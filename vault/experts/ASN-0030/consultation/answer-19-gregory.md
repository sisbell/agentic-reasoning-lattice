## Question 19 [gregory]

> In a multi-session scenario where session A creates content at I-address X and session B immediately copies it, is there any window — given run-to-completion scheduling in `bed.c` — where session B could observe the POOM entry for X but not yet see X in the granfilade?

## KB Synthesis

No. There is no such window. Run-to-completion scheduling eliminates it entirely.

## Why No Window Exists

**[INV-ATOMICITY]** (Finding 0042) establishes that `bed.c`'s event loop calls `xanadu(&task)` for a single frontend's request and blocks until it returns before calling `select()` again. The entire INSERT operation for session A — including `inserttextingranf` (granfilade allocation) and `insertpm` (POOM entry via `docopy`) — completes as one uninterruptible unit.

**[INV-SEQUENTIAL-DISPATCH]** (Finding 0042) further confirms that even when multiple frontend file descriptors are simultaneously ready in `select()`'s result, the loop iterates over them sequentially. Session B's COPY request cannot begin until session A's INSERT has fully returned to `select()`.

## The Ordering Guarantee Within INSERT

**[ST-INSERT]** (Finding 0036) documents the call chain: `doinsert` → `inserttextingranf` → `docopy` → `insertpm` + `insertspanf`. The granfilade allocation (step 1) precedes the POOM insertion (step 3) within the same atomic dispatch. The in-memory cache is global and shared across all sessions **[SS-CACHE-MECHANISM]** — there is no per-session view of state that could show a POOM entry before its corresponding granfilade entry.

## What Session B Observes

When session B's COPY eventually executes, it calls `findorgl` to locate the source document's orgl (**[PRE-COPY]**, Finding 0046), then `specset2ispanset` to convert V-spans to I-addresses, then `insertpm` to place them in B's POOM. By this point, session A's entire INSERT has completed. The granfilade and POOM entries for X are fully present in the shared in-memory state.

**Verdict:** The causal gap you describe — where the POOM entry exists without the granfilade entry — is structurally impossible under run-to-completion scheduling. Both entries are created within a single atomic operation. Session B will always see a consistent state where either neither exists (if A hasn't run yet) or both exist (if A has completed).

---

## Code Exploration

Now I have everything I need. Let me trace the full execution path carefully.

---

## Analysis: POOM/Granfilade Visibility Window

**Short answer: No such window exists — and the ordering of updates makes it doubly impossible.**

---

### 1. The Event Loop — `bed.c`

The scheduler is a single-threaded, non-preemptive `select()` loop. `bed.c:103-141`:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp = player[user].inp;
                // ...
                xanadu(&task);   // line 128
            }
        }
    }
    // ...
}
```

Each fd is dispatched sequentially inside the inner `for` loop. `xanadu()` is called and **must return before the loop advances to the next fd**. There is no threading, no coroutines, no `yield`.

`xanadu()` itself (`bed.c:153-172`):

```c
int xanadu(typetask *taskptr)
{
    typerequest request;
    // ...
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    // line 162 — handler runs to completion
        sendresultoutput(taskptr);          // line 163 — flush happens after
    }
    tfree(taskptr);
    // ...
}
```

The handler runs to completion; only then is output flushed and control returns to the loop. If session A (fd=i) and session B (fd=i+1) are both ready in the same `select()` wake, A's entire handler completes before B is dispatched.

---

### 2. The Insert Handler — `fns.c`

`fns.c:84-98` (the live implementation — the commented-out canonical version at line 69 was replaced by this "kluged unix version for speed"):

```c
void insert(typetask *taskptr)
{
    typeisa docisa, vsa;
    typetextset textset;
    bool getinsert(), doinsert();

    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);                           // line 91 — buffers OK response
    if (!doinsert (taskptr, &docisa, &vsa, textset))  // line 92 — updates data structures
        fprintf(stderr,"requestfailed in insert\n");
}
```

Note `putinsert()` [line 91] is called before `doinsert()` [line 92]. But `putinsert()` only **buffers** into `taskptr->outp`; the actual network flush happens in `sendresultoutput()` at `bed.c:163`, which executes **after** the entire handler returns. So session A's client doesn't receive acknowledgment until after the data structures are updated — and crucially, session B's dispatch cannot begin until after `xanadu()` for session A returns.

---

### 3. `doinsert` — The Ordering of Granfilade vs POOM Updates

`do1.c:87-123`:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    typehint hint;
    typespanset ispanset;
    INT ret;
    bool doretrievev(), inserttextingranf(), docopy();

    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // line 118
        && docopy (taskptr, docisaptr, vsaptr, ispanset)                 // line 119
    );
    return(ret);
}
```

The sequence is unambiguous:

1. **`inserttextingranf()` [do1.c:118]** — content is placed in the granfilade; on return, `ispanset` holds the I-address X.
2. **`docopy()` [do1.c:119]** — uses `ispanset` to update the POOM (via `insertpm()`) and spanfilade (via `insertspanf()`).

`inserttextingranf()` is `inserttextgr()` in `granf2.c:83-109`:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    // ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        // ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // line 99 — granfilade entry placed
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    // ... build ispanptr from spanorigin to lsa ...
    *ispansetptr = ispanptr;
    return (TRUE);
}
```

The I-address X is allocated and the content is inserted into the granfilade at `granf2.c:99` (`insertseq()`). Only after this function returns does control reach `docopy()` in `do1.c:119`, which calls `insertpm()` (POOM update).

`docopy()` at `do1.c:45-65` confirms:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    // ...
    return (
        specset2ispanset (...)              // resolve I-spans
        && findorgl (...)                   // locate document POOM
        && acceptablevsa (vsaptr, docorgl)
        && asserttreeisok(docorgl)
        && insertpm (...)                   // line 60 — POOM updated
        &&  insertspanf (...)               // line 62 — spanfilade updated
        && asserttreeisok(docorgl)
    );
}
```

The update order within a single `doinsert` call is strictly:

```
granfilade (insertseq)  →  POOM (insertpm)  →  spanfilade (insertspanf)
```

---

### 4. Answer to the Question

**No window exists where session B could observe the POOM entry for X without X being present in the granfilade.**

There are two independent reasons:

**Reason 1 — Run-to-completion scheduling forecloses all interleaving.** The inner loop in `bed.c:118-141` processes one fd at a time. Session B's `xanadu()` call cannot begin until session A's `xanadu()` call returns. Between the two dispatches, all of session A's data structure updates — both granfilade and POOM — are already complete and globally visible (they modify shared in-core data structures, not per-session copies).

**Reason 2 — Granfilade is updated *before* POOM within the same request.** Even if preemption existed (it doesn't), the only inconsistent intermediate state that could be observed would be: **granfilade has X, POOM does not yet**. The question posits the *inverse* (POOM has X, granfilade does not), which cannot arise from `doinsert`'s internal ordering (`do1.c:118-119`). I-address X is minted and stored in the granfilade by `inserttextingranf()` before `docopy()` / `insertpm()` ever executes.

The architecture makes this invariant structural: `insertpm()` receives the I-span returned by `inserttextingranf()`, so the granfilade entry is a logical prerequisite. The compiler-enforced call chain (`do1.c:118-119`, short-circuit `&&`) guarantees the granfilade step runs and succeeds before the POOM step is attempted.
