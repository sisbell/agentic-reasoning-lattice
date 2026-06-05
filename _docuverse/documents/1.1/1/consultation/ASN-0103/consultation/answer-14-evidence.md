## Question 14 [evidence]

> Does CREATEDOCUMENT allocate or pre-create any of the three subspaces (text `1.x`, link `2.x`, type `3.x`), or are they materialized lazily on first INSERT/CREATELINK?

## KB Synthesis

The KB does not describe a dedicated CREATEDOCUMENT code path in detail, but the evidence consistently points to **lazy materialization** of all three subspaces.

**Document creation initializes an empty POOM only**

`createenf(POOM)` produces a height-1 tree with a single zero-width bottom node and no content mappings [SS-ENFILADE-TREE, Finding 0058]. An empty document consequently returns zeros from RETRIEVEDOCVSPAN and NULL from RETRIEVEDOCVSPANSET [SS-VSPAN-VS-VSPANSET, Finding 0035]. No subspace entries exist.

**Subspace 1.x materializes on first INSERT/COPY**

`doinsert` calls `insertpm` targeting `1.x` [ST-INSERT, Findings 0009, 0052]. The two-blade knife in `makegappm` uses `blade[1] = 2.1` as the subspace boundary, but this boundary is computed *at insert time*, not pre-allocated [SS-TWO-BLADE-KNIFE, Finding 0054]. Nothing in `createorglingranf` seeds a text span.

**Subspace 2.x materializes on first CREATELINK**

`findnextlinkvsa` hardcodes the first link position as `2.1`, allocating it only when invoked during link creation [SS-LINK-SUBSPACE, Finding 0052; ST-CREATE-LINK, Finding 0009]. CREATENEWVERSION explicitly skips copying the `2.x` subspace, confirming it is never implicitly present [ST-VERSION-CREATE, Finding 0043].

**Subspace 3.x materializes on first CREATELINK (type endpoint)**

`setlinkvsas()` constructs all three link subspace positions — FROM at `2.x`, TO at `2.x`, THREE (type) at `3.x` — inside `docreatelink` [SS-SUBSPACE-CONVENTION, Finding 0038]. No 3.x entries can exist before any link creation.

**Summary:** CREATEDOCUMENT allocates a document address [SS-ADDRESS-ALLOC, Finding 0021] and an empty POOM via `createenf`. All three subspaces are ghost until first use — text `1.x` on INSERT/COPY, link `2.x` and type `3.x` on CREATELINK.

---

## Code Exploration

All citations verified. Here is the definitive answer:

---

## CREATEDOCUMENT: Lazy Materialization — No Subspaces Pre-Created

**Short answer:** CREATEDOCUMENT creates only an empty POOM enfilade. Subspaces 1.x (text), 2.x (link), and 3.x (type) are materialized lazily on first INSERT or CREATELINK.

---

### Execution Chain (fully verified)

**`fns.c:276–286` — FEBE handler**
```c
void createnewdocument(typetask *taskptr) {
    typeisa newdocisa;
    getcreatenewdocument();
    if (docreatenewdocument(taskptr, &newdocisa))
        putcreatenewdocument(taskptr, &newdocisa);
    else
        putrequestfailed(taskptr);
}
```
Only calls `docreatenewdocument`. No subspace work here.

---

**`do1.c:234–241` — Core implementation**
```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr) {
    typehint hint;
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```
`makehint` is called with `atomtype = 0` — not `TEXTATOM` (1) or `LINKATOM` (2). The hint designates a document container, not a content atom.

---

**`granf1.c:50–55` — Thin wrapper**
```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr) {
    return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

---

**`granf2.c:111–128` — The actual creation**
```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr) {
    typegranbottomcruminfo locinfo;
    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // ← only thing created
    reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);
    rejuvinate((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```
The single allocation is `createenf(POOM)` at `granf2.c:120`. That's it — an empty POOM (Parallel Order-Of-Magnitude) enfilade, registered at the document's ISA in the granfilade.

---

**`credel.c:492–516` — What `createenf(POOM)` actually builds**
```c
typecuc *createenf(INT enftype) {
    fullcrumptr = (typecuc *) createcrum(1, enftype);   // apex crum
    fullcrumptr->isapex = TRUE;
    fullcrumptr->isleftmost = TRUE;
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);  // one empty bottom
    // GRAN branch sets GRANNULL — POOM doesn't even do that
    ivemodified(ptr);
    return (fullcrumptr);
}
```
One apex crum + one empty bottom crum. No tumbler ranges, no subspace addresses, no span initialization.

---

### Where the Subspaces Actually Come From

**Text subspace (1.x)** — first INSERT calls `doinsert()` → `inserttextingranf()` → `inserttextgr()` (`granf2.c`), which inserts content into the POOM at the next available address in the 1.x range.

**Link and type subspaces (2.x, 3.x)** — CREATELINK calls `docreatelink()` (`do1.c:178–221`) which calls:
- `findnextlinkvsa()` (`do2.c:151–167`) — computes the next available VSA by querying the current document span reach and comparing against the floor `2.1`:
  ```c
  tumblerincrement(&firstlink, 0, 2, &firstlink);  // 2.x floor
  tumblerincrement(&firstlink, 1, 1, &firstlink);  // → 2.1
  ```
- `setlinkvsas()` (`do2.c:169–183`) — assigns fixed origin addresses to the link's three endsets:
  ```c
  tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // 1.1 (from-end in text space)
  tumblerincrement(tovsaptr,   0, 2, tovsaptr);     // 2.1 (to-end in link space)
  tumblerincrement(threevsaptr,0, 3, threevsaptr);  // 3.1 (type in type space)
  ```

These addresses are only computed at link-creation time; nothing in the CREATEDOCUMENT path touches them.

---

### Summary

| Subspace | Created by CREATEDOCUMENT? | Actually created by |
|----------|---------------------------|---------------------|
| 1.x text | No | First `INSERT` via `inserttextgr()` |
| 2.x link | No | First `CREATELINK` via `setlinkvsas()` |
| 3.x type | No | First `CREATELINK` (3-endset form) via `setlinkvsas()` |
| POOM enfilade | **Yes** — `createenf(POOM)` at `granf2.c:120` | `docreatenewdocument` |

CREATEDOCUMENT allocates exactly one structure: the POOM enfilade registered at the document's ISA in the granfilade (`granf2.c:120`). All three content subspaces are lazily materialized by subsequent operations that insert actual content.
