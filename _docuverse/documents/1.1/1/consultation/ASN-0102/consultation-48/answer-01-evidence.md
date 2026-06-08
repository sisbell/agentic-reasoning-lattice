## Question 1 [evidence]

> In udanax-green, is docopy ever committed as part of a larger multi-operation transaction, or is each docopy always its own atomic unit bracketed by its own POOM/spanfilade writes?

## KB Synthesis

`docopy` is never its own FEBE-level operation and has no independent transaction bracket. It is always called as an internal step within a larger FEBE dispatch.

**`docopy` is called from three FEBE operations:**

1. **INSERT** (`doinsert`) — `inserttextingranf` → `docopy` [ST-INSERT, Finding 0036]
2. **CREATELINK** (`docreatelink`) — 3-step compound: create orgl + `docopy` (link ISA into 2.x) + `insertendsetsinspanf` [ST-CREATE-LINK, Finding 0012]
3. **CREATENEWVERSION** via `docopyinternal` — allocate doc addr + `docopy` entire text vspan [ST-VERSION, Finding 0077]

**Atomicity comes from the event loop, not from `docopy` itself.** The `bed.c` event loop runs each FEBE dispatch to completion via `xanadu(&task)` before returning to `select()`. No threads, no preemption, no interleaving [INV-ATOMICITY, Finding 0042]. This makes the entire FEBE operation — including every `docopy` call within it — one uninterruptible unit.

**Within a single `docopy` invocation, both writes always happen together:** `insertpm` (POOM) followed by `insertspanf(... DOCISPAN)` (spanfilade). There is no partial-commit at the `docopy` level. However, there is no rollback mechanism — if the sequence is interrupted mid-way (e.g., crash), the enfilades can desync [INV-DUAL-ENFILADE-CONSISTENCY, Finding 0012].

**No explicit transaction concept exists** at any level. The system has no begin/commit bracketing. `docopy` is always a called subroutine within a FEBE dispatch, and its writes are sequentially coupled to whatever other writes its caller performs in that same dispatch.

---

## Code Exploration

I have all the information I need. Here is the full answer.

---

## Is `docopy` Ever Part of a Larger Multi-Operation Transaction?

**Short answer:** Yes — but through compound *intra-request* sequences, not through any explicit transaction mechanism. And in at least one call site (`docreatelink`) additional POOM and spanfilade writes occur *after* `docopy` returns, within the same FEBE request.

---

### 1. There Is No Transaction/Commit Mechanism

`bed.c:xanadu()` (lines 153–172) is the event-loop dispatcher. It calls one handler per FEBE request, then calls `tfree()` to free the task-local allocation arena, and returns:

```c
(*requestfns[request])(taskptr);
sendresultoutput(taskptr);
...
tfree(taskptr);
```

There is no "begin transaction" / "commit transaction" bracketing. `diskflush()` (`corediskout.c:58–64`) only runs when `n_players < 1` — that is, when all users have disconnected. Enfilade nodes are marked dirty in-core via `ivemodified()` and flushed en masse. There is no per-operation flush or rollback. If a step in a compound `&&`-chain fails, prior enfilade writes stay applied.

---

### 2. `docopy` as Its Own FEBE Operation — Atomic on the Wire

When the FEBE `copy` command arrives, `fns.c:35–47` dispatches it:

```c
void copy(typetask *taskptr)
{
    if (
       getcopy (taskptr, &docisa, &vsa, &localspecset)
    && docopy (taskptr, &docisa, &vsa, localspecset))
        putcopy (taskptr);
      else
        putrequestfailed (taskptr);
}
```

Here `docopy` is the entire body of work. Internally, `docopy` itself (`do1.c:45–65`) performs two enfilade writes in sequence:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // POOM write
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // spanfilade write
```

These are sequential with no commit between them, but since no other code runs in this FEBE request, the `copy` command is effectively a single atomic unit *on the wire*.

---

### 3. `docopy` Embedded in `doinsert` — Preceded by a Granfilade Write

The FEBE `insert` handler (`fns.c:84–98`) calls `doinsert`, which at `do1.c:117–122` does:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

`inserttextingranf` writes new text into the granfilade *first*, producing the `ispanset` that `docopy` then records into the POOM and spanfilade. The two are coupled in a single FEBE request with no commit between them. `docopy` here is not self-contained — there is a prior granfilade write in the same request. Nothing writes after `docopy` in this path.

---

### 4. `docopy` Embedded in `docreatelink` — Additional POOM and Spanfilade Writes Come After

The FEBE `createlink` handler (`fns.c:100–112`) calls `docreatelink` at `do1.c:195–221`, which is an 11-step `&&`-chain:

```c
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // step 1 — granfilade write
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)         // step 2
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)           // step 3
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)          // step 4 — POOM + spanfilade
  && findorgl (...)                                           // step 5
  && specset2sporglset (..., &fromsporglset, ...)             // step 6
  && specset2sporglset (..., &tosporglset, ...)               // step 7
  && specset2sporglset (..., &threesporglset, ...)            // step 8
  && setlinkvsas (...)                                        // step 9
  && insertendsetsinorgl (taskptr, linkisaptr, link,          // step 10 — more POOM writes
         &fromvsa, fromsporglset, &tovsa, tosporglset, ...)
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,        // step 11 — more spanfilade writes
         fromsporglset, tosporglset, threesporglset)
);
```

`docopy` is step 4. After it returns, steps 10 and 11 write more data into the same structures:

- **`insertendsetsinorgl`** (`do2.c:130–143`) calls `insertpm` two or three times — these are additional POOM writes into the *link*'s own orgl for its from/to/three endpoint addresses.
- **`insertendsetsinspanf`** (`do2.c:116–128`) calls `insertspanf` two or three times — these are additional spanfilade writes recording the link's endpoints.

Both `insertpm` (`orglinks.c:75`) and `insertspanf` (`spanf1.c:15`) bottom out in `insertnd` (`insertnd.c:15`), which is the same enfilade insertion routine used inside `docopy`. So within a single `createlink` FEBE request, `docopy` is *not* the last write — additional POOM and spanfilade writes follow it, with no commit boundary separating them.

---

### 5. `docopyinternal` in `docreatenewversion`

`do1.c:260–299` defines `docreatenewversion`. It uses `docopyinternal` (`do1.c:66–82`) — structurally identical to `docopy` but passes `NOBERTREQUIRED` to `findorgl` instead of `WRITEBERT`, skipping the open-document access check. This is correct because `docreatenewversion` has already handled access control directly via `addtoopen`:

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);   // bert table write (not enfilade)
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // POOM + spanfilade
logbertmodified(newisaptr, user);              // bert table update
doclose(taskptr, newisaptr, user);             // bert table write
```

The enfilade writes in `docopyinternal` are not the last writes in this compound sequence either (though the subsequent writes are to the BERT hash table in memory, not to the POOM or spanfilade enfilades).

`docreatenewversion` is called either as its own FEBE request (`fns.c:289–300`) *or* internally from `doopen` in `bert.c:264–322` when a copy-on-write open is needed — meaning it can also be silently triggered as a side-effect of another operation.

---

### Summary

| Call site | FEBE request | `docopy` position | Writes before | Writes after `docopy` |
|-----------|-------------|------------------|---------------|----------------------|
| `copy` (`fns.c:35`) | `copy` | sole operation | none | none |
| `doinsert` (`do1.c:118`) | `insert` | step 2 of 2 | granfilade (`inserttextingranf`) | none |
| `domakelink` (`do1.c:185`) | (internal) | step 4 of 10 | granfilade | `insertendsetsinorgl`, `insertendsetsinspanf` |
| `docreatelink` (`do1.c:212`) | `createlink` | step 4 of 11 | granfilade | `insertendsetsinorgl` (POOM), `insertendsetsinspanf` (spanfilade) |
| `docopyinternal` in `docreatenewversion` (`do1.c:293`) | `createnewversion` or side-effect of `open` | step 2 of 4 | granfilade (`createorglingranf`) | BERT table updates only |

**`docopy` has its own internal POOM+spanfilade write pair** (`insertpm` + `insertspanf` at `do1.c:60–62`). That pair is always executed atomically together within `docopy`'s own body. But `docopy` is *not* always the outermost atomic unit — in `docreatelink` (the most significant case), it is step 4 of 11, and two more rounds of `insertpm` and `insertspanf` follow it in the same FEBE request, with no commit boundary and no rollback capability between any of the steps.
