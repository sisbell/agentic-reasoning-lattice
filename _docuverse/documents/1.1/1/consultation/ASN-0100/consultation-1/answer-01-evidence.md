## Question 1 [evidence]

> Does udanax-green implement INSERT as a single atomic operation or as a sequence of lower-level allocation/extension/retraction/provenance steps, and what guarantees its atomicity?

## KB Synthesis

## INSERT: Compound Operation, Structurally Atomic

INSERT is a **sequence of lower-level steps**, but their atomicity is **guaranteed by the single-threaded run-to-completion event loop**.

### The Internal Sequence

INSERT decomposes into four distinct sub-operations [ST-INSERT Finding 0036]:

1. **I-address allocation** — `findisatoinsertmolecule` queries the granfilade tree for the current maximum and increments by 1 to allocate fresh I-addresses [SS-ADDRESS-SPACE Finding 0061]
2. **Granfilade update** — `inserttextingranf` writes text bytes to the permascroll at the allocated addresses
3. **POOM update** — `insertpm` → `insertnd` → `makegappm` constructs the two-blade knife, shifts existing entries in the bounded region `[blade[0], blade[1])`, and either extends an existing crum or creates a new one [SS-TWO-BLADE-KNIFE Finding 0054, ST-INSERT Finding 0062]
4. **Spanfilade update** — `insertspanf(..., DOCISPAN)` creates one index entry per contiguous I-span, making the content discoverable via `find_documents` [SS-DOCISPAN Finding 0047]

### What Guarantees Atomicity

The `bed.c` event loop uses **run-to-completion scheduling** [INV-ATOMICITY Finding 0042]:

> `xanadu(&task)` executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`. There are no threads, no state-modifying signal handlers, and no preemption.

No other FEBE request can execute between steps 1–4. Any concurrent session's view of system state sees either the complete pre-INSERT state or the complete post-INSERT state.

### Two Caveats

**Response ordering** [EC-RESPONSE-BEFORE-CHECK Finding 0050]: For INSERT, `putinsert()` (the success response) is sent to the frontend *before* `doinsert()` executes. If the BERT check fails internally, the frontend has already received success while the document is unchanged. The atomicity guarantee applies to the internal steps relative to each other — not to the response relative to state change.

**Durability** [SS-DURABILITY-BOUNDARY Finding 0059]: After INSERT, the new content is retrievable from the in-memory cache but is **not durably written to disk** until session exit (`writeenfilades()`) or grim reaper eviction. A crash after INSERT returns success but before `writeenfilades()` loses the data. The postcondition `RETRIEVE(addr) = text` holds; `crash(); restart(); RETRIEVE(addr) = text` does not.

### Summary

| Property | Status |
|----------|--------|
| Single atomic opcode? | No — four internal sub-steps |
| Atomic vs. other sessions? | Yes — run-to-completion event loop |
| Atomic vs. frontend response? | No — response sent before execution |
| Durable after completion? | No — session-level durability only |

---

## Code Exploration

I have everything needed for a complete answer. Let me write it up.

---

## Does udanax-green implement INSERT as a single atomic operation?

**Short answer:** INSERT is a four-phase sequence of lower-level mutations, not a single indivisible primitive. What approximates atomicity is the single-threaded event loop combined with a process-killing error handler — not any transaction or rollback mechanism.

---

### The Call Chain

#### Phase 0 — FEBE handler: reply before work

`fns.c:84–98`, `insert()`:

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);                          /* RESPONSE SENT HERE */
    if (!doinsert (taskptr, &docisa, &vsa, textset))
        fprintf(stderr,"requestfailed in insert\n");  /* silently dropped in DISTRIBUTION */
}
```

This is the first atomicity gap: the client receives the success reply *before* the actual work is performed. In `DISTRIBUTION` builds the `#else` branch is `;` — errors after the `put` are swallowed silently. (By contrast, `copy`, `createlink`, and query operations use the safer `if (get... && do...) put... else putrequestfailed` pattern — `fns.c:35–46`, `fns.c:100–111`.)

---

#### Phase 1 — Permascroll allocation

`do1.c:87–123`, `doinsert()`:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset));
    return(ret);
}
```

`inserttextingranf` (`granf1.c:44`) delegates immediately to `inserttextgr` (`granf2.c:83`):

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  /* writes text into granfilade */
        tumblerincrement (&lsa, 0, textset->length, &lsa);
    }
    /* build and return the ispan (I-space address range) */
    ispanptr->stream = spanorigin;
    tumblersub (&lsa, &spanorigin, &ispanptr->width);
    *ispansetptr = ispanptr;
    return (TRUE);
}
```

`findisatoinsertgr` (`granf2.c:130`) first verifies the parent document exists (`isaexistsgr`), then calls `findisatoinsertmolecule` (`granf2.c:158`) which does a `findpreviousisagr` scan to find the next unused ISA. The address is computed, justified, and returned. Text is written block-by-block via `insertseq`.

At the end of Phase 1, the text bytes live in the granfilade at a fresh permascroll address. The document's virtual space does not yet reference them.

---

#### Phase 2 — POOM tree mutation

`doinsert` then calls `docopy` (`do1.c:45–65`):

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* POOM mutation */
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) /* spanfilade update */
    && asserttreeisok(docorgl));
}
```

`insertpm` (`orglinks.c:75–134`):

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    ...
    logbertmodified(orglisa, user);   /* mark document modified in session table */
    for (; sporglset; sporglset = ...) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        movetumbler (&lstream, &crumorigin.dsas[I]);
        movetumbler (vsaptr, &crumorigin.dsas[V]);
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  /* advance V cursor */
    }
    return (TRUE);
}
```

`insertnd` (`insertnd.c:15`) is the enfilade node insertion engine. For POOM trees it:
1. Calls `makegappm` (`insertnd.c:124`) to **split** existing nodes at the insertion point — this is the "gap-making" step that shifts the V-addresses of all content to the right of the insert point. `makegappm` calls `makecutsnd` to introduce cut-planes, then `insertcutsectionnd` walks children and adjusts `cdsp` displacements (`insertnd.c:162–163`).
2. Calls `doinsertnd` → `insertmorend` → `insertcbcnd` to walk the tree and either **extend** an adjacent bottom crum (if the insert is an extension, `isanextensionnd`, `insertnd.c:301`) or **create** a new bottom crum (`createcrum` + `adopt`, `insertnd.c:260–263`).
3. Calls `recombine` (`insertnd.c:76`) to merge overfull crums and rebalance the tree.
4. Marks touched crums dirty: `ivemodified(ptr)` — which sets `ptr->modified = TRUE` on the crum and walks up to the root (`genf.c:538–542`).

---

#### Phase 3 — Spanfilade update

Back in `docopy`, after `insertpm`, comes `insertspanf` (`spanf1.c:15`):

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
    for (; sporglset; sporglset = ...) {
        ...
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    }
    return (TRUE);
}
```

This records the (I-address → document) mapping in the global spanfilade, enabling later link resolution queries (`finddocscontaining`, `findlinksfromtothree`).

---

### What Provides Atomicity (Such As It Is)

**1. Single-threaded event loop** (`bed.c:103–148`, `be.c:90–96`):

The event loop processes one FEBE request at a time — a single `select` dispatches to `xanadu()`, which calls the request handler to completion before returning. There is no preemption, no concurrency. No other request can observe a mid-INSERT state.

**2. `gerror()` → `abort()`** (`common.h:119`, `genf.c:546–550`):

```c
#define gerror(s) qerror(s)

INT qerror(char *message) {
    fprintf (stderr, "Error: %s\n", message);
    abort();
    return(1);
}
```

Any structural invariant violation during tree mutation — zero width in `insertnd`, bad enfilade type, null POOM pointer — calls `gerror`, which calls `abort()`. The process dies rather than leaving a corrupt half-done structure visible to subsequent requests. This is a crash-consistency guarantee, not a transaction guarantee.

**3. In-memory dirty-write, deferred flush** (`bed.c:105`, `bed.c:134`):

`ivemodified` marks nodes dirty in memory. Disk is only written by `diskflush()` (called when `n_players < 1`, i.e., all users have disconnected) or by `writeenfilades()` at process exit. Within a request there is no disk I/O to the enfilade data — no partial disk state can result from an interrupted INSERT.

---

### What Atomicity Does NOT Cover

There is **no rollback**. If the process crashes after Phase 1 (text written to granfilade) but before Phase 2 (POOM updated), the permascroll ISA is allocated but unreferenced — a permanent orphan. There is no transaction log, no undo, no WAL.

The **response-before-work** design in `fns.c:91–97` means the client has already received `putinsert` success before `doinsert` runs. Any failure in `doinsert` after that point is logged to stderr and silently dropped in DISTRIBUTION builds — the client cannot distinguish success from silent failure.

---

### Summary Table

| Phase | Function | File | What it does |
|---|---|---|---|
| 0 — Reply | `putinsert()` | `fns.c:91` | Sends success to client **before** mutation |
| 1 — Allocation | `inserttextgr()` | `granf2.c:83` | Finds next ISA; writes text bytes into granfilade via `insertseq` |
| 2 — POOM mutation | `insertpm()` → `insertnd()` | `orglinks.c:99`, `insertnd.c:15` | Splits gap via `makegappm`; inserts/extends bottom crum; rebalances via `recombine`; marks dirty via `ivemodified` |
| 3 — Spanfilade update | `insertspanf()` → `insertnd()` | `spanf1.c:51` | Registers I↔document mapping in global spanfilade |

**Atomicity guarantee:** The single-threaded loop makes INSERT appear atomic to other requests. The `gerror → abort()` policy makes it crash-consistent. There is no formal transaction — no rollback, no undo, and the client reply is decoupled from the actual mutation.
