## Question 1 [evidence]

> Does udanax-green's docreatenewversion (do1.c:271) operate via a separately-tracked version-allocator record (analogous to granf for content and spanf for links), or does it dispatch through the same granfilade machinery as ordinary document allocation under the parent account?

## KB Synthesis

`docreatenewversion` dispatches through the **same granfilade machinery** as ordinary document allocation. There is no separate version-allocator record.

The KB is explicit on this:

**[ST-VERSION]** (Finding 0077):
> CREATENEWVERSION(d) allocates a new document address via `createorglingranf` with a DOCUMENT hint (which calls `findisatoinsertnonmolecule`).

**[SS-ADDRESS-ALLOC]** (Finding 0068):
> VERSION uses the same stateless query-and-increment allocation mechanism as CREATE and INSERT. The algorithm calls `findpreviousisagr` to find the highest existing address below an upper bound, then increments — dispatched via `granf2.c:130-156` (`findisatoinsertgr`) → `granf2.c:203-242` (`findisatoinsertnonmolecule`).

**[FC-GRANF-ON-VERSION]** (Finding 0077):
> VERSION modifies the granfilade by adding a document address entry. It does NOT allocate new content I-addresses.

The only structural distinction from ordinary account-level document creation is the **hint parameters**: for an owned-document version, `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` sets depth=1, placing the version under the source document's address prefix rather than under the parent account (`do1.c:272-280`). For an unowned-document version, it falls back to account-level placement, identical to CREATE.

In short: granf is the single allocation registry for all entity types — text atoms, document orgls, link orgls, and version orgls. The hint mechanism selects which subtree of the granf to allocate within.

---

## Code Exploration

I now have all the evidence needed to answer definitively.

---

## Answer: `docreatenewversion` dispatches through the same `granf` as ordinary document allocation

There is **no separate version-allocator record**. `docreatenewversion` and `docreatenewdocument` both call the identical function on the identical global granfilade. The only variation is in the `typehint` that controls *where* in the tumbler address space the new document is placed.

---

### The single granfilade

There is exactly one granfilade, `granf`, and one spanfilade, `spanf`. Both are created in `entexit.c:41–46`:

```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);   // entexit.c:44
    spanf = (typespanf) createenf (SPAN);   // entexit.c:45
}
```

`granf` is the single document/content organizer. It is declared `extern typegranf granf` at `xanadu.h:14` and defined at `corediskout.c:21`. No version-specific filade is ever created.

---

### `docreatenewdocument` [do1.c:234–241]

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);  // do1.c:239
    return (createorglingranf (taskptr, granf, &hint, isaptr)); // do1.c:240
}
```

Creates a new document by calling `createorglingranf` on `granf` with a hint whose `supertype=ACCOUNT(2)`, `subtype=DOCUMENT(3)`, `hintisa=caller's account tumbler`.

---

### `docreatenewversion` [do1.c:260–299]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
  ...
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint); // do1.c:271
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);            // do1.c:275
    }
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {          // do1.c:277
        return (FALSE);
    }
    ...
```

**Same function, same `granf`.** Only the hint differs.

---

### How the hint controls tumbler placement

`typehint` is defined at `xanadu.h:148–153`:

```c
typedef struct {
    INT supertype;   // hierarchy level above (NODE=1, ACCOUNT=2, DOCUMENT=3)
    INT subtype;     // level being created
    INT atomtype;    // 0 for non-atom
    typeisa hintisa; // tumbler to allocate near
} typehint;
```

`createorglingranf` [granf1.c:50–55] is a thin wrapper:

```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr)
{
  bool createorglgr();
     return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

`createorglgr` [granf2.c:111–128] does the real work:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);    // new POOM for the document
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        // insert into granf
    return (TRUE);
}
```

`findisatoinsertgr` [granf2.c:130–156] interprets the hint: for non-ATOM subtypes (DOCUMENT falls in this category since `subtype=DOCUMENT(3) < ATOM(4)`), it calls `findisatoinsertnonmolecule`, which scans the granfilade for the highest existing tumbler address under the hint's scope and increments it to find a free slot.

---

### The two version-creation cases

| Condition | `makehint` call | Effective behaviour |
|-----------|-----------------|---------------------|
| Same account, user's own doc | `DOCUMENT, DOCUMENT, 0, isaptr` [do1.c:271] | New document tumbler allocated *within the same document scope* as the source — a sibling in tumbler space |
| Cross-account (or not user's own doc) | `ACCOUNT, DOCUMENT, 0, wheretoputit` [do1.c:275] | Identical to `docreatenewdocument` but rooted at `wheretoputit` account instead of `taskptr->account` |

The own-document case uses `supertype == subtype == DOCUMENT(3)`, which `findisatoinsertnonmolecule` treats as a depth-1 search rooted at the source document's tumbler, producing a new tumbler that is a sibling of the source — this is the version relationship encoded into tumbler geometry. The cross-account case is indistinguishable at the allocator level from creating a brand-new document.

---

### Conclusion

`docreatenewversion` uses **no separate version-allocator record** analogous to `granf` for content or `spanf` for links. It dispatches through the same `granf` granfilade as `docreatenewdocument`, `docreatenode_or_account`, and every other structural allocation. The "version" relationship is encoded entirely through the `typehint`: by passing `DOCUMENT/DOCUMENT` with the source document's tumbler as `hintisa`, the allocator places the new version's address adjacent to the original in tumbler space. The granfilade's hierarchical tumbler geometry serves double duty as both the document registry and the version namespace.
