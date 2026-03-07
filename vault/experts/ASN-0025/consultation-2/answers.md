# Revision Consultation — ASN-0025

**Review:** review-2.md
**Date:** 2026-03-07 07:35

## Summary

5 REVISE items analyzed: 4 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 1: P3 exhaustiveness claim is ungrounded

**Category:** GREGORY
**Reason:** The preferred fix (adding CREATE DOCUMENT as a seventh operation) requires implementation evidence for `docreatenewdocument`'s exact I-space and V-space effects, parallel to the Gregory confirmations provided for every other operation.

**Gregory question:** What does `docreatenewdocument` allocate in I-space — just a single orgl address via `findisatoinsertnonmolecule`, or additional entries? Is the initial V-space empty, or does it contain a structural entry?

**Gregory's Answer:**

## KB Synthesis

The KB doesn't document `docreatenewdocument` directly, but here's what can be synthesized from related entries:

## I-Space Allocation

A new document creation calls `createorglingranf`, which internally dispatches to `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC, Finding 0021]. That function allocates **exactly one address** — the document's orgl ISA — using the query-and-increment pattern: find the highest existing address under the parent account, increment by 1. No content atoms are allocated because the document starts empty. [SS-ADDRESS-SPACE, Finding 0077] explicitly confirms this pattern: VERSION likewise calls `createorglingranf` for the document address and nothing else for content. A fresh create would be the same or simpler.

No DOCISPAN entries are created — those come only from subsequent INSERT/COPY operations that call `insertspanf(..., DOCISPAN)` [SS-DOCISPAN, Finding 0036]. An empty document has nothing to index.

## Initial V-Space

The initial POOM is created by `createenf(POOM)`, which produces a **minimal height-1 tree with one zero-width bottom node** [SS-ENFILADE-TREE, Finding 0058]:

```
Fullcrum (height=1, isapex=TRUE, numberofsons=1)
  └─ Bottom node (height=0, width=0)
```

This is a structural placeholder, not user content. The 2D enfilade's emptiness is detected by `isemptyenfilade` checking `cdsp = 0 AND cwid = 0` [SS-ENFILADE-TREE, Finding 0066], which this node satisfies.

The zero-width bottom node is significant because it distinguishes a never-filled document from a delete-everything document. After delete-everything, `levelpull` (disabled) would have collapsed the tree, but instead leaves empty intermediate nodes with *no* bottom nodes — and that state causes Bug 0019 (INSERT/VCOPY crash on reinsertion) [EC-EMPTY-DOC, Finding 0058].

## Summary

- **I-space**: One orgl address allocated via `findisatoinsertnonmolecule`. Nothing else.
- **V-space**: Not empty in the tree sense — one structural zero-width bottom node exists — but empty in the content sense (`cwid = 0`, no user content, no DOCISPAN entries).

---

## Code Exploration

I now have everything needed to give the full answer.

---

## What `docreatenewdocument` Allocates

### Call chain

```
fns.c:createnewdocument
  → do1.c:docreatenewdocument
    → granf1.c:createorglingranf
      → granf2.c:createorglgr
        → granf2.c:findisatoinsertgr → findisatoinsertnonmolecule
        → credel.c:createenf(POOM)
        → insert.c:insertseq
```

---

### I-space: exactly one granfilade entry

`docreatenewdocument` [do1.c:234–241]:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

The hint has `supertype=ACCOUNT`, `subtype=DOCUMENT`, `atomtype=0`, anchored to the current user's account tumbler.

Inside `createorglgr` [granf2.c:111–128], `findisatoinsertgr` [granf2.c:130] is called. Since `hintptr->subtype == DOCUMENT` (not `ATOM`), it takes the `else` branch [granf2.c:143–152]:

```c
} else {
    findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
}
```

`findisatoinsertnonmolecule` [granf2.c:203–241] uses `depth=2` (because `ACCOUNT ≠ DOCUMENT`, so `supertype ≠ subtype` [granf2.c:209]):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

It calls `findpreviousisagr` to find the highest existing document address under the account, then either:
- **First document**: `tumblerincrement(&hintptr->hintisa, depth, 1, isaptr)` → yields `account.0.1` [granf2.c:237]
- **Nth document**: truncates the previous entry and increments → yields `account.0.N` [granf2.c:239–240]

Back in `createorglgr`, **exactly one** granfilade entry is created and inserted [granf2.c:119–125]:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // fresh V-space enfilade
reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);       // one entry in the granfilade
```

**`findisatoinsertmolecule` is never called** here — that path is only for `ATOM` subtypes (text and link content insertion).

**Total I-space allocation: one `GRANORGL` crum** in the granfilade at the computed document address.

---

### V-space: empty at creation

The orgl is `createenf(POOM)` [credel.c:492–516]. `createcruminternal` [credel.c:541] explicitly zeroes both the displacement and width arrays on every new crum [credel.c:580–581]:

```c
clear(&ptr->cdsp, sizeof(ptr->cdsp));   // all displacements → 0
clear(&ptr->cwid, sizeof(ptr->cwid));   // all widths → 0
```

`clear` is `memset(ptr, 0, count)` [common.h:162]. So the new POOM root apex has `cdsp.dsas[V] = 0` and `cwid.dsas[V] = 0`.

`createenf` builds the minimal valid enfilade [credel.c:497–501]:
- One height-1 apex crum (the root)
- One height-0 leaf crum adopted as SON

For POOM type, **no infotype initialization is performed** on the leaf (contrast with GRAN where [credel.c:503]: `((typecbc*)ptr)->cinfo.infotype = GRANNULL`). The POOM leaf is bare zeros.

This is directly observable through `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    movetumbler(&((typecuc*)orgl)->cdsp.dsas[V], &vspanptr->stream);  // → 0
    movetumbler(&((typecuc*)orgl)->cwid.dsas[V], &vspanptr->width);   // → 0
    return TRUE;
}
```

A freshly created document returns `stream=0, width=0` — **zero V-space width, no content, no structural entries**.

---

### Summary

| Question | Answer |
|---|---|
| I-space allocation | Exactly **one** `GRANORGL` entry inserted into the granfilade at the computed address (e.g., `account.0.1` for the first document) |
| Is `findisatoinsertnonmolecule` the only I-space address computation? | Yes — `findisatoinsertmolecule` is not involved; that is only for `ATOM` (text/link) insertions |
| Initial V-space | **Empty** — the POOM enfilade has a bare root with `cwid.dsas[V] = 0`; no content, no structural entry, zero width |
| What is the orgl? | A fresh `createenf(POOM)` [granf2.c:120], held in-core with `diskorglptr = DISKPTRNULL` |

Content only enters V-space when `doinsert` is later called, which goes through `insertnd` → POOM path (`makegappm` + `doinsertnd`) to place a 2D (I×V) entry into the document's orgl [insertnd.c:53–61].
