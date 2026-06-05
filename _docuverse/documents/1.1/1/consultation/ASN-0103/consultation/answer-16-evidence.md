## Question 16 [evidence]

> Does CREATEDOCUMENT touch the granfilade at all, or does the granfilade's monotonic I-address high-water mark remain unchanged since no content molecules are stored?

## KB Synthesis

## CREATEDOCUMENT and the Granfilade

CREATEDOCUMENT **does** touch the granfilade, but it does **not** advance the content I-address high-water mark.

### Two Independent Allocation Functions

[SS-ADDRESS-SPACE] (Finding 0077) is explicit: the granfilade contains both document addresses and content I-addresses in separate tumbler ranges, served by two distinct allocation functions:

- `findisatoinsertmolecule` — content (text atoms, link orgls) → **advances content high-water mark**
- `findisatoinsertnonmolecule` — structural entities (documents, versions) → **does not advance content high-water mark**

Both query the same granfilade tree but search different subtrees: `next_doc_addr(granf, parent)` and `next_content_addr(granf, doc)` are independent families of counters.

CREATEDOCUMENT calls `findisatoinsertnonmolecule` (with depth=2 for account→document, per [SS-ADDRESS-ALLOC] Finding 0021). This writes a document orgl entry to the granfilade — it *does* modify the tree — but the search is bounded to the document address range, leaving the content molecule range untouched.

### Empirical Confirmation

[FC-GRANF-ON-VERSION] (Finding 0077) provides the clearest evidence via CREATENEWVERSION, which shares the same document-allocation step:

> INSERT "ABC" → CREATENEWVERSION → INSERT "XYZ" → `compare_versions` yields **1 shared span pair** (I-addresses contiguous: I.1–I.3, I.4–I.6)

Contrast with [INT-LINK-INSERT] (Finding 0063):

> INSERT "ABC" → CREATELINK → INSERT "DEF" → `compare_versions` yields **2 shared span pairs** (gap from link orgl allocation at intermediate I-address)

CREATELINK uses `createorglingranf` which goes through `findisatoinsertmolecule` (molecule path), advancing the content counter. CREATEDOCUMENT/CREATENEWVERSION use `findisatoinsertnonmolecule` (non-molecule path), leaving it unchanged.

### Summary

| Operation | Granfilade touched? | Content high-water mark |
|-----------|--------------------|-----------------------|
| INSERT | Yes (molecule) | Advanced |
| CREATELINK | Yes (molecule) | Advanced |
| CREATEDOCUMENT | Yes (non-molecule) | **Unchanged** |
| CREATENEWVERSION | Yes (non-molecule) | **Unchanged** |
| DELETE / REARRANGE | No | Unchanged |

[FC-GRANF-ON-VERSION] captures the operation classification: "content granfilade unchanged, document granfilade modified." The content I-address monotonic sequence is partitioned by tumbler range, so document-level allocations are invisible to subsequent text insertions — they will still get the next contiguous I-addresses as if CREATEDOCUMENT had never occurred.

---

## Code Exploration

All line numbers confirmed. Here is the full answer.

---

## CREATEDOCUMENT and the Granfilade

**Short answer:** CREATEDOCUMENT absolutely touches the granfilade. It inserts a new ORGL crum, and the WIDTH span fields throughout the granfilade tree are rewritten as a direct consequence. The monotonic I-address high-water mark advances.

---

### Call Chain

```
fns.c:276       createnewdocument()
do1.c:234       docreatenewdocument()
granf1.c:50     createorglingranf()
granf2.c:111    createorglgr()
granf2.c:117      findisatoinsertgr()       ← allocates a new I-address
granf2.c:125      insertseq()               ← writes it into the granfilade tree
```

---

### Step 1 — Entry: `fns.c:276`

```c
void createnewdocument(typetask *taskptr)
{
    typeisa newdocisa;
    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
    else
        putrequestfailed (taskptr);
}
```

`requestfns[CREATENEWDOCUMENT]` is wired to this function at `init.c:52`.

---

### Step 2 — Implementation: `do1.c:234`

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

Key: `makehint` is called with `supertype=ACCOUNT`, `subtype=DOCUMENT`. The hint's `hintisa` is the caller's account I-address. This is passed directly to `createorglingranf` with the **global** `granf` pointer — the one and only granfilade.

No `findorgl()` call here. No lookup of existing documents. This is a pure creation path.

---

### Step 3 — ORGL insertion: `granf2.c:111`

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr,
                  typehint *hintptr, typeisa *isaptr)
{
    typegranbottomcruminfo locinfo;

    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   /* new POOM */
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);       /* ← HERE */
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

`granf2.c:125` — `insertseq` is called with the granfilade root, the freshly allocated I-address, and a `GRANORGL` info block. This is the granfilade write.

---

### Step 4 — I-address allocation: `granf2.c:130`

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        ...
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        /* DOCUMENT, ACCOUNT, NODE take this branch */
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);  /* line 152 */
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

Because `hintptr->subtype == DOCUMENT` (set in `do1.c:239`), the ATOM branch is skipped. `findisatoinsertnonmolecule` (`granf2.c:203`) scans to find the highest existing I-address under the account tumbler, then increments past it. The result written into `*isaptr` is the new document's permanent I-address.

---

### Step 5 — Width rewrite: `insert.c:17`

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
{
    ...
    context = retrievecrums (fullcrumptr, address, WIDTH);   /* line 28 */
    ptr = context->corecrum;
    ...
    /* create new crum, adopt as RIGHTBRO of ptr */
    new = createcrum (0,(INT)ptr->cenftype);
    adopt (new, RIGHTBRO, (typecorecrum*)ptr);
    ...
    if (iszerotumbler (&ptr->cwid.dsas[WIDTH])) {  /* last crum in granf — line 53 */
        tumblerclear (&new->cwid.dsas[WIDTH]);                       /* line 54 */
        tumblersub (&nextaddress, &offset.dsas[WIDTH],
                    &ptr->cwid.dsas[WIDTH]);                         /* line 55 */
    } else {
        dspadd (&offset, &ptr->cwid, &reach, GRAN);                  /* line 57 */
        tumblersub (&reach.dsas[WIDTH], &nextaddress,
                    &new->cwid.dsas[WIDTH]);                         /* line 58 */
        tumblersub (&nextaddress, &offset.dsas[WIDTH],
                    &ptr->cwid.dsas[WIDTH]);                         /* line 59 */
    }
    ivemodified ((typecorecrum*)ptr);
    setwispupwards (findfather ((typecorecrum*)ptr),0);              /* line 62 */
    setwispupwards (findfather ((typecorecrum*)new),1);              /* line 63 */
    ...
}
```

The `cwid.dsas[WIDTH]` field is the span width in the I-address dimension. Two things happen here that directly answer the question:

**Case A — new document is the first entry (or is appended past the current last crum):** `ptr->cwid.dsas[WIDTH]` is zero (the "open-ended" sentinel meaning "extends to infinity"). After insertion:
- `new->cwid.dsas[WIDTH]` ← 0 (new crum becomes the new open-ended tail, `insert.c:54`)
- `ptr->cwid.dsas[WIDTH]` ← `nextaddress − offset` (the previously open-ended crum is now bounded to stop at the new document's I-address, `insert.c:55`)

**Case B — new document is inserted between existing entries:** Both old and new crums get their WIDTH fields recalculated (`insert.c:57–59`).

In both cases, `setwispupwards` (`insert.c:62–63`) walks from the modified crums up to the root, recomputing cumulative WIDTH sums at every level. The root's WIDTH reflects the total I-address span of all entries in the granfilade.

---

### Summary

| Question | Answer |
|----------|--------|
| Does CREATEDOCUMENT touch the granfilade? | **Yes.** `insertseq` writes a new `GRANORGL` crum into the granfilade tree. |
| Does the high-water mark advance? | **Yes.** The new document occupies a freshly allocated I-address (`findisatoinsertnonmolecule`). `insertseq` rewrites `cwid.dsas[WIDTH]` at the affected leaf and propagates the change to the root via `setwispupwards`. |
| Does it touch content molecules (text)? | **No.** The `ATOM` branch in `findisatoinsertgr` (`granf2.c:135`) is not taken. `findisatoinsertmolecule` and `inserttextgr` are not called. |
| Is `findorgl` called? | **No.** Document creation does not look up any existing ORGL. That lookup appears in `docreatenewversion` (`do1.c:266`) but not here. |

CREATEDOCUMENT's granfilade footprint is exactly one new ORGL crum at a new I-address, plus the WIDTH bookkeeping cascaded up the tree. No content molecules are stored, but the address space is permanently extended.
