## Question 13 [evidence]

> Given that DOCISPAN entries are created per contiguous I-span at insertion time, how does FINDDOCSCONTAINING handle a query I-span that crosses multiple DOCISPAN boundaries within a single target document — one result or multiple?

## KB Synthesis

The KB doesn't give a direct answer for FINDDOCSCONTAINING, but the behavior can be inferred from three converging sources.

**DOCISPAN storage is per-span, not per-document** [SS-DOCISPAN]: `insertspanf` makes one `insertnd` call per `typeispan` struct, with no merging across separate INSERT/COPY operations. Two insertions into the same document create two independent DOCISPAN entries in the spanfilade. A query I-span crossing both boundaries intersects both entries.

**The accumulation function never deduplicates** [SS-CONTEXT-LIST]: `incontextlistnd()` — which handles N-dimensional enfilades like SPAN — performs insertion-sort and "never replaces existing entries." Each matching leaf node (each DOCISPAN entry) is accumulated independently into the result list. There is no document-identity check that would collapse two hits on the same DocISA into one.

**The analogue: link fragmentation produces duplicates** [EC-PIVOT-LINK-FRAGMENTATION]: After a pivot that fragments a link's endset, the same link appears in `find_links` results twice. This demonstrates directly that the spanfilade search + accumulation pipeline does not deduplicate by entity identity — it returns one result per matching spanfilade entry.

**Conclusion:** When a query I-span crosses *k* DOCISPAN boundaries within a single target document, FINDDOCSCONTAINING returns that document *k* times — once per overlapping DOCISPAN entry. The spanfilade provides no read-side deduplication. Callers relying on distinct document counts must deduplicate the result themselves, consistent with [EC-STALE-SPANF-REFERENCE]'s note that `find_documents` returns a superset (already accounting for stale entries that further inflate results beyond live content).

---

## Code Exploration

The code is confirmed. Here is the full answer with direct source citations.

---

## How FINDDOCSCONTAINING Handles a Query I-Span Crossing Multiple DOCISPAN Boundaries

**Answer: The document appears exactly once in the result set, regardless of how many DOCISPAN entries it matches.**

---

### The Implementation

`finddocscontainingsp` at `backend/spanf1.c:151-188` is the actual handler (`FINDDOCSCONTAINING` opcode 22 dispatches here via `init.c:59`).

```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
  tumbler docid;
  typecontext *context, *c;
  typelinkset *headptr;
  typelink document;
  typespan docspace;
  ...
  headptr = addresssetptr;              /* spanf1.c:165 — stable anchor to result list head */
  *addresssetptr = NULL;                /* spanf1.c:166 — initialize output as empty */
  clear (&docspace, sizeof(typespan));
  tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream); /* spanf1.c:168 */
  tumblerincrement (&docspace.width, 0, 1, &docspace.width);          /* spanf1.c:169 */

  for (; ispanset; ispanset = ispanset->next) {         /* spanf1.c:170 */
      context = retrieverestricted((typecuc*)spanf,
                    &docspace, ORGLRANGE,               /* constrain to DOCISPAN range */
                    ispanset, SPANRANGE,                /* query I-span */
                    (typeisa*)NULL);                    /* spanf1.c:171 */
      for (c = context; c; c = c->nextcontext) {        /* spanf1.c:172 */
          movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);   /* spanf1.c:173 */
          beheadtumbler(&docid, &document.address);               /* spanf1.c:174 */
          if (isinlinklist(*headptr, &document.address))           /* spanf1.c:175 */
              continue;                                            /* spanf1.c:176 — SKIP dup */
          document.itemid = LINKID;
          document.next = NULL;
          addresssetptr = (typelinkset *) onitemlist(taskptr,
              (typeitem*)&document, (typeitemset*)addresssetptr);  /* spanf1.c:179 */
      }
      contextfree(context);                                        /* spanf1.c:181 */
  }
  return (TRUE);
}
```

---

### How Deduplication Works

**Step 1 — retrieverestricted returns one context entry per matching DOCISPAN node.**

A query I-span crossing two DOCISPAN entries for the same document yields two context entries from `retrieveinarea`. There is no deduplication at the retrieval layer (`retrie.c`).

**Step 2 — beheadtumbler strips the DOCISPAN prefix, leaving the bare document ISA.**

At `spanf1.c:173-174`, the ORGLRANGE coordinate encodes `[DOCISPAN-prefix | document-ISA]`. `beheadtumbler` removes the high-order component, producing the same `document.address` value for every DOCISPAN entry belonging to the same document.

**Step 3 — isinlinklist checks before adding.**

```c
/* backend/spanf2.c:16-23 */
bool isinlinklist(typelinkset linkset, typeisa *linkisaptr)
{
    for (; linkset; linkset = linkset->next) {
        if (tumblereq(&linkset->address, linkisaptr))
            return (TRUE);
    }
    return (FALSE);
}
```

This walks the accumulated result list from `*headptr` (the stable list head, saved at `spanf1.c:165`) and does a tumbler equality check. When the second context for the same document arrives, `tumblereq` matches, `isinlinklist` returns TRUE, and `continue` at `spanf1.c:176` skips the duplicate before `onitemlist` is ever called.

---

### Why `headptr` vs `addresssetptr`

After the first item is added, `addresssetptr` is reassigned to point to the last-added item (`spanf1.c:179`), which allows `onitemlist` to append in O(1) without rescanning from the head. But `headptr` was saved at `spanf1.c:165` and never moves — it always resolves via `*headptr` to the caller's list-head variable. The `isinlinklist` check at line 175 uses `*headptr`, not `*addresssetptr`, so it always walks the full result list from the beginning, ensuring no duplicate can slip through.

---

### Summary

When a query I-span crosses N DOCISPAN boundaries within a single target document:
- `retrieverestricted` returns N context entries for that document (`spanf1.c:171`)
- The first entry passes `isinlinklist` (list is empty), and the document is added (`spanf1.c:175-179`)
- Each subsequent entry hits `tumblereq` in `isinlinklist` (`spanf2.c:19`), returns TRUE, and is skipped (`spanf1.c:176`)
- **The document appears exactly once in the final result** — document-level deduplication is unconditional and built into the innermost loop of `finddocscontainingsp`
