## Question 20 [gregory]

> Is there any mechanism that guarantees spanfilade completeness — that every link's endset I-spans are fully indexed — or can races, crashes, or partial `insertendsetsinspanf` failures leave a link permanently undiscoverable even though its orgl exists in the granfilade?

## KB Synthesis

## Spanfilade Completeness: No Guarantee Across Crashes

The KB gives a clear answer: **within a session, link creation is atomic, so no race can leave a link half-indexed; but crashes can produce a permanently undiscoverable link whose orgl exists in the granfilade.**

---

### What prevents races

The event loop is strictly single-threaded and run-to-completion [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]. `docreatelink` executes its three steps — (1) create link orgl in granf, (2) insert link reference in document's 2.x POOM, (3) call `insertendsetsinspanf` — as a single uninterruptible unit before `select()` is re-entered [ST-CREATE-LINK, SS-GRANF-OPERATIONS]. No other FEBE operation can interleave. So in-memory state is always consistent after link creation completes.

---

### What the KB says about crash consistency

**Durability is session-level, not operation-level** [SS-DURABILITY-BOUNDARY, INV-DURABILITY-BOUNDARY]. After a crash, only crums previously evicted by the grim reaper survive. Recent in-memory state is lost. If the crash occurs before any crum is evicted:

- All three link-creation changes are lost together — no inconsistency, the link simply never happened from the disk's perspective.

But the grim reaper complicates things. It evicts crums based on age across all enfilades indiscriminately [SS-CACHE-MECHANISM, INT-CROSS-ENFILADE-EVICTION]:

> "Memory pressure from one subsystem (e.g., a large link search loading many spanfilade crums) can evict modified crums from another subsystem (e.g., recently inserted text atoms)."

This means a granf crum containing the link orgl could be evicted and written to disk while the corresponding spanf crum (holding the endset index) has not yet been evicted. A crash at that point leaves the link orgl on disk but the endset indexing absent.

**`writeenfilades()` on clean exit introduces the same gap** [EC-CRASH-MID-WRITE]:

> "A crash between these two writes leaves the granfilade updated but the spanfilade stale — violating the cross-enfilade consistency invariant."

The function writes granf root then spanf root sequentially, with no atomic commit.

---

### The KB's explicit acknowledgment

[INV-DUAL-ENFILADE-CONSISTENCY] states directly:

> "there is no transactional mechanism documented — if the sequence is interrupted partway, the enfilades can desynchronize."

The resulting state matches a **reverse orphan** [EC-REVERSE-ORPHAN]: the link orgl is accessible directly by link ID via `follow_link` (because I-space is intact), but `find_links` cannot discover it (because the spanf index entry is missing). Unlike a standard reverse orphan created by `DELETEVSPAN(2.x)`, this one cannot be fixed by normal operations — there is no `insertspanf` that a caller can invoke to repair the index.

---

### Summary

| Threat | Protected? | Mechanism |
|--------|-----------|-----------|
| Race between sessions | Yes | Single-threaded event loop [INV-SEQUENTIAL-DISPATCH] |
| Partial `insertendsetsinspanf` within a session | Yes | Run-to-completion atomicity [INV-ATOMICITY] |
| Grim reaper evicting granf before spanf | **No** | Shared age-based eviction, no cross-enfilade ordering [INT-CROSS-ENFILADE-EVICTION] |
| Crash between granf/spanf writes at exit | **No** | Sequential writes, no fsync, no transaction log [EC-CRASH-MID-WRITE] |

There is no mechanism — no write ordering, no journal, no checksum, no startup validation [EC-NO-STARTUP-VALIDATION] — that guarantees spanfilade completeness after a crash. A link can exist permanently in the granfilade yet be undiscoverable via content-identity search.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Spanfilade Completeness: No Guarantee

There is no mechanism in udanax-green that guarantees every link's endset I-spans are fully indexed in the spanfilade. Multiple distinct failure paths can permanently leave a link's orgl in the granfilade with no corresponding spanfilade entries, making it undiscoverable via `findlinksfromtothreesp`.

---

### The `docreatelink` Call Sequence

The authoritative entry point is `docreatelink` in `do1.c:195-221`:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, ...)
{
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)   // 1. Creates orgl in granfilade
      && tumbler2spanset (...)
      && findnextlinkvsa (...)
      && docopy (...)                                             // 4. Copies link ISA into doc POOM
      && findorgl (...)
      && specset2sporglset (x3)
      && setlinkvsas (...)
      && insertendsetsinorgl (...)                               // 8. Endsets into link's own orgl
      && insertendsetsinspanf (...)                              // 9. Endsets indexed in spanfilade
    );
}
```

Step 1 (`createorglingranf`) and step 9 (`insertendsetsinspanf`) are separated by seven independent operations. There is no rollback if anything between them fails.

---

### Failure Mode 1: `insertspanf` Always Returns TRUE

`insertspanf` at `spanf1.c:51` calls `insertnd` but **discards its return value**:

```c
// spanf1.c:51
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

Then at `spanf1.c:53`:

```c
return (TRUE);
```

This is unconditional. `insertspanf` always returns `TRUE` regardless of whether `insertnd` actually succeeded. `insertendsetsinspanf` (`do2.c:116-128`) therefore cannot detect a failed index insertion:

```c
bool insertendsetsinspanf(...){
    bool insertspanf();
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)   // always TRUE
        && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))  // always TRUE
        return (FALSE);   // unreachable via normal control flow
    ...
    return(TRUE);
}
```

If `insertnd` silently fails inside any of those three `insertspanf` calls, `docreatelink` returns `TRUE` to its caller, the FEBE layer sends success to the client, but some or all of the endset I-spans are not indexed.

---

### Failure Mode 2: Partial `insertendsetsinspanf` via Abort

`qerror` is defined in `genf.c:546-551`:

```c
INT qerror(char *message)
{
    fprintf (stderr, "Error: %s\n",message);
    abort();        // genf.c:549 — terminates immediately
    return(1);
}
```

And `gerror` is a macro alias: `common.h:119: #define gerror(s) qerror(s)`.

Every disk error path (`disk.c:221`, `disk.c:334`) and enfilade integrity check calls `qerror`, which calls `abort()`. If this fires during the first of the three `insertspanf` calls (e.g., LINKFROMSPAN written, LINKTOSPAN not yet started), the process dies instantly without calling `writeenfilades`. The in-memory state is lost — **but so was any chance of rollback**. Whether this leaves the on-disk state corrupted depends on whether `writeenfilades` had been called before the abort:

- If the in-memory dirty state was not yet flushed: consistent loss (both granf and spanf at their last clean state).
- If `writeenfilades` was in progress at the time of abort: see Failure Mode 3.

---

### Failure Mode 3: Crash During `writeenfilades`

`writeenfilades` at `corediskout.c:68-88` writes granfilade and spanfilade **sequentially** to two fixed disk locations:

```c
int writeenfilades(void)
{
    temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
    ...
    orglwrite (&temporgl);   // corediskout.c:79 — writes granfilade to disk

    temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
    ...
    orglwrite (&temporgl);   // corediskout.c:87 — writes spanfilade to disk
}
```

`GRANFDISKLOCATION` and `SPANFDISKLOCATION` are separate fixed block positions (`coredisk.h:119-120`). There is no atomicity between these two `orglwrite` calls — no shadow paging, no WAL, no atomic rename.

If a signal arrives between line 79 and line 87 (e.g., SIGHUP triggers `crash()` at `socketbe.c:186-194`), the crash handler does:

```c
void crash(int signum)
{
    for (i = 0; i < 32; i++)
        close(i);   // socketbe.c:191 — no writeenfilades
    exit(9);        // socketbe.c:193
}
```

On restart, `initkluge` at `corediskin.c:18-41` reads both structures back from their fixed locations:

```c
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
inorgl (tempcbc);   // reads granfilade — newer version, with link orgl
...
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
inorgl (tempcbc);   // reads spanfilade — older version, without endset entries
```

**Result**: The granfilade contains the link's orgl. The spanfilade has no entries for its endsets. The link is permanently undiscoverable. There is no cross-validation step in `initkluge` and no repair scan anywhere in the codebase.

---

### Failure Mode 4: Mid-Sequence `docreatelink` Failure

If any step between `createorglingranf` (step 1) and `insertendsetsinspanf` (step 9) returns FALSE — e.g., `specset2sporglset` fails — `docreatelink` returns FALSE and `fns.c:111` calls `putrequestfailed`. The client is told the operation failed. But the in-memory granfilade has already been modified by `createorglingranf`. On the next `writeenfilades`, the orphan link orgl is flushed to disk with no spanfilade entries.

There is no compensating step, no orgl deletion on failure, no task-scoped rollback.

---

### No Recovery Mechanism

The persistence model (`disk.c`) uses raw `lseek`/`write` to `enf.enf`:

```c
// disk.c:328-334
if (lseek (enffiledes, (long) diskblocknumber*NUMBYTESINLOAF, 0) < 0) { ... }
if (write (enffiledes, (char*)loafptr, sizeof(*loafptr)) <= 0) { ... }
```

There is no write-ahead log, no journal, no fsync ordering guarantee, and no shadow copy with atomic rename. `diskflush` (`corediskout.c:58-64`) simply calls `writeenfilades` and re-initializes the in-core tree; it does not provide any transactional guarantee.

The `cashedisk.c` hash cache is compiled but disabled — `writethruhash` is commented out in `disk.c:305`:

```c
/**writethruhash(loafptr,diskblocknumber);*/   // disk.c:305
```

---

### Summary Table

| Failure Scenario | Granfilade State | Spanfilade State | Outcome |
|---|---|---|---|
| `insertnd` fails silently inside `insertspanf` | Link orgl present | Endset(s) not indexed | Link permanently undiscoverable; `docreatelink` returns TRUE |
| `qerror`/`abort()` during `insertendsetsinspanf` | Dirty in memory | Dirty in memory | Both lost if abort before flush; consistent but data lost |
| Crash between `orglwrite(granf)` and `orglwrite(spanf)` in `writeenfilades` | Flushed to disk (new) | Not flushed (old) | Permanent orgl/spanf divergence after restart |
| `docreatelink` fails mid-chain after `createorglingranf` | Orphan orgl in memory → flushed on next `writeenfilades` | No entries | Link permanently undiscoverable |
| Clean process crash (SIGPIPE) before any `writeenfilades` | At last clean checkpoint | At last clean checkpoint | Consistent; session changes lost but no divergence |

**Conclusion**: The spanfilade can be left permanently incomplete by any of the above paths. The most structurally concerning is the unconditional `return (TRUE)` in `insertspanf` (`spanf1.c:53`), which severs the error-propagation chain entirely and makes silent spanfilade omissions invisible to all callers. The sequential (non-atomic) write of the two enfilades in `writeenfilades` (`corediskout.c:79,87`) provides the second structural gap that a mid-flush crash exploits to create permanent orgl/spanf divergence.
