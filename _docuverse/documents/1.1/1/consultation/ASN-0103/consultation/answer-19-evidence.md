## Question 19 [evidence]

> Does CREATEDOCUMENT preserve every existing document's POOM, granfilade, and spanfilade state untouched, satisfying the F0 cross-document frame axiom?

## KB Synthesis

Yes — CREATEDOCUMENT satisfies F0 for all three structures, with one important qualifier on the granfilade.

**POOMs of existing documents: fully preserved.**
CREATEDOCUMENT allocates a new, empty document orgl via `createorglingranf`. It calls `findisatoinsertnonmolecule` to assign a fresh child address under the account, then initializes the new document's own POOM tree via `createenf`. No existing document's POOM tree is touched. This follows from the same isolation property documented for DELETE: `deletend` operates on a single orgl, and `createorglingranf` likewise writes only to the new orgl [FC-DELETE-CROSS-DOC].

**Spanfilade: fully preserved.**
No content is inserted and no link is created, so neither `insertspanf(..., DOCISPAN)` nor `insertendsetsinspanf` is called. The spanfilade is write-only and grows only via INSERT, COPY, and CREATELINK [INV-SPANF-WRITE-ONLY]. CREATEDOCUMENT triggers none of these.

**Granfilade: additive-only modification.**
CREATEDOCUMENT writes exactly one new entry to the granfilade — the new document's address. Like CREATENEWVERSION, it allocates a document address in a separate tumbler range from content I-addresses, so it does **not** break text I-address contiguity for subsequent INSERTs [INV-MONOTONIC, Finding 0077; FC-GRANF-ON-VERSION]. All existing content entries, link orgls, and document addresses remain unchanged.

**Summary:** CREATEDOCUMENT is in the same category as CREATENEWVERSION: *content-granfilade-preserving* but *document-granfilade-modifying* (one additive entry). No existing document's POOM is touched, no spanfilade entries change, and no existing granfilade entry is modified or removed. F0 holds across all existing documents [ST-ADDRESS-ALLOC], [FC-GRANF-ON-VERSION], [INV-MONOTONIC].

---

## Code Exploration

I now have the complete picture. Here is my full answer.

---

## Does CREATEDOCUMENT Satisfy the F0 Cross-Document Frame Axiom?

**Answer: Yes, with one important structural nuance to clarify.**

---

### Complete Execution Path

**`fns.c:276–286` — top-level handler:**
```c
void createnewdocument(typetask *taskptr)
{
    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
    else
        putrequestfailed (taskptr);
}
```
The handler parses the FEBE request and delegates entirely to `docreatenewdocument`.

---

**`do1.c:234–241` — the actual operation:**
```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

This is the entire body. **One function call only: `createorglingranf`.** No call to `insertspanf`. No call to `findorgl`. No `addtoopen`. The `hint` encodes `supertype=ACCOUNT`, `subtype=DOCUMENT`, `hintisa=taskptr->account` (the creating user's account tumbler).

---

**`granf1.c:50–55` — thin wrapper:**
```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr)
{
    return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

Passes straight through to `createorglgr` with the global `granf` pointer. `granf` and `spanf` are initialized in `entexit.c:44–45` as `createenf(GRAN)` and `createenf(SPAN)` respectively — two separate global enfilades.

---

**`granf2.c:111–128` — the creation kernel:**
```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typegranbottomcruminfo locinfo;

    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);    /* line 120 */
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        /* line 125 */
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

Three things happen here:

1. **`findisatoinsertgr` (`granf2.c:130–155`)** — since `hintptr->subtype == DOCUMENT` (not `ATOM`), this takes the `else` branch and calls `findisatoinsertnonmolecule`. That function reads the granfilade tree to find the last-allocated ISA under the account (`findpreviousisagr`), then increments to produce the new address. **Pure read traversal — no writes to existing crums.**

2. **`createenf(POOM)` (`granf2.c:120`)** — allocates a brand new, empty POOM enfilade. This is an entirely fresh allocation. It is not connected to any existing document's POOM in any way.

3. **`insertseq(fullcrumptr, isaptr, &locinfo)` (`granf2.c:125`, implemented in `insert.c:17–70`)** — inserts the new `GRANORGL` leaf into the shared global granfilade.

---

**`insert.c:17–70` — what insertseq modifies:**

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
{
    context = retrievecrums (fullcrumptr, address, WIDTH);  /* find insertion point */
    ptr = context->corecrum;
    new = createcrum (0,(INT)ptr->cenftype);                /* NEW crum allocation */
    adopt (new, RIGHTBRO, (typecorecrum*)ptr);              /* link into tree */
    splitsomething = splitcrumupwards (findfather (new));
    if (info->infotype == GRANORGL){
        info->granstuff.orglstuff.orglptr->leftbroorfather = new; /* line 50 */
    }
    moveinfo (info, &((typecbc *)new)->cinfo);              /* write to NEW crum */
    /* adjust cwid (cumulative-width) bookkeeping */
    tumblersub (..., &ptr->cwid.dsas[WIDTH]);               /* line 55: cwid of neighbor */
    setwispupwards (findfather ((typecorecrum*)ptr),0);
    setwispupwards (findfather ((typecorecrum*)new),1);
    splitsomething |= splitcrumupwards (findfather ((typecorecrum*)ptr));
    if(splitsomething) recombine (fullcrumptr);
}
```

The writes are precisely:
- **`new->cinfo`** — the newly-allocated crum gets the new document's `locinfo`. No existing crum's `cinfo` is touched.
- **`ptr->cwid.dsas[WIDTH]`** — the adjacent crum's cumulative-width metadata is adjusted. `cwid` is navigation bookkeeping, not document content. The `cinfo` of `ptr` (which holds an existing document's POOM pointer and disk pointer) is never touched.
- **Internal nodes' `cwid`** — via `setwispupwards`. Again, structural bookkeeping only.
- **`info->granstuff.orglstuff.orglptr->leftbroorfather = new`** (`insert.c:50`) — this sets the new POOM's root crum's `leftbroorfather` to the new granfilade leaf. This is initializing the new document's POOM infrastructure, not touching any existing POOM.

The `recombine` and `splitcrumupwards` calls may further restructure the granfilade tree, but these operations only rearrange which subtrees live under which internal nodes — they never write `cinfo` into existing GRANORGL bottom crums.

---

### Structure-by-Structure Verdict

| Structure | Modified by CREATEDOCUMENT? | Detail |
|---|---|---|
| **New document POOM** | Yes — created | Fresh `createenf(POOM)` at `granf2.c:120` |
| **Existing documents' POOMs** | **No** | Each POOM is a private, separate `createenf(POOM)` allocation. CREATEDOCUMENT never calls `findorgl` on any existing doc. |
| **Global granfilade (`granf`)** | Structurally yes; logically no | A new leaf is inserted and `cwid` bookkeeping adjusts. But no existing GRANORGL bottom crum's `cinfo` (POOM pointer, disk pointer, `orglincore` flag) is written. |
| **Global spanfilade (`spanf`)** | **No** | `docreatenewdocument` (`do1.c:234–241`) calls only `createorglingranf`. There is no `insertspanf` call anywhere in the CREATEDOCUMENT path. The spanfilade is untouched. |
| **BERT table** | **No** | No `addtoopen` or `checkforopen` is called during `docreatenewdocument`. No existing document's open state is affected. |

---

### Conclusion

**CREATEDOCUMENT satisfies the F0 cross-document frame axiom.**

The implementation is architecturally correct for frame preservation:

- Every document's POOM is a private `createenf(POOM)` allocation (`granf2.c:120`). These are not shared. CREATEDOCUMENT creates exactly one new POOM; existing POOMs are never referenced, never passed as arguments, never touched in memory.

- The global granfilade receives a new leaf, and the surrounding tree's `cwid` navigation metadata is recalculated. This is shared infrastructure bookkeeping. The logical state of every existing document — its ISA address, its POOM pointer, its disk location, its content — is preserved in the bottom crums' `cinfo` fields, and those fields are never written during CREATEDOCUMENT.

- The spanfilade is not touched at all. The absence of any `insertspanf` call in `docreatenewdocument` (`do1.c:239`) is explicit — a new document has no content and no links, so it has no spans to register.

The one thing CREATEDOCUMENT does change globally is the shared index tree's topology and `cwid` bookkeeping. If F0 is interpreted as requiring the shared index structure to be frozen in addition to per-document state, then it is technically violated by the `cwid` adjustments. But in the Xanadu model, the granfilade index is infrastructure, not part of any individual document's observable state. At the level of document content, virtual address spaces, and link endpoint sets, F0 holds exactly.
