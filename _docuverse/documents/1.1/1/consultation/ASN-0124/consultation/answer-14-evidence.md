## Question 14 [evidence]

> Is partial overlap sufficient for a document to be returned — that is, if a document's DOCISPAN entry shares even a single I-address position with the queried sporgl set, is it included, or must the document contain the full queried I-span?

## KB Synthesis

## Partial Overlap Is Sufficient

Yes, partial I-address overlap is sufficient. A document is returned by `FINDDOCSCONTAINING` if any I-address in the queried range intersects a DOCISPAN entry for that document — full containment of the queried span is not required.

### Evidence from the KB

**The spanfilade uses range intersection, not containment.** [SS-DOCISPAN] describes DOCISPAN entries as `Map<ISpan, DocISA>`, where each entry records a contiguous I-address range placed into a document. The spanfilade 2D search (`retrieverestricted`, `findcbcinarea2d`) classifies candidate crums using `intervalcmp` [SS-INTERVAL-CMP], which returns `THRUME` for interior hits, `ONMYLEFTBORDER`/`ONMYRIGHTBORDER` for boundary hits, and only `TOMYLEFT`/`TOMYRIGHT` for non-overlapping cases. Any intersection — even a single I-address at a boundary — is treated as a match.

**Confirmed by the find_links parallel.** `find_links` and `FINDDOCSCONTAINING` both query the spanfilade using the same `retrievesporglsetinrange()` infrastructure [SS-RETRIEVE-ENDSETS], [SS-SPORGL-LINK-INDEX]. For find_links, [SS-FIND-LINKS] Finding 0028 states explicitly: "Partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link." The same range-intersection logic governs DOCISPAN queries.

**Transclusion confirms partial-overlap semantics.** [INT-TRANSCLUSION] Finding 0018 shows that `FINDDOCSCONTAINING` finds documents that hold only a *subset* of the queried content's I-addresses. If document B vcopy'd only a few characters from a larger document A, searching on A's full I-span still returns B — because B's DOCISPAN entry covers the sub-range it actually holds, and that sub-range intersects the query.

**Stale reference behavior further confirms it.** [EC-STALE-SPANF-REFERENCE] Finding 0057 shows that after partial deletion, `FIND_DOCUMENTS(α₁..α₅)` still returns the deleted-from document alongside intact holders. The stale DOCISPAN entry for a sub-range of α₁..α₅ is sufficient for inclusion.

**Deletion of part of a range doesn't remove discovery.** [INV-IADDRESS-PERMANENT] Finding 0023 establishes that even after a document deletes content at certain I-addresses, `find_documents` continues to include it — the DOCISPAN entry for whatever I-span was originally placed persists unchanged [INV-SPANF-WRITE-ONLY].

### Formal statement

The postcondition of `FINDDOCSCONTAINING(query_ispan)` is:

```
result = { D | ∃ entry ∈ DOCISPAN : entry.doc = D ∧ entry.ispan ∩ query_ispan ≠ ∅ }
```

Because DOCISPAN is append-only and the spanfilade uses intersection matching, this is a *superset* of documents currently containing the I-addresses: `actual_docs(query_ispan) ⊆ result` [EC-STALE-SPANF-REFERENCE]. The KB contains no evidence of any containment predicate or minimum-overlap threshold beyond `≠ ∅`.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## Answer: Partial Overlap Is Sufficient

**A document is returned if any single I-address position in its DOCISPAN entry intersects the queried I-span.** The backend uses an overlap (intersection) test, not a containment test. A document need not contain the full queried I-span.

---

## Call Chain

The FEBE `finddocscontaining` command dispatches through:

```
fns.c:20  finddocscontaining()
  → do1.c:15  dofinddocscontaining()
      → do2.c:14  specset2ispanset()   [converts vspecs to I-spans]
      → spanf1.c:151  finddocscontainingsp()
          → retrie.c:56  retrieverestricted()
              → retrie.c:87  retrieveinarea()
                  → retrie.c:229  findcbcinarea2d()
                      → retrie.c:270  crumqualifies2d()   ← **THE GATE**
```

---

## The Spanfilade Structure

`insertspanf` [`spanf1.c:15`] records every I-span insertion as a 2-D crum in the spanfilade:

```c
// spanf1.c:22-51
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // dim 0: docISA with DOCISPAN prefix
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);            // dim 1: I-span start
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);             // dim 1: I-span width
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

`ORGLRANGE = 0`, `SPANRANGE = 1` [`wisp.h:15-16`].  
`DOCISPAN = 4` [`xanadu.h:39`].

Each crum thus carries `(docISA @ DOCISPAN, I-span)` in two independent dimensions.

---

## The Query in `finddocscontainingsp`

```c
// spanf1.c:167-172
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // [DOCISPAN, DOCISPAN+1)
tumblerincrement (&docspace.width,  0, 1,        &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
```

Two constraints are applied simultaneously:
- **span1** (ORGLRANGE, `index1`): restrict to crums tagged `DOCISPAN` — selects only document-membership entries, not link-endpoint entries.
- **span2** (SPANRANGE, `index2`): restrict to the queried I-span set.

---

## The Overlap Gate: `crumqualifies2d`

This function [`retrie.c:270`] is called on every crum during the tree walk. The crum is included only if it passes both span checks. The SPANRANGE check (the one that governs the I-space question) is:

```c
// retrie.c:292-300
endcmp = iszerotumbler (span2end) ? TOMYRIGHT
       : whereoncrum (crumptr, offset, span2end, index2);
if ( endcmp < ONMYLEFTBORDER)/* <= was < 12/20/84 */
    return(FALSE);

startcmp = whereoncrum (crumptr, offset, span2start, index2);
if( (startcmp > THRUME))
    return (FALSE);
```

The constants are [`common.h:86-90`]:

| Symbol | Value | Meaning |
|--------|-------|---------|
| `TOMYLEFT` | -2 | address strictly left of crum |
| `ONMYLEFTBORDER` | -1 | address at crum's left endpoint |
| `THRUME` | 0 | address strictly inside crum |
| `ONMYRIGHTBORDER` | 1 | address at crum's right endpoint |
| `TOMYRIGHT` | 2 | address strictly right of crum |

**Failure conditions for SPANRANGE:**

1. `endcmp < ONMYLEFTBORDER` → `endcmp == TOMYLEFT (-2)` → query end is **strictly left** of the crum's span start. (The query is entirely before this crum.)
2. `startcmp > THRUME` → `startcmp ∈ {ONMYRIGHTBORDER, TOMYRIGHT}` → query start is **at or past** the crum's span right boundary. (The query begins where this crum ends, or after.)

**A crum passes if and only if:**
- Query end is NOT strictly left of the crum start (i.e., query end ≥ crum start), **and**
- Query start is NOT at or past the crum end (i.e., query start < crum end strictly).

This is the standard half-open interval overlap condition: `query_start < crum_end AND crum_start ≤ query_end`. Any non-empty intersection — including a single shared boundary point — satisfies it.

### The 12/20/84 boundary change

The inline comment `/* <= was < 12/20/84 */` at `retrie.c:293` records a deliberate loosening of the boundary: the old code used `<= ONMYLEFTBORDER`, which would have **rejected** a query whose end exactly touched the crum's left boundary (zero-width contact). The current code uses `< ONMYLEFTBORDER`, which **accepts** that case. The system was intentionally made to include even single-point boundary overlaps.

The symmetric ORGLRANGE check at line 283 uses `<=/*=*/`, the `/*=*/` comment indicating an earlier debate about the `=` component. The SPANRANGE check was definitively settled more permissively.

---

## What "Document's DOCISPAN entry" Means

Each `docopy` call [`do1.c:62`] registers the exact I-spans being incorporated:

```c
// do1.c:62
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

A document may accumulate many DOCISPAN crums — one per `docopy` or `doinsert` operation. In `finddocscontainingsp`, the outer loop over `ispanset` iterates over each queried I-span, and for each one calls `retrieverestricted`. If **any** crum stored for this document overlaps with **any** queried I-span, that document will appear in the result. The dedup guard at `spanf1.c:175`:

```c
if (isinlinklist(*headptr, &document.address))
    continue;
```

ensures each document address appears at most once in the output regardless of how many matching crums it has.

---

## Summary

Partial overlap is sufficient, down to a single shared I-address. The system asks: "does any crum in this document's DOCISPAN row of the spanfilade overlap (even at a single point) with the queried I-span?" If yes, the document is included. There is no requirement that the document contain the full queried I-span, nor that the queried span be contained within the document's I-span coverage. The governing code is `crumqualifies2d` at `retrie.c:270`, with the SPANRANGE overlap condition at lines 292–300.
