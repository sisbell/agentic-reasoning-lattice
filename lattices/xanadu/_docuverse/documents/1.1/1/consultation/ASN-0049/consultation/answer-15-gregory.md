## Question 15 [gregory]

> After COPY creates shared I-addresses between doc1 and doc2, does an INSERT into doc1 at a position within the transcluded range affect doc2's POOM in any way — specifically, does `makegappm` operate only on the single `fullcrumptr` passed to `insertnd`, with no mechanism to locate or modify doc2's tree?

## KB Synthesis

No. An INSERT into doc1 has zero effect on doc2's POOM, regardless of shared I-addresses. The reasoning is structural:

**`makegappm` operates on a single POOM tree.** The function receives `fullcrumptr` — the root of the target document's orgl enfilade [SS-TWO-BLADE-KNIFE]. It constructs a two-blade knife and calls `insertcutsectionnd` to shift entries within `[blade[0], blade[1])` in that one tree. There is no global POOM registry, no mechanism to enumerate other documents' orgl trees, and no lookup path from a V-position to "all POOMs that share I-addresses at this position."

**POOM trees are per-document and fully independent.** Each document's POOM is a separate B-tree structure at its own memory/disk address [SS-POOM-MUTABILITY]. Doc2's tree has its own root pointer, its own nodes, and its own V-space coordinate system. `insertnd` operates on the single `fullcrumptr` passed to it — doc2's tree is not reachable from doc1's tree traversal.

**Transclusion shares I-addresses, not V-space.** COPY places the same I-addresses into multiple POOM trees, but each tree independently maps its own V-positions to those I-addresses [SS-CONTENT-IDENTITY], [FC-DOC-ISOLATION]. When INSERT into doc1 shifts V-positions in doc1's POOM (entries in `[blade[0], blade[1])`), doc2's corresponding V-positions are untouched. Doc2 still maps its own (unchanged) V-positions to the shared I-addresses.

**The I-addresses themselves are immutable.** INSERT allocates fresh I-addresses for new content — it does not modify the granfilade entries that doc2 already references [INV-IADDR-IMMUTABILITY], [FC-INSERT-IADDR]. Doc2 continues to read identical bytes at the same I-addresses.

**Explicit frame condition.** [FC-DELETE-CROSS-DOC] states this same invariant for DELETE: "DELETE in one document has zero effect on any other document's POOM mappings." INSERT is strictly additive and the same isolation applies — the shift mechanism in `makegappm` is scoped to the single orgl tree being modified [ST-INSERT] Finding 0054.

Summary: after `COPY(doc1 → doc2)` and then `INSERT(doc1, pos, text)`, doc2's POOM is bit-for-bit identical to what it was immediately after the COPY. The shared I-addresses remain accessible from doc2 at the same V-positions, with the same content bytes, as if the INSERT never happened.

---

## Code Exploration

---

## Answer

**Yes — `makegappm` operates exclusively on the single `fullcrumptr` passed to `insertnd`. There is no mechanism by which INSERT into doc1 can locate or modify doc2's POOM.**

The proof runs through every layer of the call stack.

---

### 1. INSERT entry point — `fns.c:84–98`

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);
    if (!doinsert (taskptr, &docisa, &vsa, textset)) ...
}
```

INSERT takes a single `docisa`. Everything downstream is keyed to that one document identity.

---

### 2. `doinsert` — `do1.c:87–123`

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

Two operations: `inserttextingranf` writes the new text bytes into the permascroll (granfilade), assigning them fresh I-addresses. `docopy` records the resulting I-span into **one document's** POOM.

---

### 3. `docopy` — `do1.c:45–65`

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    );
}
```

`findorgl` is called with `docisaptr` — the address of doc1. It returns exactly one orgl: doc1's.

---

### 4. `findorgl` → `fetchorglgr` — `granf1.c:17–41` and `granf2.c:22–80`

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    ...
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH);
    ...
    ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
    ...
    return ((typeorgl)ret);
}
```

`fetchorglgr` uses `retrievecrums` to look up the granfilade node whose ISA matches `address`. It then returns the `orglptr` stored in that specific node's `cinfo.granstuff.orglstuff` — **the POOM tree belonging to that one document**. doc2's orgl is stored at doc2's ISA address; it is never touched here.

---

### 5. `insertpm` — `orglinks.c:75–134`

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    logbertmodified(orglisa, user);
    for (; sporglset; sporglset = ...) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        movetumbler (&lstream, &crumorigin.dsas[I]);
        movetumbler (&lwidth,  &crumwidth.dsas[I]);
        movetumbler (vsaptr,   &crumorigin.dsas[V]);
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
    }
    return (TRUE);
}
```

`insertpm` constructs a 2D crum address (`crumorigin` has both I and V coordinates) and calls `insertnd` on `orgl` — **a single orgl, passed in, never looked up again**. doc2's orgl is never passed here.

---

### 6. `insertnd` — `insertnd.c:15–111`

```c
int insertnd(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr, INT index)
{
    ...
    switch (fullcrumptr->cenftype) {
      case POOM:
          makegappm (taskptr, fullcrumptr, origin, width);   // line 54
          setwispupwards(fullcrumptr, 0);
          bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
          setwispupwards(fullcrumptr, 1);
          break;
      ...
    }
    if (bothertorecombine || ...) recombine(fullcrumptr);
}
```

`insertnd` receives `fullcrumptr` as its sole tree parameter. Every subsequent operation — `makegappm`, `setwispupwards`, `doinsertnd`, `recombine` — is called with that same pointer or a pointer derived from walking its subtree.

---

### 7. `makegappm` — `insertnd.c:124–172`

```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width)
{
    ...
    prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
    if (iszerotumbler(&fullcrumptr->cwid.dsas[V]) || ...) return(0);

    movetumbler (&origin->dsas[V], &knives.blades[0]);
    findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = V;
    makecutsnd (fullcrumptr, &knives);                    // cuts within fullcrumptr's tree
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // finds father within fullcrumptr's tree
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, NULL);
    for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {  // iterates children of father
        i = insertcutsectionnd(ptr, &fgrasp, &knives);
        switch (i) {
          case 1:
              tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // line 162
              ivemodified(ptr);
              break;
          ...
        }
    }
    setwidnd(father);
    setwispupwards(findfather((typecorecrum*)father), 1);
}
```

Every pointer used in `makegappm` is derived from `fullcrumptr`:
- `makecutsnd(fullcrumptr, &knives)` — splits nodes within this tree
- `newfindintersectionnd(fullcrumptr, ...)` — locates `father` by walking this tree
- `findleftson(father)` / `findrightbro(ptr)` — iterates children **within this tree**
- `findfather((typecorecrum*)father)` — walks up within this tree

The displacement update at line 162 — `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` — moves sibling crums in doc1's V-space to the right of the insertion point. These `ptr` nodes are children of `father`, which is a node in doc1's POOM tree. No function call in `makegappm` takes a document ISA, queries the granfilade for another document, or produces a pointer to any structure outside `fullcrumptr`'s tree.

---

### Why shared I-addresses don't create coupling

After COPY, both doc1's POOM and doc2's POOM contain bottom crums whose **I-dimension** (`cdsp.dsas[I]`, `cwid.dsas[I]`) points to the same permascroll range. But this is just a stored tumbler value — a number. There is no back-pointer from the granfilade content store to every POOM that references it, and no lookup of "all documents referencing this I-span." The granfilade node for a document stores only one orgl pointer (`cinfo.granstuff.orglstuff.orglptr`); there is no reverse index.

The V-space trees of doc1 and doc2 are structurally independent POOM enfilades. `makegappm` creates a gap in doc1's V-axis by cutting nodes and adjusting displacements within doc1's tree. doc2's V-axis — which has its own independent layout of V→I mappings — is not touched.

---

### Summary

| Step | Code | What it touches |
|------|------|-----------------|
| `insert()` | `fns.c:84` | Passes `docisa` (doc1) through |
| `doinsert()` | `do1.c:87` | Writes text to granfilade; calls `docopy(doc1)` |
| `docopy()` | `do1.c:45` | Calls `findorgl(doc1)` → returns doc1's orgl only |
| `fetchorglgr()` | `granf2.c:22` | Looks up ISA address; returns single orgl pointer |
| `insertpm()` | `orglinks.c:75` | Calls `insertnd(orgl)` — single orgl, no re-lookup |
| `insertnd()` | `insertnd.c:15` | Calls `makegappm(fullcrumptr)` — single tree |
| `makegappm()` | `insertnd.c:124` | All pointers derived from `fullcrumptr`; adjusts V-displacements within doc1's tree only |

**doc2's POOM is completely unaffected.** The shared I-addresses are a shared *content citation* (two documents happen to cite the same permascroll range), not a shared *structural node*. The POOM trees are entirely independent, and there is no mechanism — no reverse index, no broadcast, no shared node — by which a V-space operation on doc1 propagates to doc2.
