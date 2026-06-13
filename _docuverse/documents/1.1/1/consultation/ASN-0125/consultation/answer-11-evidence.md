## Question 11 [evidence]

> Is there any backend code path that mutates an existing link orgl's endsets in place in the granfilade, or does every endset change necessarily require allocating a new link orgl with a fresh I-address under `findisatoinsertnonmolecule`?

## KB Synthesis

The KB gives a clear answer: **no backend code path mutates an existing link orgl's endsets in-place.** Every link is write-once at creation time, and any endset change would require allocating a new link orgl at a fresh I-address.

**The granfilade is append-only by architecture**

[INV-IADDR-IMMUTABILITY] states that "the content associated with any I-address never changes" — this applies universally to all granfilade content, including link orgls. [FC-GRANF-ON-DELETE] confirms that only INSERT, COPY, and CREATELINK add entries; no operation modifies existing content. [SS-POOM-MUTABILITY] formalizes the three-way split: "granfilade: I-addr → byte — immutable, append-only."

**The granf interface has no modify operation**

[SS-GRANF-OPERATIONS] lists the four granf operation classes: `findorgl()` (locate), `inserttextingranf()` (add text), `createorglingranf()` (create new orgl), and `ispanset2vstuffset()` (dereference). There is no `modifyorgl`, `updateendsets`, or equivalent. The interface simply does not provide an in-place mutation path.

**CREATELINK is the only write to I-space for links**

[ST-CREATE-LINK] (Finding 0012) describes link creation as: "(1) create a link orgl in `granf` via `createorglingranf()`; (2) copy the link's ISA reference into the document's link subspace; (3) index endpoints in `spanf`." This three-step sequence is the totality of what writes to a link's I-space entry. The FEBE protocol has no MODIFYLINK or UPDATELINK opcode — [INV-LINK-PERMANENCE] (Finding 0024) confirms there is not even a DELETELINK.

**The three-layer model makes this explicit**

[SS-THREE-LAYER-MODEL] (Finding 0040) states: "`CREATELINK` writes to all three layers. `DELETEVSPAN(2.x)` removes only the POOM entry. **No operation removes from I-space or spanfilade.**" Mutation is equally absent — only the POOM layer (document-level V-stream) is mutable; the I-space link orgl is fixed from birth.

**On the allocation mechanism**

One small correction to the question's framing: link orgls use `findisatoinsertmolecule` (the same allocator as text atoms), not `findisatoinsertnonmolecule` which handles document/version addresses [SS-ADDRESS-ALLOC] (Finding 0065). But the consequence is the same — any new link orgl gets a fresh, monotonically-increasing I-address [INV-MONOTONIC], and there is no way to reuse or overwrite an old one [INV-NO-IADDR-REUSE].

**Summary:** Endset data is baked into the link orgl at `createorglingranf()` time and never touched again. If a "changed" link were needed, the only path would be to call CREATELINK again, producing a brand-new link orgl at a new I-address — the old one remaining permanent and unmodified at its original address.

---

## Code Exploration

I now have the complete picture across all relevant source files. Here is the full answer.

---

## Answer

**No, there is no code path that mutates an existing link orgl's endsets in place in the granfilade.** However, there is also a correction to the question's premise: link orgl I-addresses are allocated by `findisatoinsertmolecule`, not `findisatoinsertnonmolecule`.

---

### The Only Two Entry Points That Create Link Orgls With Endsets

Both entry points in the FEBE command surface are:

- `domakelink` [do1.c:169–193]
- `docreatelink` [do1.c:195–221] — called from `fns.c:createlink` (the FEBE `CREATELINK` handler)

Both follow an identical, strictly ordered sequence. For `docreatelink`:

```c
// do1.c:207-219
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // [1] fresh I-address
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED) // [2] fetch new orgl
  && specset2sporglset (...)
  && setlinkvsas (...)
  && insertendsetsinorgl (taskptr, linkisaptr, link, ...)    // [3] populate endsets
  && insertendsetsinspanf (...)
);
```

Step [1] always precedes step [3]. There is no code path where `insertendsetsinorgl` is called on a link orgl that was not just freshly created by `createorglingranf` in the same function call.

---

### The Allocation Route Is `findisatoinsertmolecule`, Not `findisatoinsertnonmolecule`

`makehint` sets `hint.subtype = ATOM` [do1.c:207 → do2.c:80–83]. Inside `findisatoinsertgr` [granf2.c:130–156]:

```c
// granf2.c:135
if (hintptr->subtype == ATOM) {
    ...
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // link atoms go here
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // DOCUMENT/ACCOUNT/NODE
}
```

`findisatoinsertnonmolecule` [granf2.c:203–242] handles non-ATOM types (DOCUMENT, ACCOUNT, NODE). It is **not** on the link-creation path. Link orgls use `findisatoinsertmolecule` [granf2.c:158–181], which for `LINKATOM` increments from the previous link-atom I-address to produce a new unique position.

---

### What `createorglgr` Does (granf2.c:111–128)

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);  // brand-new empty POOM enfilade
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);      // places it in granfilade at fresh ISA
```

`createenf(POOM)` [credel.c:492] creates a fresh, empty POOM enfilade. `insertseq` [insert.c:17] places a new `GRANORGL` crum at the just-allocated I-address. This crum records a pointer to the new POOM enfilade. No function anywhere replaces or deletes this crum after the fact.

---

### `insertendsetsinorgl` Only Operates on Freshly Created Orgls

`insertendsetsinorgl` [do2.c:130–149] calls `insertpm` three times:

```c
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)
insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)
```

`insertpm` [orglinks.c:75–134] calls `insertnd` to insert crum nodes into the POOM enfilade:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

There are exactly two call sites for `insertendsetsinorgl` in the entire codebase: `domakelink` (do1.c:190) and `docreatelink` (do1.c:218). Both always call `createorglingranf` first in the same evaluation chain.

---

### No Post-Creation Endset Mutation Exists — Four Layers of Evidence

**1. FEBE protocol has no such operation.** `requests.h` defines the complete set of link operations:

```
CREATELINK         27
FOLLOWLINK         18
RETRIEVEENDSETS    28
FINDLINKSFROMTOTHREE    30
FINDNUMOFLINKSFROMTOTHREE 29
FINDNEXTNLINKSFROMTOTHREE 31
```

There is no `UPDATELINK`, `ADDENDSET`, `REMOVEENDSET`, or `SETENDSETS` operation.

**2. `insertpm` has exactly two call sites**, both inside `insertendsetsinorgl`, which is always preceded by `createorglingranf` in the same call chain.

**3. `deletend` and `rearrangend` are never called on link orgls.** `deletevspanpm` [orglinks.c:145–152] and `rearrangepm` [orglinks.c:137–142] call `deletend` and `rearrangend` respectively, but both operate exclusively on document orgls fetched by `findorgl` from `dodeletevspan` and `dorearrange`. No parallel function for link orgls exists.

**4. No granfilade record replacement path exists.** `insertseq` places a `GRANORGL` crum at an I-address. No function in the codebase locates an existing `GRANORGL` by I-address and replaces its `orglptr` with a different enfilade, or deletes the crum from the granfilade.

---

### Summary

Every link creation in udanax-green:

1. Allocates a fresh I-address via `findisatoinsertmolecule` (not `findisatoinsertnonmolecule`) [granf2.c:142]
2. Creates a brand-new empty POOM enfilade via `createenf(POOM)` [granf2.c:120]
3. Records it in the granfilade as a new `GRANORGL` crum via `insertseq` [granf2.c:125]
4. Populates the endsets in that new orgl via `insertendsetsinorgl` → `insertpm` → `insertnd` [do2.c:132–138]

Once a link orgl's I-address is established in the granfilade, its POOM content (endsets) is structurally immutable: the FEBE protocol exposes no mutation operation, and no internal function is wired to modify it. The granfilade record (`GRANORGL` crum) and the POOM enfilade it points to are both written once at creation time and only read thereafter.
