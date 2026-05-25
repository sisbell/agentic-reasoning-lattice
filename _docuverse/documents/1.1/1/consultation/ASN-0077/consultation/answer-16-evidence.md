## Question 16 [evidence]

> When the queried I-span crosses multiple DOCISPAN boundaries in the spanfilade (because the original content was inserted as separate operations), are multiple matches returned per origin document or is the result coalesced?

## KB Synthesis

The KB does not fully answer this question, but the available evidence points toward **multiple matches being returned without coalescing**.

**What the KB establishes:**

The DOCISPAN sub-index is stored per-span at insertion granularity [SS-DOCISPAN, Finding 0047]: each INSERT or COPY operation creates one `insertnd` call per `typeispan`. If a document received content in three separate operations producing non-contiguous I-address regions, it has three independent DOCISPAN entries. The spanfilade search via `insertspanf`/`finddocscontainingsp` traverses the enfilade tree and accumulates all matching crums [SS-SPANF-OPERATIONS, Finding 0012].

**The duplication evidence:**

The KB explicitly documents that the analogous link-search path does NOT coalesce: after a pivot rearrangement fragments a link's endset, `find_links` returns the same link twice [EC-PIVOT-LINK-FRAGMENTATION]. Similarly, multi-span link creation causes `retrieve_endsets` to return duplicate spans [EC-MULTISPAN-LINK-DUPLICATION]. Both paths share the same spanfilade traversal machinery.

**The gap:**

The KB does not explicitly state whether `finddocscontainingsp` (FIND_DOCUMENTS) deduplicates per-document results when multiple DOCISPAN entries match. The [EC-STALE-SPANF-REFERENCE] example shows `FIND_DOCUMENTS → {S, T}` as a set, but that example doesn't involve a single document with multiple matching entries.

**Best inference:** Given that the link-search paths demonstrably return duplicates from fragmented spanfilade entries, and that FIND_DOCUMENTS uses the same accumulation mechanism, crossing multiple DOCISPAN boundaries would likely yield multiple matches for the same origin document — not coalesced. Callers should expect to deduplicate results themselves.

---

## Code Exploration

I now have all the code I need. Here is the complete answer:

---

## Result: Multiple Contexts, Selectively Coalesced Depending on API Layer

The answer differs by layer. The retrieval engine itself **does not coalesce** — it returns one context per matching crum. Deduplication only happens at specific higher-level callers, and only by document identity, never by span merging.

---

### 1. Insertion: One Crum Per Insert Operation

`insertspanf` (spanf1.c:25–52) loops over its `sporglset` and calls `insertnd` once per element (line 51). Two separate insert operations into the same document produce two separate DOCISPAN crums in the 2D spanfilade — each with its own `SPANRANGE` and `ORGLRANGE`. The ORGLRANGE for each is prefixed with `DOCISPAN = 4` (xanadu.h:39), identifying the origin document via the tumbler stored in `linfo.homedoc` (lines 29, 33, 42).

```c
/* spanf1.c:49-51 */
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

---

### 2. Retrieval Engine: No Coalescing

`findcbcinarea2d` (retrie.c:229–268) is the 2D area query engine. For every qualifying leaf crum (`height == 0`), it creates a separate context and appends it:

```c
/* retrie.c:262-263 */
context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd (headptr, context, index1);
```

There is no span-merging step. If a queried I-span overlaps three DOCISPAN crums that all belong to the same origin document, all three produce distinct context objects.

---

### 3. Context List Ordering: Sorted, Never Merged

`incontextlistnd` (context.c:75–111) inserts each new context in sorted position by the given index dimension. The sort key is the crum's position in SPANRANGE (`index1`). There is no adjacency test, no span merging, and no check for duplicate home-doc tumblers. Two contexts from the same document at adjacent span positions remain two separate nodes:

```c
/* context.c:96-104 — "in middle" insertion */
for (; nextc = clist->nextcontext; clist = nextc) {
    if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
        && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
            c->nextcontext = nextc;
            clist->nextcontext = c;
            return(0);
    }
}
```

---

### 4. `finddocscontainingsp`: Document-Level Deduplication

`finddocscontainingsp` (spanf1.c:151–188) is the high-level "which docs contain this I-span?" query. It calls `retrieverestricted` with:
- `span1ptr = &docspace` (ORGLRANGE restricted to the DOCISPAN slot) 
- `span2ptr = ispanset` (SPANRANGE restricted to the queried I-span)

For each returned context it extracts the origin document address, then explicitly **skips duplicates**:

```c
/* spanf1.c:172-179 */
for (c = context; c; c = c->nextcontext) {
    movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
    beheadtumbler (&docid, &document.address);
    if (isinlinklist(*headptr, &document.address))  /* <-- SKIP DUPLICATE DOCS */
        continue;
    document.itemid = LINKID;
    document.next = NULL;
    addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
}
```

`isinlinklist` (spanf2.c:16–23) does a linear scan for a matching tumbler. So if the queried I-span crosses three crums from the same document, `finddocscontainingsp` returns that document **exactly once**.

---

### 5. `retrievesporglsetinrange`: No Deduplication

`retrievesporglsetinrange` (spanf1.c:237–267) converts each context to a `sporgl` (a span-with-origin record), one-to-one:

```c
/* spanf1.c:248-252 */
for (c = context; c;) {
    sporglset = (typesporgl*) taskalloc(taskptr, sizeof(typesporgl));
    contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
    *sporglsetptr = (typesporglset)sporglset;
    sporglsetptr = (typesporglset*)&sporglset->next;
    ...
}
```

No deduplication. Three crums from the same document yield three sporgls.

---

### 6. `onlinklist` in spanf2.c: Dedup at Link-Item Level

`onlinklist` (spanf2.c:26–44) does skip duplicate ISA tumblers (line 39), but this function operates on final link items (endpoints of `LINKFROMSPAN`/`LINKTOSPAN` relationships), not on the span retrieval results.

---

## Summary

| Layer | Behavior |
|---|---|
| `insertnd` (spanf1.c:51) | One crum per insert — no pre-coalescing |
| `findcbcinarea2d` (retrie.c:262-263) | **Multiple contexts, one per matching crum** — no merge |
| `incontextlistnd` (context.c:75-111) | Sorted insertion, **no span merging** |
| `finddocscontainingsp` (spanf1.c:175) | **One entry per unique document** — explicit dedup by doc address |
| `retrievesporglsetinrange` (spanf1.c:248-252) | **Multiple sporgls, one per crum** — no dedup |

**Conclusion**: When a queried I-span crosses multiple DOCISPAN boundaries from separate insert operations, the retrieval engine returns **multiple matches — one context per DOCISPAN crum, not coalesced**. At the document-discovery level (`finddocscontainingsp`), the caller deduplicates by document address so each origin document appears only once. At the sporgl level (`retrievesporglsetinrange`), the full granularity is preserved with one sporgl per matching crum. **No span-level coalescing occurs anywhere** — adjacent spans from the same origin document that happen to be contiguous in I-space are never merged back into a single span in any code path.
