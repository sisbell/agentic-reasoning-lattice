## Question 16 [evidence]

> What is the iteration order of returned documents — sorted by document ISA, by DOCISPAN insertion order in the spanfilade, or by some 2D-enfilade traversal order — and is the order stable across sessions?

## KB Synthesis

## Iteration Order for FINDDOCSCONTAINING

The KB is explicit enough to answer this, but the answer requires synthesizing several findings.

### What determines order: `incontextlistnd()` insertion-sort

All retrieval from 2D enfilades (SPAN, POOM) goes through `incontextlistnd()`, which performs an **insertion-sort by left boundary in the accumulated dimension** [SS-CONTEXT-LIST]. The spanfilade is a 2D enfilade (type SPAN, confirmed in [SS-DUAL-ENFILADE] Finding 0012: `spanf = createenf(SPAN)`).

For the SPAN enfilade, dimension layout is: `dsas[0]` = ORGLRANGE (document/link ISA), `dsas[1]` = SPANRANGE (I-address content) [SS-ENFILADE-TREE] Finding 0071. FINDDOCSCONTAINING restricts on SPANRANGE (the I-address query) and accumulates results in ORGLRANGE (document ISA). The sort key in `incontextlistnd` is `totaloffset.dsas[index]` for the accumulation dimension — here, **document ISA in ascending tumbler order**.

This is **not** DOCISPAN insertion order. The insertion-sort explicitly overrides whatever order the B-tree traversal discovers entries in.

### Tree structure and insertion order do not matter

[INV-RETRIEVAL-TREE-INDEPENDENCE] is explicit: "The V-ordering of retrieval results is independent of the internal B-tree structure. Even if split/rebalance operations or out-of-order insertions produce a tree where sibling order does not match V-address order, the `incontextlistnd` insertion-sort re-establishes ordering during retrieval."

The 2D rebalancing algorithm sorts children by diagonal key (`dsas[0] + dsas[1]`) [SS-ENFILADE-TREE] Finding 0071, which determines tree shape — but `incontextlistnd` discards this traversal order and re-sorts.

### Stability across sessions

The sort is deterministic: ascending by document ISA tumbler value via `tumblercmp` [INV-TUMBLER-TOTAL-ORDER]. For the same set of indexed documents, the order is identical across sessions.

However, the spanfilade is append-only [INV-SPANF-WRITE-ONLY]. New transclusions add DOCISPAN entries for new documents, expanding the result set. The **relative order of previously-returned documents is preserved**, but new documents are interleaved at their ISA-sorted position.

There is one additional complication: [EC-STALE-SPANF-REFERENCE] — deleted content leaves stale DOCISPAN entries. These stale documents still appear in the sorted result, in ISA order, mixed with live results. The caller must post-filter via I-to-V conversion [INV-ITOV-FILTERING].

### Summary

| Question | Answer |
|---|---|
| Sort basis | Document ISA ascending (tumbler total order) |
| Determined by | `incontextlistnd()` insertion-sort, not insertion order or tree traversal |
| Stable within session | Yes |
| Stable across sessions | Yes, for same document set; expands monotonically as new transclusions occur |
| Includes stale entries | Yes — spanfilade never shrinks; deleted-content documents remain in results |

---

## Code Exploration

Now I have the complete picture from the source code. Here is the full answer:

---

## Document Iteration Order in udanax-green

### Short Answer

Documents returned by `finddocscontainingsp` are **sorted by document ISA** — which equals **creation/insertion order within an account** — not by spanfilade tree shape or 2D-enfilade traversal order. The ordering is **stable across sessions**.

---

### 1. The Call Chain

`finddocscontainingsp` (`spanf1.c:151`) is the function that builds the document list. Its loop at `spanf1.c:170-181`:

```c
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        ...
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
    contextfree (context);
}
```

The critical index argument to `retrieverestricted` is **`ORGLRANGE`** as `index1` (`spanf1.c:171`). This flows into `retrieveinarea` (`retrie.c:87`) → `findcbcinarea2d` (`retrie.c:229`).

### 2. Where Ordering Is Imposed: `incontextlistnd`

Inside `findcbcinarea2d` (`retrie.c:252-264`), every time a qualifying leaf is found:

```c
context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd (headptr, context, index1);   /* retrie.c:263 */
```

`incontextlistnd` (`context.c:75-111`) does a **sorted insertion by position in the `index1` dimension** — here ORGLRANGE:

```c
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist;
    *clistptr = c;         /* insert at front if before current head */
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        if ((whereoncontext (clist, ...) > ONMYLEFTBORDER)
         && (whereoncontext (nextc, ...) < ONMYLEFTBORDER)) {
            c->nextcontext = nextc;
            clist->nextcontext = c;  /* insert in middle */
        }
    }
    clist->nextcontext = c;   /* append at end */  /* context.c:110 */
}
```

The result list is **sorted ascending by ORGLRANGE value**. This is the 2D-enfilade axis that encodes the document's position in the document-space. The traversal order of the 2D tree is irrelevant because `incontextlistnd` re-sorts regardless.

GRAN-based retrieval (`findcbcseq`, `findcbcinspanseq`) uses **`oncontextlistseq`** (`context.c:113-123`) instead — pure append in tree-left-to-right order — but `finddocscontainingsp` never calls those; it calls `retrieverestricted` which dispatches to `findcbcinarea2d` for SPAN enfilades (`retrie.c:94-98`).

### 3. ORGLRANGE = Document ISA

When a document span is inserted into the spanfilade via `insertspanf` (`spanf1.c:15`):

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  /* spanf1.c:22 */
```

The ORGLRANGE coordinate is the document's ISA prefixed with the span-type code (DOCISPAN). When `finddocscontainingsp` reads back `c->totaloffset.dsas[ORGLRANGE]` and strips the prefix via `beheadtumbler` (`spanf1.c:174`), what remains is the bare document ISA.

So: **sorting by ORGLRANGE = sorting by document ISA**.

### 4. ISA Assignment Is Monotonically Increasing

`findisatoinsertnonmolecule` (`granf2.c:203-241`) assigns ISAs by:

1. Calling `findpreviousisagr` (`granf2.c:255-278`) to locate the highest existing ISA under the hint
2. If nothing exists: produces `hintisa.0.1` (`granf2.c:237`)
3. If something exists: truncates to `hintlength + depth` then increments (`granf2.c:239-240`):

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   /* first child */
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

Each new document gets an ISA **strictly greater** than all prior documents under the same account. **ISA order = creation/insertion order** within an account.

### 5. Session Stability

The ordering depends on:
- ORGLRANGE values encoded in spanfilade leaf nodes — persisted on disk
- `incontextlistnd`'s comparison using `tumblercmp` on tumbler values — deterministic arithmetic

There is no heap-pointer comparison, no random seed, no memory-layout-dependent sort. The tree is loaded from disk via explicit pointer chains (`findleftson`, `getrightbro`) in `findpreviousisagr` (`granf2.c:267`). Given identical on-disk state, the same traversal produces the same sorted list.

**Order is stable across sessions.**

---

### Summary Table

| Question | Answer | Key evidence |
|---|---|---|
| Iteration order | Sorted ascending by document ISA | `incontextlistnd` called with `ORGLRANGE` index: `retrie.c:263`, `context.c:75-111` |
| ISA vs. insertion order | They are equivalent | `findisatoinsertnonmolecule` always increments past previous max: `granf2.c:235-241` |
| Spanfilade traversal order matters? | No — `incontextlistnd` re-sorts regardless | `context.c:90-110` does position-based sorted insert |
| GRAN enfilades | Sequential append order (left-to-right tree walk) | `oncontextlistseq` at `retrie.c:323`, `context.c:113-123` — but not used for doc lookups |
| Stable across sessions? | Yes | ORGLRANGE values are disk-persisted; no memory-layout dependence |
