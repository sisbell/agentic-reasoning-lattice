## Question 3 [evidence]

> When COPY places content into a document that already has a recorded reference to that I-address (e.g., re-copying previously deleted transcluded material), does udanax-green skip the provenance/reference recording step or emit it redundantly?

## KB Synthesis

The KB is explicit on this: COPY **always emits DOCISPAN entries redundantly** — there is no skip or deduplication logic anywhere in the path.

The evidence converges from several independent angles:

**No duplicate check at the COPY level.** [PRE-COPY] (Finding 0046) states explicitly: "`docopy()` performs NO duplicate checking before inserting V→I mappings into the target document's POOM." `isanextensionnd()` checks only whether new content is contiguous with an existing crum — never whether the I-address is already indexed in the spanfilade.

**No deduplication at the spanfilade insertion level.** [ST-COPY] / [SS-DOCISPAN] (Finding 0047) describe the call chain: `docopy → insertspanf(..., DOCISPAN)`, which loops over the ispanset and calls `insertnd` once per `typeispan`. There is no guard of the form "if this (I-address, doc) pair already exists, skip." The 2D spanfilade's `insertnd` adopts new crums as RIGHTBRO siblings without consulting whether an equivalent mapping already exists [SS-ENFILADE-TREE, Finding 0041].

**The spanfilade is structurally incapable of deduplication.** [INV-SPANF-WRITE-ONLY] (Finding 0057) establishes that the spanfilade is append-only: no `deletespanf` or equivalent function exists. Since there is no removal, there can be no "check-and-replace" — the only possible outcome of a second COPY is a second entry. [INV-SPANF-GROWTH] (Finding 0047) formalizes this: `|DOCISPAN| ≤ Σ_{all INSERT/COPY ops} |ispanset(op)|`, which counts operations, not unique (I-address, doc) pairs.

**Observable consequence.** [EC-STALE-SPANF-REFERENCE] (Finding 0057) and [INT-DELETE-SPANF-DIVERGENCE] note that `FIND_DOCUMENTS` returns a *superset* of currently-live references precisely because stale and duplicate entries accumulate. The formal invariant is `actual_docs(i) ⊆ find_documents(i)` — the reverse inclusion fails, meaning the index grows without bound relative to live POOM state.

**Summary:** When COPY re-places an I-address that the spanfilade already records for the target document, a duplicate DOCISPAN entry is emitted unconditionally. FIND_DOCUMENTS continues to work correctly (it returns the document regardless), but at the cost of unbounded index growth proportional to re-copy operations rather than unique content placements.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## Answer: udanax-green emits the spanfilade reference redundantly

There is no deduplication guard in the COPY insertion path. When the same I-address is inserted into a document that already has a recorded reference to it, a second crum is unconditionally created in the spanfilade. The only deduplication that exists operates at *query* time, not insertion time.

---

### Execution path through `docopy`

`copy` → `docopy` → `insertpm` + `insertspanf` [`do1.c:53–64`]:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   /* POOM */
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN) /* spanfilade */
&& asserttreeisok(docorgl)
```

The question is entirely about `insertspanf` and whether it skips the second call when the `(I-span, document)` pair already exists.

---

### Fact 1: Deletion does NOT clear the spanfilade

`dodeletevspan` [`do1.c:158–167`]:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
/*&& TRUE*/ /* ht stuff */
```

There is no `deletend` on `spanf`, no `deletespanf`, nothing. After a delete, the original `(I-span → document)` entry in the spanfilade survives intact. When the "previously deleted transcluded material" is re-copied, the first recording is still present.

---

### Fact 2: `insertspanf` has no pre-check

`insertspanf` [`spanf1.c:15–53`] iterates the sporglset and calls `insertnd` unconditionally for every I-span:

```c
for (; sporglset; sporglset = ...) {
    ...
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width,  &lwidth);
    movetumbler (isaptr, &linfo.homedoc);
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

There is no lookup of the existing spanfilade before this call. There is no "already recorded?" guard.

---

### Fact 3: `insertcbcnd`'s sole merge test is adjacency, not identity

Inside `insertnd` → `insertmorend` → `insertcbcnd` [`insertnd.c:242–275`], the only path that avoids creating a new crum is `isanextensionnd` returning TRUE:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        ...
        return(FALSE);         /* extended existing crum, no new one */
    }
}
/* falls through — new crum created unconditionally */
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
```

`isanextensionnd` [`insertnd.c:301–309`]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must both be true:
1. Same `homedoc` (same document ISA) — this would be satisfied
2. New span's origin == `reach` (right edge of the existing crum) — **adjacency**, not identity

For a re-copy of the same I-span, the new origin equals the *start* of the existing entry, not its right edge. `lockeq(reach, origin)` is FALSE. The branch is not taken. `createcrum` / `reserve` / `adopt` proceed unconditionally, creating a **duplicate crum** in the spanfilade.

---

### Fact 4: `recombine` is structural, not semantic

`recombinend` [`recombine.c:104–131`] is a B-tree balancing pass. It calls `getorderedsons` (sorts children by diagonal sum of `dsp[0]+dsp[1]` [`recombine.c:296–299`]) and redistributes children between underfull sibling nodes via `takeovernephewsnd` / `eatbrossubtreend`. It never inspects the *content* (span addresses and homedoc) of two crums for equality. Duplicate crums are invisible to it.

---

### Fact 5: Query-time deduplication exists but insertion-time deduplication does not

`finddocscontainingsp` [`spanf1.c:170–181`] does guard against emitting the same document ISA twice in its result:

```c
if (isinlinklist(*headptr, &document.address))
    continue;
```

This means the redundant spanfilade entry is silently suppressed at *query* time when building the list of documents containing a given I-span. But the underlying spanfilade still holds two crums for the same `(I-span, document)` pair.

---

### Summary

| Layer | Behavior |
|-------|----------|
| `dodeletevspan` | Does **not** remove spanfilade entries — they survive deletion |
| `insertspanf` | No pre-check; calls `insertnd` unconditionally for every I-span |
| `insertcbcnd` → `isanextensionnd` | Only merges **adjacent** (contiguous) spans; does not detect identical/overlapping spans |
| `recombinend` | Structural B-tree rebalancing only; no content-semantic deduplication |
| `finddocscontainingsp` (query) | Deduplicates at read time via `isinlinklist` |

**Conclusion:** udanax-green **emits the provenance reference redundantly**. The provenance/reference recording step in `insertspanf` is unconditional. After a delete-then-recopy cycle, the spanfilade contains two crums mapping the same I-span to the same document ISA. The system tolerates this because `finddocscontainingsp` deduplies at query time, but the storage itself accumulates duplicate provenance records.
