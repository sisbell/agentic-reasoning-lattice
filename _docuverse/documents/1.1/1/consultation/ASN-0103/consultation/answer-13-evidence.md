## Question 13 [evidence]

> Does creating a new document invoke `createenf` to build an initial empty POOM (2D orgl) tree, and what is the structural height of that freshly created empty enfilade?

## KB Synthesis

Yes. [SS-ENFILADE-TREE] (Finding 0058) is the direct source:

> `createenf(POOM)` produces a minimal **height-1** tree: a fullcrum with `isapex=TRUE`, `height=1`, containing a single bottom node (height-0) with **zero width**.

```
createenf(POOM):
  Fullcrum (height=1, isapex=TRUE, numberofsons=1)
    └─ Bottom node (height=0, width=0)
```

Code reference: `backend/credel.c:492-516`.

**Key structural details to note:**

- The bottom node has zero width — it is an empty placeholder, not content.
- For GRAN enfilades the bottom node has `infotype=GRANNULL`; POOM bottom nodes carry dual V/I coordinate fields initialized to zero.
- This never-filled state is **structurally distinct** from a document that had content and then had it all deleted. The delete-everything case retains the tree's grown height (via the disabled `levelpull`) with empty intermediate nodes and no bottom nodes at all [SS-ENFILADE-TREE, EC-EMPTY-DOC]. Crucially, Bug 0019 shows that the delete-everything state crashes on reinsertion because `firstinsertionnd` assumes a bottom crum always exists — a precondition the never-filled `createenf` state satisfies but the delete-everything state does not.

The KB does not explicitly trace `createorglingranf` (called during `CREATEDOCUMENT` and `CREATENEWVERSION` per [ST-VERSION-CREATE]) to a `createenf` call for the per-document POOM. That linkage is not answerable from the KB as written.

---

## Code Exploration

I now have the complete picture. Here is my full answer.

---

## Does `createenf` build the initial empty POOM tree for a new document?

**Yes.** Every path to document creation ends at `createenf(POOM)`. The structural height of the freshly built tree is **1**.

---

## Call Chain

### Step 1 — FEBE handler: `fns.c`

```c
// fns.c:276-286
void createnewdocument(typetask *taskptr)
{
  typeisa newdocisa;
  bool docreatenewdocument();

    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
      else
        putrequestfailed (taskptr);
}
```

### Step 2 — Document layer: `do1.c:234-241`

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`makehint` builds a hint with `supertype=ACCOUNT`, `subtype=DOCUMENT`. This is **not** an `ATOM` subtype, so it follows the `findisatoinsertnonmolecule` path when allocating the address.

### Step 3 — Granfilade shim: `granf1.c:50-55`

```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr)
{
  bool createorglgr();
     return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

### Step 4 — Granfilade core: `granf2.c:111-128`

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;
  bool findisatoinsertgr();
  typecuc *createenf();

      if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
          return (FALSE);
      locinfo.infotype = GRANORGL;
      locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // ← HERE
  reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
      locinfo.granstuff.orglstuff.orglincore = TRUE;
      locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
      locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
      insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
  rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
      return (TRUE);
}
```

`createenf(POOM)` is called at `granf2.c:120`. The returned pointer is stored in the granfilade leaf's `orglstuff.orglptr` field (`locinfo.infotype = GRANORGL`), then written into the granfilade tree via `insertseq`.

### Step 5 — `createenf`: `credel.c:492-516`

```c
typecuc *createenf(INT enftype)
{
  typecuc *fullcrumptr;
  typecorecrum *ptr;

    fullcrumptr = (typecuc *) createcrum(1, enftype);  // apex at height=1
    fullcrumptr->cenftype = enftype;                   // POOM
    fullcrumptr->isapex = TRUE;
    fullcrumptr->isleftmost = TRUE;
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);  // one leaf at height=0
    if (enftype == GRAN) {              // NOT entered for POOM
        ((typecbc *)ptr)->cinfo.infotype = GRANNULL;
    }
    ivemodified  (ptr);
    return (fullcrumptr);
}
```

`SON` is `#define SON LEFTMOSTSON` [`enf.h:137`], so the leaf is placed as the leftmost child of the apex.

---

## How `createcruminternal` initializes each node (`credel.c:541-596`)

| Call | `crumheight` | `enftype` | C type | What is zeroed |
|------|-------------|-----------|--------|----------------|
| `createcrum(1, POOM)` — apex | 1 | POOM | `typecuc` | `cwid`, `cdsp`, `numberofsons=0`, `leftson=NULL`, `sonorigin=DISKPTRNULL` |
| `createcrum(0, POOM)` — leaf | 0 | POOM | `type2dcbc` | `c2dinfo` is `clear()`'d (zero-filled) |

Critically, the `if (enftype == GRAN)` branch at `credel.c:587-590` that sets `GRANCLEARLYILLEGALINFO` is **not** entered. The `type2dcbc` leaf's `c2dinfo` is left completely zero-initialized, with no width or displacement content. This is the correct empty state for a POOM bottom crum.

---

## Structural Height of the Empty Enfilade

The apex is created as `createcrum(1, POOM)`, which sets `ptr->height = 1` at `credel.c:572`. The single leaf child has `height = 0`.

```
fullcrumptr  [height=1, isapex=TRUE, POOM, numberofsons=1, cwid=0, cdsp=0]
    └── ptr  [height=0, type2dcbc, c2dinfo=zeroed]
```

**The structural height of a freshly created empty POOM enfilade is 1.**

The `height` field counts levels above the bottom. Height=1 means "one layer of UC nodes above the leaves." When the tree fills and must grow, `levelpush` at `genf.c:263-294` increments `fullcrumptr->height++`, raising it to 2. An empty document starts at the minimum viable height (1) with a single zero-content leaf.

---

## Context: Two Other `createenf` Calls

For completeness: `entexit.c:44-45` calls `createenf(GRAN)` and `createenf(SPAN)` at system startup to initialize the global `granf` and `spanf` enfilades. These are the universe-level index trees, not per-document orgls. The per-document POOM orgl is always created by the path traced above.
