# Revision Consultation — ASN-0025

**Review:** review-1.md
**Date:** 2026-03-07 07:15

## Summary

9 REVISE items analyzed: 8 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 5: CREATE VERSION I-space effect is self-contradictory

**Category:** GREGORY
**Reason:** The Gregory evidence for CREATE VERSION covers only POOM (V-space) allocation. The parenthetical claim about an orgl entry in I-space is unsupported by any cited implementation evidence. We need confirmation of what `docreatenewversion` actually allocates in the granfilade.

**Gregory question:** Does `docreatenewversion` allocate any entry in the granfilade (I-space), such as an orgl record? If so, what I-address does it receive and in which subspace?

**Gregory's Answer:**

## KB Synthesis

Yes — `docreatenewversion` allocates exactly **one** granfilade entry: a new document orgl record. Here are the details.

## What is allocated

`docreatenewversion` calls `createorglingranf` with a DOCUMENT hint, which internally calls `findisatoinsertnonmolecule`. This allocates a new **document address** (not a content I-address) via the stateless query-and-increment mechanism:

1. Compute upper bound: `tumblerincrement(source_doc, depth=0, 1)` — the next sibling of the source document
2. Call `findpreviousisagr` to find the highest existing address below that bound
3. Allocate: first child as `source_doc.1`, or increment from the highest existing child

[ST-VERSION], [SS-ADDRESS-ALLOC] (Finding 0068)

## What I-address it receives

The allocated address lands in the **document address namespace**, structurally subordinate to the source document:

```
Source doc:       1.1.0.1.0.1
First version:    1.1.0.1.0.1.1        (owned case — child of source)
Second version:   1.1.0.1.0.1.2
Cross-user case:  1.1.0.2.0.1          (unowned — under creating user's account)
```

[SS-VERSION-ADDRESS] (Finding 0068), [ST-VERSION-OWNERSHIP]

## Which subspace

This address is in the **document address namespace** — entirely separate from both content subspaces:

| Namespace | Structure | Allocated by |
|-----------|-----------|--------------|
| Document addresses | `account.0.doc.N` or `doc.N` | `findisatoinsertnonmolecule` |
| Text content I-addresses | `doc.0.3.x` (element_field=3) | `findisatoinsertmolecule` |
| Link I-addresses | `doc.0.2.x` (element_field=2) | `findisatoinsertmolecule` |

[SS-ADDRESS-SPACE] (Finding 0065, 0077)

## Critical: no content I-addresses allocated

`docreatenewversion` does NOT call `findisatoinsertgr` for content. The `docopyinternal` step copies existing I-addresses from the source via `insertpm` + `insertspanf` — sharing them, not allocating new ones. This is why VERSION does not break I-address contiguity for subsequent text INSERTs (unlike CREATELINK, which allocates a link orgl in the content I-address range and introduces a gap).

[FC-GRANF-ON-VERSION], [INV-MONOTONIC] (Finding 0077):

> "CREATENEWVERSION does NOT break I-address contiguity for subsequent text INSERTs. Unlike CREATELINK… VERSION allocates only a document address in a separate tumbler range."

---

## Code Exploration

---

## Answer

Yes. `docreatenewversion` unconditionally allocates a new GRANORGL entry in the granfilade (I-space). Here is the complete trace.

---

### Call chain

```
createnewversion()          [fns.c:289]
  └─ docreatenewversion()   [do1.c:260]
       └─ createorglingranf()  [granf1.c:50]
            └─ createorglgr()     [granf2.c:111]
                 ├─ findisatoinsertgr()           [granf2.c:130]  → computes I-address
                 │    └─ findisatoinsertnonmolecule()  [granf2.c:203]
                 ├─ createenf(POOM)               [granf2.c:120]  → empty orgl
                 └─ insertseq()                   [granf2.c:125]  → writes into granfilade
```

---

### What it allocates

`createorglgr` at `granf2.c:111–128` does three things:

1. Computes the new I-address via `findisatoinsertgr` (written into `*isaptr`, which is `newisaptr` from the caller).
2. Creates a fresh empty POOM enfilade: `createenf(POOM)` at `granf2.c:120`. This is the orgl that will later hold V-space content for the new version.
3. Inserts a `GRANORGL` crum into the granfilade at the computed address via `insertseq` at `granf2.c:125`.

```c
// granf2.c:111–128
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;
  bool findisatoinsertgr();
  typecuc *createenf();

      if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
          return (FALSE);
      locinfo.infotype = GRANORGL;
      locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // new POOM enfilade
      reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
      locinfo.granstuff.orglstuff.orglincore = TRUE;
      locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
      locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
      insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);       // placed at computed I-address
      rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
      return (TRUE);
}
```

---

### What I-address it receives — two cases

The hint passed to `createorglgr` is constructed at `do1.c:270–276`, with an ownership test that selects one of two hint types. Note that in the FEBE path (`fns.c:296`), both `isaptr` and `wheretoputit` are `&originaldocisa`, so `tumbleraccounteq` is trivially true and `isthisusersdocument` is the deciding condition.

#### Case A — own document: `DOCUMENT → DOCUMENT` hint (depth = 1)

```c
// do1.c:270–271
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
```

Constants from `xanadu.h:141–142`: `DOCUMENT = 3`. Since `supertype == subtype`, `depth = 1` at `granf2.c:209`.

`findisatoinsertnonmolecule` with depth=1 and `hintisa = D` (the original document's address):

- `upperbound = tumblerincrement(D, depth−1=0, 1)` → the next sibling document address (e.g., `1.1.0.1.0.2` if `D = 1.1.0.1.0.1`)
- `findpreviousisagr` returns the highest I-address less than `upperbound` that already exists — either `D` itself (empty doc) or the highest content item under `D`
- **First new version of empty doc**: lowerbound = `D` (length = `hintlength`), so `tumblerincrement(D, depth=1, 1, isaptr)` → appends one position: `D.0.1`
- **Subsequent versions**: lowerbound already has length > `hintlength`; `tumblertruncate` to `hintlength+1`, then `tumblerincrement` at position 0 → `D.0.N` where N increments

**Result**: the new version's orgl lands at **`D.0.N`** — within the original document's own I-sub-space.

Concrete example: document `1.1.0.1.0.1` → first new version gets I-address **`1.1.0.1.0.1.0.1`**.

Text atoms in the same document (inserted via `findisatoinsertmolecule` with TEXTATOM) use a deeper sub-address (`D.0.0.N.0.1`), so there is no collision.

#### Case B — another user's document: `ACCOUNT → DOCUMENT` hint (depth = 2)

```c
// do1.c:272–275
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
```

`ACCOUNT = 2, DOCUMENT = 3`; since `supertype ≠ subtype`, `depth = 2`.

This is identical in algorithm to `docreatenewdocument` at `do1.c:234–241`:
```c
// do1.c:238–240
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

With depth=2 and `hintisa = account`:
- `tumblerincrement(account, depth=2, 1)` → `account.0.N` (two levels deeper)

**Result**: the new version's orgl is allocated in the **user's account document sub-space**, exactly like a brand-new document.

Concrete example: account `1.1.0.1`, no prior documents → new version gets I-address **`1.1.0.1.0.1`**.

The `bert.c` copy-on-write path explicitly passes `&taskptr->account` as `wheretoputit`:
```c
// bert.c:274
docreatenewversion(taskptr, tp, &taskptr->account, newtp);
```
so Case B always fires from there, placing the version in the current user's account sub-space regardless of the source document's owner.

---

### Summary

| Condition | Hint | Depth | I-address subspace | Example result |
|---|---|---|---|---|
| User's own document | `DOCUMENT → DOCUMENT`, `hintisa = original_doc` | 1 | Original document's I-sub-space | `1.1.0.1.0.1` → `1.1.0.1.0.1.0.1` |
| Another user's doc (FEBE or bert.c) | `ACCOUNT → DOCUMENT`, `hintisa = target_account` | 2 | User's account document sub-space | account `1.1.0.1` → `1.1.0.1.0.N` |

In both cases, a single `GRANORGL` crum is inserted into the granfilade at the computed I-address. The address is written back into the caller's `newisaptr` (returned to the client as the new document's I-address via `putcreatenewversion` at `fns.c:297`). The new orgl begins as an empty POOM enfilade; content is then copied into it by `docopyinternal` at `do1.c:293`.
