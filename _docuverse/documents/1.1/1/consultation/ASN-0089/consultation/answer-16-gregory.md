## Question 16 [gregory]

> The spanfilade DOCISPAN entry created by INSERT — does `insertspanf` record the document's I-address as the full `docISA` tumbler or just the document-level prefix, and does a single bulk INSERT of N bytes produce exactly one DOCISPAN entry covering the contiguous I-span?

## KB Synthesis

Both parts are directly answered by the KB.

**1. What `insertspanf` records for the document key**

The call is `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` [SS-DOCISPAN, Finding 0036]. The third argument is `docisaptr` — the full document ISA tumbler (e.g., `1.1.0.1.0.1`), not a truncated prefix. The DOCISPAN entry maps `(I-span) → docISA`, where docISA is the complete document address as used throughout the granfilade address space [SS-ADDRESS-SPACE, SS-LINK-HOME-DOCUMENT].

**2. How many DOCISPAN entries a single bulk INSERT produces**

Exactly one [SS-DOCISPAN, Finding 0047].

The call chain is: `doinsert` → `inserttextingranf` → `docopy` → `insertspanf(..., DOCISPAN)` [ST-INSERT, Finding 0036]. `inserttextingranf` allocates the N bytes as a single contiguous I-span (monotonic increment, `tumblerincrement(&lsa, 0, N, &lsa)` [ST-INSERT, Finding 0031]). `docopy` calls `specset2ispanset`, which returns 1 `typeispan` struct covering that contiguous range. `insertspanf` loops over the `ispanset` linked list making one `insertnd` call per `typeispan` [SS-DOCISPAN, Finding 0047]. Since there is one `typeispan`, there is one `insertnd` call and one DOCISPAN entry: `(α₁, width N) → docISA`.

The concrete example from Finding 0047 confirms:
```
INSERT "ABCDEFGHIJ" (10 bytes):
  inserttextingranf → 1 contiguous I-span {α₁, width 10}
  insertspanf → 1 insertnd call → 1 DOCISPAN entry
```

The number of DOCISPAN entries is O(number of operations), not O(bytes) [INV-SPANF-GROWTH]. For sequential single-character inserts, each insert individually produces 1 DOCISPAN entry, but the I-spans are contiguous in I-space (monotonic allocation [INV-MONOTONIC]), so they represent the same logical content range spread across N operations rather than 1 — still 1 entry per INSERT call, N entries total for N single-character inserts.

---

## Code Exploration

I now have everything needed to answer both questions definitively. Here is the full analysis:

---

## DOCISPAN Entry Structure in `insertspanf`

### Call Chain

```
fns.c:insert → do1.c:doinsert → do1.c:docopy → spanf1.c:insertspanf
```

`doinsert` [do1.c:117-122]:
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
    ...
```

`inserttextingranf` is a one-line wrapper [granf1.c:44-47]:
```c
bool inserttextingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typetextset textset, typeispanset *ispansetptr)
{  bool inserttextgr();
   return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
}
```

`docopy` [do1.c:53-63] calls:
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
...
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

---

## Question 1: Full `docISA` or just document-level prefix?

`insertspanf` [spanf1.c:15-53] begins:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, typesporglset sporglset, INT spantype)
{
  typedsp crumorigin;
  ...
  prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

`prefixtumbler` [tumble.c:641-651]:
```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
  tumbler temp1, temp2;
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;          // temp1 = DOCISPAN (4), single digit
    movetumbler (aptr, &temp2);        // temp2 = full docISA
    if (!iszerotumbler (&temp2))
        temp2.exp -= 1;                // shift docISA one digit position rightward
    tumbleradd (&temp1, &temp2, cptr); // result = DOCISPAN prepended to full docISA
}
```

**`DOCISPAN = 4`** [xanadu.h:39]. The result stored in `crumorigin.dsas[ORGLRANGE]` is `4.<fullDocISA>` — the full document ISA is retained as the suffix.

Then for ISPANID items (which is what `inserttextgr` produces), the bottom crum `homedoc` field is set [spanf1.c:29]:
```c
movetumbler (isaptr, &linfo.homedoc);
```
`type2dbottomcruminfo` [wisp.h:107-109] has exactly one field:
```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**Answer to Q1:** `insertspanf` records the **full `docISA` tumbler** — not a truncated prefix. The ORGLRANGE key is `prefixtumbler(docISA, DOCISPAN)` = `4.<fullDocISA>`, and `linfo.homedoc` separately stores the raw full `docISA`. The `DOCISPAN` (4) value is a category prefix, not a replacement for the document address.

---

## Question 2: Single bulk INSERT of N bytes → exactly one DOCISPAN entry?

**Step 1: `inserttextgr` collapses all text into one ispan.**

`inserttextgr` [granf2.c:83-109]:
```c
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
ispanptr = (typeispan *) taskalloc (taskptr, sizeof(typeispan));
ispanptr->itemid = ISPANID;
ispanptr->next = NULL;
movetumbler (&spanorigin, &ispanptr->stream);
tumblersub (&lsa, &spanorigin, &ispanptr->width);
*ispansetptr = ispanptr;
```

Regardless of how many `textset` chunks are passed, this always produces **exactly one `typeispan`** node: stream = start address, width = total accumulated length. The list has `next = NULL`.

**Step 2: `specset2ispanset` passes ISPANID items through unchanged.**

[do2.c:24-26]:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
```

ISPANID items are chained directly into the output, no transformation.

**Step 3: `insertspanf` iterates the ispanset and calls `insertnd` once per item.**

[spanf1.c:25-51]:
```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);
        movetumbler (&((typeispan *)sporglset)->width, &lwidth);
        movetumbler (isaptr, &linfo.homedoc);
    } ...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

Since the ispanset has exactly one item, the loop runs once, and `insertnd` is called once.

**Answer to Q2:** Yes — a single bulk INSERT of N bytes produces **exactly one DOCISPAN crum** in the spanfilade. The one crum's SPANRANGE key covers the entire contiguous I-span `[stream, stream+N)`, its ORGLRANGE key is `4.<fullDocISA>`, and its `homedoc` bottom-crum field holds the full docISA. This holds even when the client sends multiple `textset` chunks: `inserttextgr` folds them all into one ispan before `insertspanf` is ever called.
