## Question 15 [evidence]

> For a span that has been transcluded across N documents, does `find_documents_containing` return all N documents, and in what tumbler order — by document I-address ascending?

## KB Synthesis

## FINDDOCSCONTAINING: All N Documents, Sorted by Document I-Address

### Does it return all N documents?

Yes — and more. It returns a **superset** of the N currently-live documents.

**Why all N are included:** Each vcopy (transclusion) call goes through `docopy`, which calls `insertspanf(..., DOCISPAN)`, creating a DOCISPAN entry mapping the content's I-address range to the receiving document's ISA. This fires for every recipient of the transcluded content [SS-DOCISPAN, FC-CONTENT-SPANF-ISOLATION].

**Why the superset may be larger:** The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. No operation ever removes a DOCISPAN entry. So documents that once contained the span but have since deleted it are permanently indexed [INV-IADDRESS-PERMANENT]:

> `∀ D, α: α ∈ I-addresses-ever(D) ⟹ D ∈ FINDDOCSCONTAINING(α)`

This is confirmed explicitly by [EC-STALE-SPANF-REFERENCE]: `actual_docs(i) ⊆ find_documents(i)`. Post-delete, the POOM mapping is gone but the DOCISPAN entry persists — a "ghost reference." Callers must post-filter via I-to-V conversion (which silently drops unresolvable I-addresses per [INV-ITOV-FILTERING]) to determine which documents currently contain the content.

---

### What order — document I-address ascending?

Yes, ascending by document ISA (tumbler order).

The spanfilade is a 2D enfilade (SPAN type). All 2D enfilade retrievals use `incontextlistnd()`, which performs insertion-sort as contexts are discovered during B-tree traversal [SS-CONTEXT-LIST]:

> "Two distinct accumulation strategies exist: `incontextlistnd()` maintains sorted order by insertion-sort (used for N-dimensional enfilades where tree order does not guarantee V-order)..."

[INV-RETRIEVAL-V-SORTED] states the postcondition:

> "the result list is sorted by left boundary in the queried dimension"

For FINDDOCSCONTAINING, the query constrains the SPANRANGE dimension (I-address content range is fixed), and results are accumulated in the ORGLRANGE dimension (document ISAs). So sorting is by document I-address (ORGLRANGE left boundary) in ascending tumbler order.

The tumbler total order is lexicographic after exponent alignment [INV-TUMBLER-TOTAL-ORDER], meaning `1.1.0.1.0.1` < `1.1.0.1.0.2` < `1.1.0.2.0.1`, etc.

---

**Key caveat:** [INV-RETRIEVAL-TREE-INDEPENDENCE] confirms this ordering is independent of internal tree structure (splits, rebalances, insertion order), so the result set is deterministic regardless of operational history.

---

## Code Exploration

I now have all verified citations. Here is the complete answer.

---

## `find_documents_containing` — Full Code Trace

### Call Chain

```
finddocscontaining()          [fns.c:20]
  → dofinddocscontaining()    [do1.c:15]
      → specset2ispanset()    [do2.c — V-space → I-span conversion]
      → finddocscontainingsp() [spanf1.c:151]
          → retrieverestricted() → findcbcinarea2d() [retrie.c:252]
              → incontextlistnd()   [context.c:75]
          → onitemlist()           [orglinks.c:464]
```

---

### 1. Entry Point

`fns.c:20-32` — `finddocscontaining()`:

```c
void finddocscontaining(typetask *taskptr)
{
  typespecset specset;
  typelinkset addressset;
  bool getfinddocscontaining(), dofinddocscontaining();

    if (
       getfinddocscontaining (taskptr, &specset)
    && dofinddocscontaining (taskptr, specset, &addressset))
        putfinddocscontaining (taskptr, (typeitemset)addressset);
       else
        putrequestfailed (taskptr);
}
```

`do1.c:15-23` — `dofinddocscontaining()`:

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
  bool specset2ispanset(), finddocscontainingsp();

    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

The V-space spec is converted to I-space spans first, then the spanfilade query runs.

---

### 2. Does It Return All N Documents?

**Yes.** `spanf1.c:151-188` — `finddocscontainingsp()`:

```c
for (; ispanset; ispanset = ispanset->next) {                     // line 170 — no early exit
    context = retrieverestricted ((typecuc*)spanf, &docspace,
                ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);  // line 171
    for (c = context; c; c = c->nextcontext) {                    // line 172 — all contexts
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);    // line 173
        beheadtumbler (&docid, &document.address);                // line 174
        if (isinlinklist(*headptr, &document.address))            // line 175 — skip dups only
            continue;
        document.itemid = LINKID;
        document.next = NULL;
        addresssetptr = (typelinkset *) onitemlist(taskptr,       // line 179 — append
            (typeitem*)&document, (typeitemset*)addresssetptr);
    }
    contextfree (context);                                        // line 181
}
```

The outer loop processes every I-span in the input set without early exit. The inner loop processes every context returned from `retrieverestricted`. The only skips are exact-address duplicates via `isinlinklist`. All N document entries are collected.

The query is 2D: `docspace` bounds the ORGLRANGE (document I-address dimension), and `ispanset` restricts the SPANRANGE (content I-address dimension). Any spanfilade leaf whose content I-span overlaps the query and whose document I-address falls in doc-space is returned.

---

### 3. Tumbler Order — Ascending Document I-Address

**Yes, results are in ascending document I-address order.** The ordering is established deep inside `retrieverestricted` → `findcbcinarea2d`.

`retrie.c:252-264` — `findcbcinarea2d()`, at leaf nodes:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {          // line 252 — tree traversal
    ...
    if (crumptr->height != 0) {
        ...
        findcbcinarea2d (...);                              // line 259 — recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr,
                      (typewid*)offsetptr);                // line 262
        incontextlistnd (headptr, context, index1);        // line 263 — SORTED INSERT
    }
}
```

`context.c:74-111` — `incontextlistnd()` (comment from source: `"put c on clist in index order"`):

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    ...
    /* 1st insertion */
    if (!clist) { *clistptr = c; return(0); }

    /* on beginning */
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist; *clistptr = c; return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            /* in middle */
            if ((whereoncontext (clist, &grasp.dsas[index], ...) > ONMYLEFTBORDER)
             && (whereoncontext (nextc,  &grasp.dsas[index], ...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc;
                clist->nextcontext = c;
                return(0);
            }
        }
    }
    /* on end */
    clist->nextcontext = c;
}
```

`index1` passed at `retrie.c:263` is `ORGLRANGE` — the document I-address dimension. Each context from a spanfilade leaf is inserted into the sorted list by its ORGLRANGE offset (= document I-address). The comparisons are done by `whereoncontext()` → `intervalcmp()` via tumbler arithmetic (`context.c:124-148`).

By the time `retrieverestricted` returns, the context list is sorted in ascending document I-address order.

Back in `finddocscontainingsp`, `onitemlist` (`orglinks.c:464-537`) is a simple tail-append — it walks to the end of the list and appends (`orglinks.c:534`):

```c
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

Since the iteration over `context` at `spanf1.c:172` traverses the already-sorted context list in order, and `onitemlist` appends each to the tail of the result list, the final `addressset` preserves the ascending document I-address order.

---

### Summary

| Question | Answer |
|---|---|
| Returns all N documents? | **Yes** — no early exit in `finddocscontainingsp` [`spanf1.c:170-181`] |
| Duplicates? | Skipped by `isinlinklist` [`spanf1.c:175`]; cannot appear twice |
| Result order? | **Ascending document I-address** — enforced by `incontextlistnd`'s sorted insertion [`context.c:75`, `retrie.c:263`] with `index=ORGLRANGE` |
| Sorting mechanism | Insertion sort during enfilade traversal, not a post-pass sort |
| Multi-span input caveat | Results from successive `ispanset` elements are appended after the previous batch; each batch is internally sorted, but batches are not globally merged-sorted. For a single query span this is moot. |
