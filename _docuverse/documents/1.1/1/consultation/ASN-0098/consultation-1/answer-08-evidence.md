## Question 8 [evidence]

> For each non-invariant (novelty, cardinality, document-identity), which specific udanax-green operation produces an observable change in that property, and what is the minimal trace exhibiting the change?

## KB Synthesis

## Novelty, Cardinality, Document-Identity: Which Operations Change Each

---

### Novelty — creation of I-addresses that have never existed

**Operation:** INSERT (and CREATELINK for link orgls)

INSERT is the **only** operation that allocates fresh I-addresses from the global permascroll. VCOPY shares existing ones. VERSION copies existing ones. DELETE, REARRANGE touch no I-addresses at all [FC-GRANF-ON-DELETE].

**Minimal trace:**

```
CREATE doc D
INSERT "A" at V=1.1 into D
  → allocates I-address I.1 (never existed before)
  → FINDDOCSCONTAINING(I.1) = {D}
  → compare_versions(D, any_prior_doc) = ∅ for this character
```

CREATELINK produces a second novelty kind — a link-orgl I-address — which breaks text I-address contiguity for subsequent INSERTs [INT-LINK-INSERT]:

```
INSERT "AB" → I.1, I.2
CREATELINK  → link orgl consumes I-space up to ~I.2.0
INSERT "CD" → I.2.1, I.2.2 (gap from "AB")
compare_versions → 2 shared span pairs, not 1
```

---

### Cardinality — count of elements in a set

Three distinct cardinalities with different operations:

**V-stream cardinality (mutable, bidirectional):**

| Operation | Effect | Minimal trace |
|-----------|--------|---------------|
| INSERT | +width | `INSERT "AB" → width 0.2` |
| DELETE | −width | `DELETE(D, 1.1, 0.1) → width 0.1` |
| REARRANGE | **invariant** | no change — identity-preserving permutation [INV-REARRANGE-IDENTITY] |
| VCOPY | +width | same as INSERT for V-cardinality |

**I-address cardinality (permanent, monotone-increasing only):**

Only INSERT and CREATELINK increase it. No operation in the system decreases it [INV-NO-IADDR-REUSE, INV-MONOTONIC]. Minimal trace:

```
INSERT "A" → one new I-address; global max advances
INSERT "A" again → one more new I-address; max advances again
DELETE "A" → V-mapping gone; I-address count UNCHANGED
```

**Link cardinality (permanent, monotone-increasing only):**

Only CREATELINK increases it [INV-LINK-PERMANENCE]. Minimal trace:

```
INSERT source_text, target_text
CREATELINK → |links| = 1 forever
```

---

### Document-Identity — what V→I mapping this document has

The POOM is the sole mutable layer [SS-POOM-MUTABILITY]; every mutation changes document-identity in V-space. But V-space and I-space tell different stories:

**V-space document-identity (POOM state):**

INSERT, DELETE, REARRANGE, VCOPY all change it. Minimal distinguishing trace for INSERT vs VCOPY:

```
INSERT "X" into D:
  D.poom = {V=1.1 → I.fresh}       ← novelty; I.fresh is new

VCOPY "X" from S into D:
  D.poom = {V=1.1 → I.existing}    ← shared identity; I.existing was S's
```

Observable distinction: `compare_versions(D_insert, S) = ∅`; `compare_versions(D_vcopy, S) = [{span, span}]`.

**I-space document-identity (spanfilade association — permanent):**

DELETE does NOT change this. After `INSERT "A"` then `DELETE "A"`, FINDDOCSCONTAINING still returns the document [INV-IADDRESS-PERMANENT, EC-STALE-SPANF-REFERENCE]. Only INSERT and VCOPY grow the document's I-space association:

```
INSERT "A" into D → FINDDOCSCONTAINING(I.1) = {D}
DELETE "A" from D → FINDDOCSCONTAINING(I.1) = {D}   ← unchanged
```

**Summary table:**

| Property | INSERT | DELETE | REARRANGE | VCOPY | CREATELINK | VERSION |
|----------|--------|--------|-----------|-------|------------|---------|
| Novelty (new I-addr) | **yes** | no | no | no | **yes (link)** | no |
| V-stream cardinality | +width | −width | unchanged | +width | no | no |
| I-addr cardinality | +1/char | unchanged | unchanged | unchanged | +1 link | unchanged |
| POOM (V→I mapping) | **yes** | **yes** | **yes** | **yes** | **yes (2.x)** | creates new |
| Spanfilade association | +entries | unchanged | unchanged | +entries | +entries | +entries |

---

## Code Exploration

I now have all the evidence needed. Let me compose the full answer.

---

## Non-Invariants in udanax-green: Novelty, Cardinality, Document-Identity

All citations use relative paths from the repository root. Code quoted verbatim from source; line numbers from `Read` tool output.

---

### 1. Novelty

**Definition in the implementation.** Novelty is the property that an I-space span represents content allocated for the first time — content whose I-addresses have no prior existence anywhere in the permascroll. It is the structural opposite of transcluded content, which reuses pre-existing I-addresses.

**The operation that creates novelty: `doinsert`** (`do1.c:87`).

`doinsert` is the *only* FEBE operation that calls `inserttextingranf` — the only path in the system that allocates new granfilade leaves:

```c
/* do1.c:117-122 */
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

The allocation chain descends as follows:

**`inserttextgr`** (`granf2.c:83`):
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);   /* granf2.c:99 */
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
```

**`findisatoinsertmolecule`** (`granf2.c:158`) computes the novel address:
```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); /* granf2.c:164 */
/* lowerbound = highest existing I-address under this document's text subspace */
...
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);   /* granf2.c:169 — KEY LINE */
```

`findpreviousisagr` (`granf2.c:255`) walks the granfilade tree rightward (highest-first) to find the current ceiling. `tumblerincrement` with rightshift=0 adds 1 to the last mantissa digit of `lowerbound`, producing an I-address that has never been placed in any granfilade crum before.

That address is then written permanently into the granfilade at `granf2.c:99` via `insertseq`. The moment `insertseq` returns, the content is in the permascroll at a novel I-address.

**Minimal trace exhibiting novelty:**

```
doinsert                              [do1.c:87]
  inserttextingranf → inserttextgr   [granf1.c:44, granf2.c:83]
    findisatoinsertgr                 [granf2.c:130]
      findisatoinsertmolecule         [granf2.c:158]
        findpreviousisagr             [granf2.c:255]
          ← returns: lowerbound = highest current I-address
        tumblerincrement(lowerbound, 0, 1, isaptr)   [granf2.c:169]
          ← isaptr = lsa = first never-before-used I-address
    insertseq(fullcrumptr, &lsa, &locinfo)           [granf2.c:99]
          ← text enters permascroll at novel I-address
```

**No other FEBE operation reaches `inserttextgr`.** `docopy` (`do1.c:45`), used internally by `doinsert` and by the COPY operation, calls only `insertpm` (`orglinks.c:75`) — it maps existing I-spans into V-space. It never allocates a new granfilade leaf. `docreatenewversion` (`do1.c:260`) calls `docopyinternal` (`do1.c:66`) which likewise routes through `insertpm`, not `inserttextgr`. Thus novelty is INSERT-exclusive.

---

### 2. Cardinality

**Definition in the implementation.** Cardinality is the V-space width of a document's POOM root: `((typecuc*)orgl)->cwid.dsas[V]`. It is read by `retrievedocumentpartofvspanpm` (`orglinks.c:155`) and returned to the client as the `width` field of a `typevspan`:

```c
/* orglinks.c:158-161 */
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

Two operations produce observable changes:

#### 2a. INSERT / COPY increase cardinality

Both `doinsert` and `docopy` ultimately call `insertpm` (`orglinks.c:75`), which calls `insertnd` to create or extend bottom crums (POOM leaves) with new V-span mappings:

```c
/* orglinks.c:113-131 */
movetumbler (vsaptr, &crumorigin.dsas[V]);
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
/* ↑ inserts new POOM crum mapping vsaptr → ispanset */
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
```

`insertnd` (`insertnd.c:15`) dispatches to `doinsertnd` → `insertcbcnd` (`insertnd.c:242`):

```c
new = createcrum (0, (INT)father->cenftype);   /* insertnd.c:260 */
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
movewisp (width, &new->cwid);
```

After insertion, `setwispupwards` (`insertnd.c:56-58`) propagates the width increase to the root:

```c
setwispupwards(fullcrumptr, 1);
```

`setwispupwards` recomputes `cwid` at every ancestor, so `fullcrumptr->cwid.dsas[V]` grows by exactly `crumwidth.dsas[V]` (the V-width of what was inserted).

**Minimal trace (INSERT, cardinality increases by N bytes):**
```
doinsert                              [do1.c:87]
  inserttextingranf → ispanset (width N)
  docopy                             [do1.c:119 → do1.c:45]
    insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)  [do1.c:60 → orglinks.c:75]
      insertnd(taskptr, orgl, &crumorigin, &crumwidth, &linfo, V)  [orglinks.c:130]
        doinsertnd → insertcbcnd      [insertnd.c:57, 231]
          createcrum / adopt          [insertnd.c:260-263]  ← new POOM leaf
        setwispupwards(fullcrumptr,1) [insertnd.c:56]
          ← orgl->cwid.dsas[V] += N
```

#### 2b. DELETE decreases cardinality

`dodeletevspan` (`do1.c:158`) → `deletevspanpm` (`orglinks.c:145`) → `deletend` (`edit.c:31`):

```c
/* edit.c:47-73 */
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);         /* edit.c:59 */
        subtreefree ((typecorecrum*)ptr);    /* edit.c:60 */
        break;                               /* POOM leaf gone */
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;                               /* width trimmed */
    }
}
setwispupwards (father, 1);   /* edit.c:74 — cwid.dsas[V] decreases */
```

**Minimal trace (DELETE width W, cardinality decreases by W):**
```
dodeletevspan(taskptr, docisaptr, vspanptr)  [do1.c:158]
  deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)  [do1.c:165 → orglinks.c:145]
    deletend(orgl, &vspanptr->stream, &vspanptr->width, V)  [orglinks.c:149 → edit.c:31]
      makecutsnd / newfindintersectionnd     [edit.c:44-46]
      loop: deletecutsectionnd → disown + subtreefree  [edit.c:59-60]  ← POOM leaf removed
      setwispupwards(father, 1)              [edit.c:74]
        ← orgl->cwid.dsas[V] -= W
```

**REARRANGE does NOT change cardinality.** `rearrangend` (`edit.c:78`) permutes the POOM but calls only `makecutsnd`, `newfindintersectionnd`, and `insertcutsectionnd`/`deletecutsectionnd` — it never creates or removes content. The root `cwid.dsas[V]` remains constant.

---

### 3. Document-Identity

**Definition in the implementation.** Document-identity is the `typeisa` (which is `typedef tumbler typeisa`) assigned to a document on creation — its canonical address in the granfilade. It is the key for all access: `findorgl` (`granf1.c:17`) looks up the POOM by ISA via `fetchorglgr` (`granf2.c:22`), which calls `retrievecrums` to walk the granfilade tree to the exact ISA. Every FEBE operation that reads or writes a document passes this ISA; the granfilade rejects any ISA that does not exist (`isaexistsgr`, `granf2.c:244`).

**The ISA of an existing document never changes.** There is no operation in the FEBE set that modifies the granfilade key of an existing document. The granfilade is append-only for keys: `insertseq` adds nodes; `deleteseq` (`edit.c:16`) removes them but is only called for 1-D (GRAN-type) sequential operations, not POOM or SPAN enfilades.

**The operation that creates new document-identity: `docreatenewdocument`** (`do1.c:234`) and **`docreatenewversion`** (`do1.c:260`).

```c
/* do1.c:234-241 */
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

The chain:

**`createorglingranf` → `createorglgr`** (`granf1.c:49`, `granf2.c:111`):
```c
/* granf2.c:117-127 */
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);    /* granf2.c:120 */
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        /* granf2.c:125 */
```

**`findisatoinsertnonmolecule`** (`granf2.c:203`) computes the new ISA:
```c
/* granf2.c:209 */
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
/* ACCOUNT → DOCUMENT: depth = 2 */

tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); /* granf2.c:213 */
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); /* granf2.c:217 */

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr); /* granf2.c:237 — first doc */
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
    /* granf2.c:239-240 — next sibling */
}
```

After `tumblerjustify(isaptr)` (`granf2.c:154`), `isaptr` holds the new document's permanent ISA. It is written into the granfilade at `granf2.c:125` via `insertseq`. From that moment on, the ISA exists and is findable; it is never mutated by any subsequent operation.

**`docreatenewversion`** creates a distinct identity for the version:

```c
/* do1.c:270-277 */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint); /* sibling versioning */
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint); /* cross-account */
}
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) { /* newisaptr ← new ISA */
    return (FALSE);
}
```

`newisaptr` receives a fresh ISA. The source document's `isaptr` is completely unaffected.

**Minimal trace (new document-identity):**
```
docreatenewdocument(taskptr, isaptr)          [do1.c:234]
  makehint(ACCOUNT, DOCUMENT, 0, ...)         [do1.c:239]
  createorglingranf(taskptr, granf, &hint, isaptr)  [do1.c:240 → granf1.c:49]
    createorglgr(taskptr, granfptr, hintptr, isaptr)  [granf2.c:111]
      findisatoinsertgr(fullcrumptr, hintptr, isaptr)  [granf2.c:117]
        findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr)  [granf2.c:152]
          findpreviousisagr(fullcrumptr, &upperbound, &lowerbound)  [granf2.c:217]
            ← lowerbound = highest existing doc ISA under this account
          tumblerincrement(&hintptr->hintisa, depth, 1, isaptr)  [granf2.c:237]
            ← isaptr = lowerbound.account.succ = new permanent identity
        tumblerjustify(isaptr)                [granf2.c:154]
      locinfo.granstuff.orglstuff.orglptr = createenf(POOM)  [granf2.c:120]
      insertseq(fullcrumptr, isaptr, &locinfo)  [granf2.c:125]
        ← ISA permanently installed in granfilade; POOM root created
```

---

### Summary Table

| Property | Observed via | Increased / Created by | Decreased by | Unchanged by |
|---|---|---|---|---|
| **Novelty** | I-address uniqueness (not in any other POOM or granfilade crum) | `doinsert` → `inserttextgr` → `insertseq` at fresh I-addr (`granf2.c:99`) | `docopy` reuses I-addrs (no new novelty); DELETE removes V-ref but I-addr persists | REARRANGE, COPY, CREATENEWVERSION |
| **Cardinality** | `cwid.dsas[V]` of POOM root (`orglinks.c:160`) | `doinsert`, `docopy` → `insertpm` → `insertnd` → `setwispupwards` (`insertnd.c:56`) | `dodeletevspan` → `deletend` → `disown`+`subtreefree` → `setwispupwards` (`edit.c:59-74`) | `dorearrange` (V-span shuffled, not grown or shrunk) |
| **Document-identity** | `typeisa` tumbler (granfilade key, set at creation) | `docreatenewdocument` / `docreatenewversion` → `createorglgr` → `insertseq` at new ISA (`granf2.c:125`) | *Never reduced* — ISA is permanent | All read/write operations (INSERT, COPY, DELETE, REARRANGE) |

**Key structural invariants behind the table:**
- The granfilade is **append-only for keys**. `insertseq` adds; nothing removes a GRANORGL or GRANTEXT key once placed. [`granf2.c:99`, `granf2.c:125`]
- The POOM is **write-many in V-space**. `insertnd` adds crums (cardinality up); `deletend` prunes crums (cardinality down); neither touches the granfilade. [`insertnd.c:15`, `edit.c:31`]
- Novel I-addresses come only from `findisatoinsertmolecule`'s `tumblerincrement` on `findpreviousisagr`'s result. [`granf2.c:164-169`] This is called only from the INSERT path.
