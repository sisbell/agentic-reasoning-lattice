## Question 1 [evidence]

> Does ValidComposite★ (ASN-0047) define a composite as a contiguous transition sequence Σ₀ → … → Σₙ in which no foreign elementary transition may interleave, making composite-level atomicity definitional rather than a stronger property the substrate must separately provide?

## KB Synthesis

Not answerable from the KB.

The KB contains implementation findings about udanax-green's run-to-completion event loop ([INV-ATOMICITY], [INV-SEQUENTIAL-DISPATCH]) — which establish that each FEBE operation executes without interleaving at the substrate level — but it contains no findings about ASN-0047 or any definition of `ValidComposite★`. The KB does not cover spec document definitions or their logical structure.

To answer the question, ASN-0047 itself would need to be in scope.

---

## Code Exploration

I now have enough evidence from direct source reads. Let me compile the answer.

---

## ValidComposite (ASN-0047): Is Composite-Level Atomicity Definitional?

**The short answer is yes — but the framing requires precision.** The term "ValidComposite" and the label "ASN-0047" appear nowhere in the udanax-green source code, its findings, or its knowledge base. The implementation does not use the vocabulary of "composite transitions" or "elementary transitions" at all. What the code *does* contain is a concrete architectural mechanism that makes composite-level atomicity structurally inevitable rather than separately enforced. Here is the full account from source.

---

### The Execution Model: `bed.c`

The backend entry point is `bed.c`. The main loop:

```c
// bed.c:103-149
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
        ...
    } else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.inp  = player[user].inp;
                task.outp = player[user].outp;
                task.account = player[user].account;
                xanadu(&task);          // ← BLOCKS until complete
                ...
            }
        }
    }
    leave(player, &n_players);
    new_players(player, &n_players, FALSE, &task);
}
```

`xanadu()` at `bed.c:153-172`:

```c
int xanadu(typetask *taskptr)
{
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // dispatch to handler
        sendresultoutput(taskptr);
        ...
    }
    tfree(taskptr);
    ...
}
```

The loop does **not** return to `select()` until `xanadu()` returns. `xanadu()` does not return until `(*requestfns[request])` returns. There are no threads, no state-modifying signal handlers (`SIGINT` only sets `quitafteruser = TRUE` at `bed.c:187`), and no preemption.

---

### What a "Composite" Operation Actually Is

Each FEBE request maps to a C handler in `requestfns[]`. These handlers call multiple internal sub-functions sequentially. From `fns.c:84-98`, the INSERT handler:

```c
// fns.c:84-98
void insert(typetask *taskptr)
{
    typeisa docisa, vsa;
    typetextset textset;

    (void) getinsert(taskptr, &docisa, &vsa, &textset);
    putinsert(taskptr);                         // send response
    if (!doinsert(taskptr, &docisa, &vsa, textset))
        fprintf(stderr,"requestfailed in insert\n");
}
```

`doinsert()` at `do1.c:87-123`:

```c
// do1.c:117-122
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy(taskptr, docisaptr, vsaptr, ispanset)
        /* docopy includes insertpm + insertspanf */
    );
return(ret);
```

`docopy()` at `do1.c:45-65` chains:

```c
// do1.c:53-64
return (
   specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa(vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)   // POOM update
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN) // spanf update
&& asserttreeisok(docorgl)
);
```

So a single INSERT involves: I-address allocation in `granf`, granfilade text insertion, POOM V→I mapping update, and spanfilade DOCISPAN insertion — all within one invocation of `requestfns[INSERT]`, which itself executes within one iteration of the `select()` loop.

CREATELINK (`do1.c:195-220`) is even longer — seven chained operations across both `granf` and `spanf`, all under one `requestfns[CREATELINK]` call:

```c
// do1.c:208-220
return (
     createorglingranf(...)       // step 1: allocate link orgl
  && tumbler2spanset(...)         // step 2
  && findnextlinkvsa(...)         // step 3
  && docopy(...)                  // step 4: inscribe link ref in doc
  && findorgl(...)                // step 5
  && specset2sporglset(...)       // step 6
  && ...
  && insertendsetsinspanf(...)    // step 7: index endpoints in spanf
);
```

`kb-formal.md:3868` characterises this precisely: *"Link creation (`docreatelink`) is a compound state transition that updates both enfilades atomically."*

---

### Is Atomicity Definitional or Separately Enforced?

**Definitional.** There is no separate enforcement mechanism:

- No mutual-exclusion locks
- No transaction log with rollback capability
- No two-phase commit
- No atomic CPU primitives used for multi-step coordination

`bert.c` (the document-access-control module) does track open/write state per connection:

```c
// bert.c:52-86  — checkforopen
int checkforopen(tumbler *tp, int type, int connection)
{
    for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
        bert = p->stuff;
        if (tumblereq(tp, &bert->documentid)) {
            if (connection == bert->connection) {
                switch (bert->type) {
                    case READBERT:  return (type == READBERT) ? READBERT : -1;
                    case WRITEBERT: return WRITEBERT;
                }
            } else {
                if (bert->type != READBERT) foundnonread = TRUE;
            }
        }
    }
    ...
}
```

But this is sequential conflict-detection, not mutual exclusion. It is only reachable because only one `xanadu()` call executes at a time — there is no race condition to guard against.

`kb-formal.md:6106-6108` (INV-ATOMICITY, sourced from Finding 0042) states it directly:

> *"The `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`. Multi-step operations like INSERT (which involves I-address allocation, granfilade insertion, spanfilade update, and POOM update) execute as a single uninterruptible unit. There are no threads, no state-modifying signal handlers, and no preemption."*

> *"This is the foundational atomicity invariant: every operation's view of shared state (ispace, spanfilade, POOMs) is consistent throughout execution. **No interleaving is possible.** This means all state transitions documented in other findings are truly atomic — there is no partial-execution state observable by any frontend. Any formal spec can model operations as atomic transitions **without reasoning about interleavings.**"*

And from `bed.c:118-128` (INV-SEQUENTIAL-DISPATCH in kb-formal.md), even when multiple frontends have requests ready simultaneously, they are serialised by the inner `for` loop — not by any lock, but because the loop itself is single-threaded.

---

### Direct Answer to the Question

**Does ValidComposite (ASN-0047) define a composite as a contiguous transition sequence Σ₀ → … → Σₙ in which no foreign elementary transition may interleave, making composite-level atomicity definitional rather than a stronger property the substrate must separately provide?**

The terminology "ValidComposite" and "ASN-0047" are not present in the C source. But the **architectural fact the question describes is correct**: the substrate produces exactly the behaviour that proposition asserts, and it does so definitionally.

The mechanism is: `bed.c`'s event loop dispatches exactly one `xanadu()` per `select()` iteration, and `xanadu()` dispatches exactly one `requestfns[request]()` call to completion before returning. Every FEBE request — whether "elementary" (a single-step query) or "compound" (INSERT's four sub-steps, CREATELINK's seven) — executes as one uninterruptible unit within that call frame. There is no substrate mechanism by which any other request's sub-steps can interleave with it. The prohibition on interleaving is not enforced; it is architecturally impossible.

The practical consequence: composite-level atomicity (the fact that a multi-step state transition Σ₀ → Σ₁ → … → Σₙ leaves no intermediate Σᵢ observable by any foreign client) is **a consequence of the execution model's structure**, not of a separately provided serialisation service. A formal spec built on this substrate is entitled to treat every FEBE operation as an atomic state transition and ignore intermediate states, because those intermediate states are not reachable from any frontend — `kb-formal.md:6108`. The atomicity guarantee is as strong as the guarantee that `xanadu()` does not return early, which is a structural property of the C call stack, not a runtime invariant that must be checked or enforced.

**One caveat**: `kb-formal.md:8304` notes that if the backend were ever made concurrent, V-positions of link orgls would **not** be stable under interleaving, because `findnextlinkvsa` (`do2.c:151-167`) reads the current extent non-atomically with respect to insertion. This confirms that the current atomicity is structural/definitional — remove the single-threaded architecture and you would need to separately provide atomicity, which the substrate currently does not have the machinery for.
