# Revision Consultation — ASN-0006

**Review:** review-4.md
**Date:** 2026-03-06 23:55

## Summary

6 REVISE items analyzed: 5 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 4: AX1 claims universality beyond its evidence

**Category:** GREGORY
**Reason:** Closing the operation set requires confirming that INSERT, DELETE, COPY, CREATENEWVERSION, and MAKELINK are the complete set of mutating FEBE operations — only implementation evidence can verify no other mutating operations exist.

**Gregory question:** Are there any mutating FEBE operations in udanax-green beyond INSERT, DELETE, COPY, CREATENEWVERSION, and MAKELINK that modify a document's POOM?

**Gregory's Answer:**

## KB Synthesis

Yes — you're missing **REARRANGE** (FEBE command 3), and possibly **APPEND**.

## REARRANGE

This is the most significant omission. [SS-POOM-MUTABILITY] explicitly names it alongside INSERT and DELETE:

> "The POOM maps V-addresses to I-addresses and is modified in-place by INSERT (adds new leaf nodes), DELETE (removes and frees leaf nodes), and **REARRANGE (restructures mappings)**."

REARRANGE (pivot/swap) modifies the POOM in-place by adding a computed displacement to the V-address component (`ptr->cdsp.dsas[index]`) of each affected crum [ST-REARRANGE, Finding 0056]. It does not touch I-addresses, the granfilade, or the spanfilade — POOM only. This makes it structurally distinct from INSERT/DELETE (which also touch the granfilade or spanfilade) and from COPY (which also writes DOCISPAN to the spanf).

The subspace isolation consequence is directly tied to REARRANGE's POOM mechanics: it can move content across subspace boundaries via displacement arithmetic without any guard [PRE-REARRANGE, Finding 0051], which is how it can produce the INV-SUBSPACE-CONVENTION violations documented in [EC-REARRANGE-CROSS-SUBSPACE].

## APPEND

APPEND (`doappend`) also modifies the POOM — it calls `appendpm` to add content, which places V→I mappings just as INSERT does. The key distinction from INSERT is that APPEND does **not** write DOCISPAN entries to the spanfilade [FC-APPEND-NO-DOCISPAN]. So APPEND is a POOM-writer with different spanf semantics, not a non-mutating operation.

## Summary

| Operation | POOM | Granfilade | Spanf (link index) | Spanf (DOCISPAN) |
|-----------|------|------------|--------------------|------------------|
| INSERT | Write | Write | No | Write |
| DELETE | Write | No | No | No |
| COPY/VCOPY | Write | No | No | Write |
| CREATENEWVERSION | New POOM | Write (doc addr) | No | Write |
| MAKELINK | Write (2.x) | Write (link orgl) | Write | Write |
| **REARRANGE** | **Write** | **No** | **No** | **No** |
| APPEND | Write | Write | No | **No** |

REARRANGE is the operationally important missing entry — it is the only operation that permutes existing POOM entries in-place without allocation. [SS-POOM-MUTABILITY], [ST-REARRANGE]

---

## Code Exploration

I have enough information to write the complete answer.

---

## Mutating FEBE Operations Beyond INSERT, DELETE, COPY, CREATENEWVERSION, and MAKELINK

### The Complete Dispatch Table

From `backend/init.c:45-69`, all registered FEBE handlers are:

```c
requestfns[INSERT]                    = insert;                    // 0
requestfns[RETRIEVEDOCVSPANSET]       = retrievedocvspanset;       // 1  (read-only)
requestfns[COPY]                      = copy;                      // 2
requestfns[REARRANGE]                 = rearrange;                 // 3  ← NEW MUTATOR
requestfns[RETRIEVEV]                 = retrievev;                 // 5  (read-only)
requestfns[NAVIGATEONHT]              = navigateonht;              // 9  (stub)
requestfns[SHOWRELATIONOF2VERSIONS]   = showrelationof2versions;   // 10 (read-only)
requestfns[CREATENEWDOCUMENT]         = createnewdocument;         // 11 ← POOM-allocating
requestfns[DELETEVSPAN]               = deletevspan;               // 12
requestfns[CREATENEWVERSION]          = createnewversion;          // 13
requestfns[RETRIEVEDOCVSPAN]          = retrievedocvspan;          // 14 (read-only)
requestfns[QUIT]                      = quitxanadu;                // 16
requestfns[FOLLOWLINK]                = followlink;                // 18 (read-only)
requestfns[FINDDOCSCONTAINING]        = finddocscontaining;        // 22 (read-only)
requestfns[CREATELINK]                = createlink;                // 27
requestfns[RETRIEVEENDSETS]           = retrieveendsets;           // 28 (read-only)
requestfns[FINDNUMOFLINKSFROMTOTHREE] = findnumoflinksfromtothree; // 29 (read-only)
requestfns[FINDLINKSFROMTOTHREE]      = findlinksfromtothree;      // 30 (read-only)
requestfns[FINDNEXTNLINKSFROMTOTHREE] = findnextnlinksfromtothree; // 31 (read-only)
requestfns[XACCOUNT]                  = xaccount;                  // 34 (session only)
requestfns[OPEN]                      = myopen;                    // 35 ← conditionally mutating
requestfns[CLOSE]                     = myclose;                   // 36 (bert table only)
requestfns[CREATENODE_OR_ACCOUNT]     = createnode_or_account;     // 38 ← POOM-allocating
requestfns[DUMPSTATE]                 = dumpstate;                 // 39 (diagnostic)
```

---

### Additional Mutating Operations

#### 1. REARRANGE (3) — Directly Modifies an Existing Document's POOM

This is the most significant find. REARRANGE is a full POOM-mutating operation on par with INSERT and DELETE.

**Call chain:**

`fns.c:159-173` → `do1.c:34-43` → `orglinks.c:137-142` → `edit.c:78-160`

```c
// fns.c:159
void rearrange(typetask *taskptr) {
    (void) getrearrange (taskptr, &docisa, &cutseq);
    putrearrange (taskptr);
    if (!dorearrange (taskptr, &docisa, &cutseq)) ...
}
```

```c
// do1.c:34-43
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr) {
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```

```c
// orglinks.c:137-142
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr) {
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` [edit.c:78] takes the document's POOM (passed as `docorgl`) and a `cutseq` (a sequence of V-space cut positions), then physically shifts the `dsas[V]` (dimensional address) of each POOM crum into its new position:

```c
// edit.c:124-128
case 1:  case 2:  case 3:
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

It supports 3-cut and 4-cut rearrangements [edit.c:162-183], computing offsets for each section of content between cut points, then applying them directly to each crum's virtual-space position. This is a structural reordering of the POOM's content map — not creation of new permanent content, but a remapping of the virtual-space layout.

**REARRANGE requires WRITEBERT** [do1.c:40], meaning the document must be open for writing. It calls `logbertmodified` [orglinks.c:140], marking the document as modified.

---

#### 2. CREATENEWDOCUMENT (11) — Allocates a New Empty POOM

**Call chain:** `fns.c:276` → `do1.c:234-241` → `granf1.c:50` → `granf2.c:111-128`

```c
// do1.c:234-241
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr) {
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

```c
// granf2.c:111-128
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr) {
    ...
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // ← creates new POOM enfilade
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        // ← inserts into granfilade
    return (TRUE);
}
```

This **allocates a new empty POOM** for the new document and inserts a reference to it into the granfilade. This is creating new persistent state, but it does not modify any existing document's POOM.

---

#### 3. OPEN (35) — Conditionally Creates a New Version (Populates a New POOM)

**Call chain:** `fns.c:388-401` → `bert.c:264-322`

```c
// bert.c:273-298
bool doopen(typetask *taskptr, tumbler *tp, tumbler *newtp, int type, int mode, int connection) {
    if (mode == BERTMODECOPY) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // ← creates copy
        addtoopen(newtp, connection, TRUE, type);
        return 1;
    }
    openState = checkforopen(tp, type, connection);
    switch (mode) {
    case BERTMODECOPYIF:
        if (openState == -1) {
            docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // ← creates copy
            ...
        }
    }
}
```

When mode is `BERTMODECOPY` or `BERTMODECOPYIF` with write conflict, OPEN calls `docreatenewversion` [do1.c:260-298], which:
1. Allocates a new document ISA in the granfilade (`createorglingranf`)
2. Retrieves the original document's vspan
3. Calls `docopyinternal` to populate the new document's POOM with the original's content

The **original** document's POOM is not modified; the new version's POOM is written. This is POOM-creation, not POOM-mutation of an existing document.

---

#### 4. CREATENODE_OR_ACCOUNT (38) — Allocates a Granfilade Node with a POOM

**Call chain:** `fns.c:375` → `do1.c:243-258` → `granf1.c:50` → `granf2.c:111`

```c
// do1.c:243-258
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    ...
}
```

Same `createorglgr` path as CREATENEWDOCUMENT, but with hint type `NODE`. Creates a namespace/account node in the granfilade with a fresh POOM. This is an administrative operation for namespace management, not document content editing.

---

#### 5. Note: `doappend` Is Not a FEBE Operation

`doappend` exists at `do1.c:25-32` and calls `appendpm` → `doinsert`, which would modify a POOM. However, **there is no request code registered for APPEND** in `init.c`. `doappend` is an internal helper function never directly invoked via the FEBE protocol.

---

### Summary

| Operation | Code | POOM Effect |
|-----------|------|-------------|
| **REARRANGE** | 3 | **Directly modifies an existing document's POOM** — rearranges crum V-space addresses |
| CREATENEWDOCUMENT | 11 | Allocates a new empty POOM for a new document |
| OPEN | 35 | In COPY/COPYIF mode: creates a new document and populates its POOM from original |
| CREATENODE_OR_ACCOUNT | 38 | Allocates a granfilade namespace node with a fresh POOM |

**The answer is yes.** Beyond the five listed operations, **REARRANGE (3)** is an additional mutating FEBE operation that directly modifies a document's POOM. It reorders existing virtual-space content by physically shifting crum dimensional addresses within the POOM enfilade, requiring WRITEBERT access [do1.c:40], and marking the document modified via `logbertmodified` [orglinks.c:140]. The other three operations (CREATENEWDOCUMENT, OPEN, CREATENODE_OR_ACCOUNT) are POOM-allocating rather than POOM-mutating: they write new POOMs for newly created entities rather than modifying the structure of existing documents.
