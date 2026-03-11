## Question 12 [gregory]

> What state is initialized when a new document is created — is the POOM created empty (zero-height tree), or is there a sentinel entry, and are any granfilade or spanfilade entries written at creation time before any INSERT?

## KB Synthesis

## Document Creation: Initial State

### POOM State

A newly created document's POOM is **not** a zero-height tree. `createenf(POOM)` produces a minimal height-1 tree with a sentinel bottom node [SS-ENFILADE-TREE]:

- Fullcrum: `isapex=TRUE`, `height=1`, `numberofsons=1`
- One bottom crum: `height=0`, zero width, `infotype=GRANNULL`
- Root-level `cdsp=0`, `cwid=0`

This sentinel bottom crum is structurally critical. Finding 0058 documents that the "never-filled" state and the "deleted-everything" state are **not equivalent**: after delete-everything, `levelpull` (disabled) never collapses the tree, so no bottom crum exists at all. Subsequent INSERT or VCOPY into a deleted-everything document crashes because `firstinsertionnd()` calls `findleftson()` which returns NULL — it assumes a bottom crum always exists. A freshly created document satisfies this assumption; a deleted-empty document does not [EC-EMPTY-DOC].

### Granfilade

Yes — one granfilade entry is written at creation time: the document orgl itself, allocated via `createorglingranf` → `findisatoinsertnonmolecule`. This assigns the document its address in the hierarchical granfilade tree. No content I-addresses are allocated at this point [SS-ADDRESS-ALLOC, ST-ADDRESS-ALLOC].

### Spanfilade

No spanfilade entries are written at creation time for an empty document:

- **DOCISPAN entries** are created only during INSERT and COPY operations [ST-INSERT, SS-DOCISPAN]
- **Link index entries** are created only during CREATELINK [ST-CREATE-LINK]

CREATENEWVERSION is the exception: it additionally calls `docopyinternal` → `insertspanf` to copy the source document's content mappings into the spanfilade [ST-VERSION]. But for a bare CREATEDOCUMENT, the spanfilade is untouched.

### Summary

| Layer | State after CREATEDOCUMENT |
|-------|---------------------------|
| POOM | Height-1 tree, 1 sentinel zero-width bottom crum |
| Granfilade | One orgl entry (document address allocation) |
| Spanfilade | Empty — no DOCISPAN, no link entries |

---

## Code Exploration

I now have everything I need to give a complete, fully-cited answer. Here it is.

---

## What State Is Initialized When a New Document Is Created

### The Call Chain

**`fns.c:276–286`** — `createnewdocument()` calls `docreatenewdocument()`, then puts the response.

**`do1.c:234–241`** — `docreatenewdocument()` does exactly two things:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

That's it. No INSERT, no copy, no spanfilade call — only `makehint` + `createorglingranf`.

---

### What `createorglingranf` Does

**`granf1.c:50–55`** — thin wrapper that calls `createorglgr`.

**`granf2.c:111–128`** — `createorglgr`:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;
  ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);      // ← creates the POOM
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);          // ← writes to granfilade
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

Steps:
1. Computes the new document's ISA address via `findisatoinsertgr`.
2. Calls `createenf(POOM)` — creates the POOM.
3. Writes a single `GRANORGL` bottom-crum entry into the granfilade (`granf`) at the new ISA address, pointing at the fresh POOM. `diskorglptr.diskblocknumber = DISKPTRNULL` means it's in-core only, not yet on disk.

---

### What `createenf(POOM)` Creates — The POOM Structure

**`credel.c:492–516`** — `createenf`:

```c
typecuc *createenf(INT enftype)
{
  typecuc *fullcrumptr;
  typecorecrum *ptr;

    fullcrumptr = (typecuc *) createcrum(1, enftype);   // height-1 apex
    fullcrumptr->cenftype = enftype;
    fullcrumptr->isapex = TRUE;
    fullcrumptr->isleftmost = TRUE;
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);  // one bottom crum
    if (enftype == GRAN) {
        ((typecbc *)ptr)->cinfo.infotype = GRANNULL;  // GRAN only — not POOM
    }
    ivemodified (ptr);
    return (fullcrumptr);
}
```

For `POOM` the `if (enftype == GRAN)` branch is **not taken**. The POOM bottom crum is not given a `GRANNULL` sentinel or any special marker.

**`credel.c:541–596`** — `createcruminternal` (called by `createcrum`) shows what happens to the bottom crum:

```c
ptr->height = crumheight;           // 0
ptr->isapex = FALSE;
ptr->cenftype = enftype;            // POOM
ptr->modified = TRUE;
ptr->isleftmost = FALSE;
ptr->age = NEW;
ptr->leftbroorfather = NULL;
ptr->rightbro = NULL;
clear(&ptr->cdsp, sizeof(ptr->cdsp));   // all zeros
clear(&ptr->cwid, sizeof(ptr->cwid));   // all zeros
...
// For POOM/SPAN height-0 crum:
clear(&((type2dcbc *)ptr)->c2dinfo, sizeof(((type2dcbc *)ptr)->c2dinfo));  // all zeros
```

**The freshly-created POOM has:**
- Height = 1 (one-level enfilade: one upper crum (the apex/fullcrum) + one bottom crum beneath it)
- The single bottom crum (`type2dcbc`) has `cwid = 0`, `cdsp = 0`, and `c2dinfo = 0` — it is all-zero structural scaffolding, **not a content sentinel**
- **Not** a zero-height tree — the height is 1, but the bottom crum carries no content and has zero width

---

### The "Emptiness" Predicate

**`genf.c:97–116`** — `isemptyenfilade` on a POOM:

```c
case POOM :
    return (
       iszerolock(ptr->cwid.dsas, (unsigned)widsize(ptr->cenftype))
    && iszerolock(ptr->cdsp.dsas, (unsigned)dspsize(ptr->cenftype)));
```

Both `cwid` and `cdsp` are zero on the freshly created fullcrum — so `isemptyenfilade` returns **TRUE**.

**`orglinks.c:539–544`** — `isemptyorgl` (called by `doretrievedocvspanset`):

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((typecuc*)((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

Same test. Used at **`do1.c:330–332`**:

```c
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```

So a freshly created document returns an empty vspanset from `RETRIEVE_DOC_VSPAN_SET`.

---

### No Spanfilade Entries at Creation Time

`docreatenewdocument` never calls `insertspanf`, `insertnd`, or any spanfilade function. Contrast this with `docopy` [`do1.c:53–65`] and `docreatenewversion` [`do1.c:260–299`], both of which explicitly call `insertspanf` after inserting content. The spanfilade is only written when content (text or link references) is placed into the document.

---

### Summary

At `CREATENEWDOCUMENT`, the following and **only** the following state is initialized:

| Structure | What is written |
|-----------|----------------|
| **Granfilade (`granf`)** | One `GRANORGL` bottom-crum entry at the new document's ISA address. Points to the new POOM. `diskorglptr = DISKPTRNULL` (in-core only). |
| **POOM** | Height-1 enfilade: one apex (`typecuc`, `isapex=TRUE`) + one bottom crum (`type2dcbc`, all fields zero). Both `cwid` and `cdsp` are all-zero. `isemptyorgl()` → TRUE. |
| **Spanfilade (`spanf`)** | **Nothing.** No entries written. |
| **Content (permascroll atoms)** | **Nothing.** No text, no links. |

The POOM is **not** a zero-height tree — it has a height-1 apex plus one all-zero bottom crum — but it IS functionally empty by the `isemptyenfilade`/`isemptyorgl` tests, which check that all widths are zero. There is no sentinel content entry; the bottom crum is unavoidable structural scaffolding that `createenf` always installs (the enfilade is never truly height-0). First content insertion hits the `isemptyenfilade` branch in `doinsertnd` [`insertnd.c:191–193`], which routes to `firstinsertionnd` to overwrite that bottom crum with real content rather than creating a new one.
