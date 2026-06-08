## Question 16 [evidence]

> Does INSERT create exactly one DOCISPAN entry in the spanfilade per contiguous I-span, and are all prior spanfilade entries preserved (write-only)?

## KB Synthesis

**Yes to both, with important precision on each.**

---

## INSERT creates exactly one DOCISPAN entry per contiguous I-span

The call chain is: `doinsert` → `inserttextingranf` (allocates one contiguous I-address range) → `docopy` → `insertspanf(..., DOCISPAN)`. Because `inserttextingranf` always returns a single contiguous `ispanset`, `insertspanf` makes exactly one `insertnd` call [SS-DOCISPAN Finding 0047, ST-INSERT Finding 0036].

Formally: `INSERT(doc, k_bytes) → |new_DOCISPAN_entries| = 1`, regardless of byte count. Ten bytes or one byte, it's one I-span, one entry [ST-INSERT Finding 0047].

For sequential single-character inserts, the same holds per-operation: each allocates contiguous I-addresses (monotonically appended), so each individual insert produces one entry [INV-MONOTONIC, SS-DOCISPAN Finding 0047].

**Critical exception:** APPEND (`doappend`) has the `insertspanf(..., DOCISPAN)` call explicitly commented out — content added via APPEND is **not discoverable** via `find_documents` [EC-APPEND-NO-DOCISPAN].

---

## All prior spanfilade entries are preserved — the spanfilade is strictly write-only

No deletion function exists anywhere in `spanf1.c` or `spanf2.c`. Only insertion and query functions are present [INV-SPANF-WRITE-ONLY Finding 0057].

DELETE (`dodeletevspan`) calls only `deletevspanpm` → `deletend` (POOM/granf only) and `logbertmodified` — **no spanf call whatsoever** [ST-DELETE Finding 0057]. Prior DOCISPAN entries survive intact.

The structural invariant: `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)` — monotonically non-decreasing [INV-SPANF-WRITE-ONLY].

This produces a **permanent divergence** between the POOM and spanfilade after DELETE: the spanfilade continues to assert a document contains I-addresses whose V-to-I mappings have been removed. FIND_DOCUMENTS consequently returns a superset of documents currently containing the queried I-addresses [EC-STALE-SPANF-REFERENCE, INT-DELETE-SPANF-DIVERGENCE].

Multiple INSERTs accumulate independently — later inserts never disturb earlier DOCISPAN entries [INV-INSERT-ACCUMULATE].

---

## Code Exploration

I now have all the information needed. Here is the complete answer.

---

## Does INSERT Create Exactly One DOCISPAN Per Contiguous I-Span, and Is the Spanfilade Write-Only?

**Yes to both — with one important nuance on the first question.**

---

### Execution Path from Protocol to Spanfilade

**Step 1: `fns.c:84–98` — `insert()`**

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);
    if (!doinsert (taskptr, &docisa, &vsa, textset))
        ...
}
```

`insert()` immediately ACKs the client and dispatches to `doinsert`.

---

**Step 2: `do1.c:87–123` — `doinsert()`**

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    typespanset ispanset;
    ...
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

Two stages: allocate text in the granfilade (producing an I-span set), then map that I-span into the document's V-space and record it in the spanfilade.

---

**Step 3: `granf1.c:44–46` → `granf2.c:83–109` — `inserttextingranf()` / `inserttextgr()`**

`inserttextingranf` is a thin wrapper (confirmed at `granf1.c:44-46`) that calls `inserttextgr`:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
        return (FALSE);
    movetumbler (&lsa, &spanorigin);                         // record start
    for (; textset; textset = textset->next) {
        ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
        tumblerincrement (&lsa, 0, textset->length, &lsa);  // advance sequentially
    }
    ispanptr = (typeispan *) taskalloc (taskptr, sizeof(typeispan));
    ispanptr->itemid = ISPANID;
    ispanptr->next = NULL;
    movetumbler (&spanorigin, &ispanptr->stream);
    tumblersub (&lsa, &spanorigin, &ispanptr->width);       // width = total run
    *ispansetptr = ispanptr;
    return (TRUE);
}
```

**Critical observation:** regardless of how many `textset` segments exist, `inserttextgr` places them all sequentially in the permascroll starting from a single `spanorigin`, then constructs **exactly one `typeispan`** whose `stream` is `spanorigin` and `width` is the total cumulative extent (`lsa - spanorigin`). The `next` pointer is set to `NULL`. This is a single-element list — one contiguous I-span, always.

---

**Step 4: `do1.c:45–65` — `docopy()`**

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    typeispanset ispanset;
    ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // POOM: V→I mapping
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) // spanfilade
    && asserttreeisok(docorgl)
    );
}
```

`specset2ispanset` at `do2.c:24` passes through ISPANID items directly:

```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
}
```

So the single I-span from `inserttextgr` arrives at `insertspanf` intact and unchanged.

---

**Step 5: `spanf1.c:15–54` — `insertspanf()`**

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    ...
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
    tumblerclear (&crumwidth.dsas[ORGLRANGE]);
    clear (&linfo, sizeof(linfo));
    for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
        if (((typeitemheader *)sporglset)->itemid == ISPANID) {
            movetumbler (&((typeispan *)sporglset)->stream, &lstream);
            movetumbler (&((typeispan *)sporglset)->width, &lwidth);
            movetumbler (isaptr, &linfo.homedoc);
        } ...
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    }
    return (TRUE);
}
```

The loop runs **once** (the sporglset from `inserttextgr` is a single-element list). `insertnd` is called once with the one I-span as the SPANRANGE key, and the document ISA prefixed into the ORGLRANGE key.

---

**Step 6: `insertnd.c:62–66` + `insertnd.c:185–197` — dispatch to `insertcbcnd`**

For SPAN-type enfilades (`insertnd.c:62`):

```c
case SPAN:
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
```

`doinsertnd` (`insertnd.c:185–197`) routes to either:
- `firstinsertionnd` if the enfilade is empty (no new crum: sets values on the existing blank bottom crum)
- `insertmorend` → `insertcbcnd` otherwise

---

**Step 7: `insertnd.c:242–275` — `insertcbcnd()` — the extension test**

```c
INT insertcbcnd(typecuc *father, typedsp *grasp, typewid *origin,
                typewid *width, type2dbottomcruminfo *infoptr)
{
    ...
    for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
        if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
            dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // widen existing
            ivemodified (ptr);
            ...
            return(FALSE);
        }
    }
    // No extension: create a brand new bottom crum
    new = createcrum (0, (INT)father->cenftype);
    reserve (new);
    adopt (new, SON, (typecorecrum*)father);
    ...
}
```

`isanextensionnd` (`insertnd.c:301–309`) returns TRUE when:

1. `infoptr->homedoc` equals the existing crum's `c2dinfo.homedoc` — same document ISA
2. `reach` (the end address of the existing crum) equals `origin` — the new I-span is contiguous

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

---

### Direct Answer

**On "exactly one DOCISPAN entry per contiguous I-span":**

- `inserttextgr` (`granf2.c:95–108`) **always produces one I-span** for a single INSERT operation, covering all text segments contiguously in the permascroll.
- `insertspanf` calls `insertnd` exactly once for this single I-span.
- `insertcbcnd` may then either:
  - **Extend an existing bottom crum** (if the new I-span abuts the end of a prior entry for the same document) — no new entry is created; the existing crum's `cwid` is widened by `dspadd` at `insertnd.c:251`
  - **Create a new bottom crum** (`createcrum` + `adopt` at `insertnd.c:260–262`) — if the new I-span is not contiguous with any existing entry

So the invariant is: **one spanfilade insertion call per INSERT operation, but the result is one new entry OR widening of an existing contiguous entry.** The number of distinct bottom crums in the spanfilade grows by 1 only when the permascroll allocation is non-contiguous with what's already there.

**On write-only preservation of prior entries:**

The spanfilade is **strictly append/extend during INSERT**. The only mutation `insertcbcnd` applies to an existing crum is `dspadd(&ptr->cwid, width, &ptr->cwid, ...)` at `insertnd.c:251` — a monotonic widening of the I-range covered. No existing crum is removed, overwritten with different data, or narrowed. The POOM is updated by `insertpm`, but the spanfilade entries accumulate without deletion. The design is write-only for INSERT: prior DOCISPAN entries are preserved.
