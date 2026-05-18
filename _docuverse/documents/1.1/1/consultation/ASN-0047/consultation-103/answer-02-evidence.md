## Question 2 [evidence]

> In udanax-green, when a document is created (`docreatenewdocument`), is any version-sub-allocator state established at that moment, or does the version allocator only become observable when `docreatenewversion` is first invoked on the document?

## KB Synthesis

No version-sub-allocator state is established at document creation time. The version allocator becomes observable only when `docreatenewversion` is first invoked.

**Why:** Version address allocation is stateless query-and-increment against the granfilade tree. When `docreatenewversion` is called on a document `d`, it runs `findpreviousisagr` to find the highest existing address below the upper bound `tumblerincrement(d, 0, 1)`, applies a containment check to verify any found address is actually under `d`, and if **no child exists** allocates `d.1` as the first version [ST-ADDRESS-ALLOC, Finding 0068].

`docreatenewdocument` adds only the document's own address entry to the granfilade. It does not pre-allocate child slots, initialize a counter, or write any version-namespace sentinel. The granfilade simply gains one new entry for the document itself [SS-ADDRESS-ALLOC, Finding 0021].

The version "allocator state" is entirely implicit in the granfilade tree: `next_version_addr(granf, d) = max_child(granf, d) + 1`, evaluated fresh on each call. There is no Σ.next counter, no per-document sub-allocator struct, and no initialization step at document creation [INV-MONOTONIC, Finding 0077; SS-ADDRESS-SPACE, Finding 0061].

**Corollary:** If `docreatenewversion` has never been called on document `d`, `findpreviousisagr` finds nothing under `d`, and the first version receives address `d.1`. The first call to `docreatenewversion` is the moment the version namespace becomes occupied.

---

## Code Exploration

I now have everything I need for a complete, line-cited answer.

---

## Answer: Version-Sub-Allocator State in `docreatenewdocument` vs. `docreatenewversion`

**Short answer:** No version-sub-allocator state is established at `docreatenewdocument` time. The version allocator is only initialized — in two distinct ways — inside `docreatenewversion`.

---

### What `docreatenewdocument` actually does

```c
// do1.c:234-241
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`createorglingranf` → `createorglgr` (granf2.c:111-128) → `createenf(POOM)` (credel.c:492-516). The key allocation is in `createcruminternal`:

```c
// credel.c:580-581
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
```

Every crum — including the root of the new POOM — is initialized with all-zero `cdsp` and `cwid`. For a POOM enfilade, `cdsp.dsas[V]` is the V-dimension displacement (the "version stream base") and `cwid.dsas[V]` is the V-dimension width. After `docreatenewdocument`:

- V-stream = 0 (no allocated version sub-space)
- V-width = 0 (no content)
- **No BERT entry** — `addtoopen` is never called

The document "exists" as an address in the granfilade, but the version coordinate system is completely uninitialized.

---

### What `docreatenewversion` actually does

```c
// do1.c:260-299
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
  typehint hint;
  typevspan vspan;
  typevspec vspec;
  tumbler newtp;
  bool doretrievedocvspanfoo(), createorglingranf();

    // ... hint selection for same-account vs. cross-account ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
        return (FALSE);
    }

    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {   // (1)
        return FALSE;
    }

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);
    vspec.vspanset = &vspan;

    addtoopen(newisaptr, user, TRUE, WRITEBERT);              // (2)
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);// (3)
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);

    return (TRUE);
}
```

Three things happen here that never happen in `docreatenewdocument`:

**Step (1) — Version stream base is read from the source document.**

```c
// do1.c:301-309
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
    && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

```c
// orglinks.c:155-162
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // V-DSP
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // V-WID
    return (TRUE);
}
```

`vspan.stream` = the source document's `cdsp.dsas[V]` — this is the base address in version-space where the new version's content will be allocated.

**Step (2) — The BERT entry is created for the first time.**

```c
// bert.c:13-19
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;
```

`addtoopen(newisaptr, user, TRUE, WRITEBERT)` allocates a `bertentry` and inserts it into `berttable[NUMBEROFBERTTABLE]` (a hash table of 1327 buckets, `bert.c:27-29`). The `created=TRUE` flag marks it as newly created so `removefromopen` won't delete it on close.

This is the first time any BERT access-control record exists for any document associated with this creation chain. Without it, `findorgl(..., WRITEBERT)` — called by every mutating operation including `doinsert` (do1.c:40, do1.c:55, do1.c:164) — returns `FALSE`.

**Step (3) — Content is written, stamping V-DSP and V-WID into the new POOM.**

`docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)` inserts the source document's content into the new POOM, using `vspan.stream` as the version-space origin. This updates `cdsp.dsas[V]` and `cwid.dsas[V]` in the new POOM root from their initial zero values to real V-coordinates.

---

### The structural invariant

Every subsequent write operation checks BERT before proceeding:

```c
// do1.c:39-40  (doinsert)
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
```

```c
// do1.c:164  (dodeletevspan)
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
```

`checkforopen` in `bert.c:55-90` returns `0` (open required) for any document not in the BERT table. Since `docreatenewdocument` never calls `addtoopen`, a freshly created document is inaccessible to all mutation operations until `docreatenewversion` registers it.

---

### Summary

| State | After `docreatenewdocument` | After `docreatenewversion` |
|---|---|---|
| ISA allocated in granfilade | Yes | Yes (new ISA) |
| POOM V-DSP (`cdsp.dsas[V]`) | 0 (`credel.c:580`) | Set from source doc's V-DSP (`orglinks.c:159`) |
| POOM V-WID (`cwid.dsas[V]`) | 0 (`credel.c:581`) | Updated by `docopyinternal` |
| BERT entry in `berttable` | None | Yes (`bert.c:128`, called at `do1.c:292`) |
| Writable via `findorgl(..., WRITEBERT)` | No | Yes (while open) |

The version sub-allocator — the V-dimension coordinates that govern where new content is placed in version-space, and the BERT entry that gates all write access — is entirely absent after `docreatenewdocument`. It is fully established only inside `docreatenewversion`, at lines `do1.c:281-293`.
