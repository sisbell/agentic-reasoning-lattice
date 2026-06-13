## Question 13 [evidence]

> When one link orgl's endset spans multiple non-contiguous I-spans and the query's from-set overlaps several of them, does the count deduplicate to one link identity, or contribute one per overlapping spanfilade entry?

## KB Synthesis

## Short answer: one contribution per overlapping spanfilade entry — no deduplication.

### How the machinery works

**Indexing step (link creation)**

When a link is created whose endpoint V-span maps to N non-contiguous I-address regions, `vspanset2sporglset` splits the span into N independent sporgls, and `insertendsetsinspanf` makes N separate `insertnd` calls into the spanfilade — one per sporgl [ST-LINK-CREATE], [SS-SPORGL], [INT-SPORGL-LINK-INDEX]. Each entry is keyed independently by its I-address range.

**Search step (find_links)**

`findlinksfromtothreesp` converts the query specset to I-spans, then searches the spanfilade for any FROM-dimension entries overlapping those I-spans [SS-FIND-LINKS, Finding 0028]. The spanfilade walk accumulates matching link ISAs into a linked list. If the query I-spans overlap *k* distinct spanfilade entries that all carry the same link ISA, that ISA is appended *k* times — the accumulation path (`incontextlistnd`, sorted-insert for 2D enfilades) inserts each found context independently and never replaces existing entries [SS-CONTEXT-LIST, Finding 0078]. There is no deduplication stage between the spanfilade walk and the returned list.

The `intersectlinksets` function at `spanf2.c:46-120` (O(n·m) or O(n·m·p)) intersects the FROM, TO, and THREE result sets against each other [SS-FIND-LINKS, Finding 0035], but this only removes links absent from one of the required endpoint sets — it does not collapse duplicate link ISAs within a single endpoint's result set.

### Direct empirical confirmation

The KB records two cases where this duplication is observable:

**EC-PIVOT-LINK-FRAGMENTATION** — after rearranging content that served as a link endpoint, the endset splits into four spans and `find_links` returns the same link ISA **twice**.

**EC-MULTISPAN-LINK-DUPLICATION** — a link created with multiple source spans (`["First" at 1.1, "second" at 1.16]`) causes `retrieve_endsets` to return three spans where one position appears twice.

Both findings note the duplication "may be a bug or may reflect the internal representation of fragmented spans" [EC-PIVOT-LINK-FRAGMENTATION], but neither reports any normalization occurring.

### Formal consequence

The return type of `find_links` is not `Set<LinkISA>` but rather a linked list that behaves as a **multiset**. A link with an endset fragmented into k non-contiguous I-spans, of which m are overlapped by the query, appears m times in the result. The count returned by `findnumoflinksfromtothreesp` walks the list and tallies raw elements [SS-FIND-LINKS, Finding 0035], so it over-counts by the same factor.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Answer: Link Count Deduplication Across Non-Contiguous I-Span Hits

### Short Answer

**The count does not fully deduplicate.** When the query's from-set overlaps N ≥ 2 non-contiguous I-spans of the same link's endset, the link appears **exactly twice** in the output — not once, and not N times. The deduplication in `onlinklist` has an off-by-one: the last element of the accumulating list is never checked, so the **second** hit always creates a duplicate; the third and subsequent hits are correctly caught.

---

### Storage: One Spanfilade Crum Per I-Span

When a link is created, `insertendsetsinspanf` (`do2.c:116`) calls `insertspanf` (`spanf1.c:15`):

```c
for (; sporglset; sporglset = ...) {
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

Each I-span in the from-endset is a **separate bottom crum** inserted into the 2D spanfilade. The ORGLRANGE coordinate for every crum belonging to the same link is set by:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

i.e. `LINKFROMSPAN . linkISA` — **identical across all crums of the same link**, varying only in the SPANRANGE coordinate. A link with N non-contiguous from-I-spans contributes N crums, all sharing the same ORGLRANGE key.

---

### Query: `retrieverestricted` Emits One Context Entry Per Matching Crum

`sporglset2linksetinrange` (`sporgl.c:239`) calls `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229`):

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // retrie.c:263
    }
}
```

Each qualifying bottom crum produces an independent `context` entry. There is no crum-merging at this level. If the query's I-span range overlaps K of the N stored crums, K context entries are returned — each carrying `totaloffset.dsas[ORGLRANGE] = LINKFROMSPAN.linkISA`.

After `beheadtumbler` (`tumble.c:673`) strips the `LINKFROMSPAN` prefix digit, `linksa = linkISA` is identical across all K entries:

```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);   // sporgl.c:264
    onlinklist (taskptr, linksetptr, &linksa);
}
```

---

### Deduplication: The Off-by-One in `onlinklist`

`onlinklist` (`spanf2.c:26`) is the sole function building the link-address list:

```c
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
    linkset = makelinkitem (taskptr, linkisaptr);

    if (*linksetptr == NULL) {
        *linksetptr = linkset;
        return(0);
    }

    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq (&temp->address, linkisaptr))
            return(0);
    }

    temp->next = linkset;
}
```

The loop's exit condition is `nextlink = temp->next`. The loop body runs while `temp->next != NULL` — which means **the last element of the list is never examined by `tumblereq`**.

Trace for K = 2 overlapping I-spans of link L:

| Call | List state | `temp` | `nextlink` | Loop body fires? | Result |
|------|-----------|--------|------------|-----------------|--------|
| 1st (I-span A) | `[]` | — | — | list empty, fast-path | `[L]` |
| 2nd (I-span B) | `[L]` | `L` | `L->next = NULL` | **No** — condition false | `[L, L']` ← **duplicate** |

For K = 3 (I-span C added):

| Call | List state | `temp` | `nextlink` | Loop body fires? | Result |
|------|-----------|--------|------------|-----------------|--------|
| 3rd (I-span C) | `[L, L']` | `L` | `L->next = L'` (truthy) | **Yes** — `tumblereq(L.isa, L.isa) → TRUE` | `return(0)` — deduplicated |

The pattern generalises: with K ≥ 2 hits the output always contains **exactly two** entries for L, because the second hit always bypasses the check (the list has one element whose `->next` is NULL), and every subsequent hit is caught by the first element (whose `->next` is now non-NULL, so the loop body executes).

---

### The Correct Loop — Used Elsewhere But Not Here

`isinlinklist` (`spanf2.c:16`) uses the correct form:

```c
for (; linkset; linkset = linkset->next) {
    if (tumblereq (&linkset->address, linkisaptr))
        return (TRUE);
}
```

This checks every element including the last. But `isinlinklist` is only called from `finddocscontainingsp` (`spanf1.c:175`); it is never consulted in the link-set construction path (`onlinklist` is used instead).

---

### Effect on Counts

`findnumoflinksfromtothreesp` (`spanf1.c:105`) counts the list produced by `findlinksfromtothreesp`:

```c
for (n = 0; linkset; linkset = linkset->next, ++n);
*numptr = n;
```

With K ≥ 2 overlapping I-spans of a single link L, the list is `[L, L']`, so **the reported count is 2, not 1**.

This is consistent with the empirical observation in **Finding 0019 §3** ("the same link is also returned twice by `find_links`" after a pivot fragments endsets), which is now explained at the source level: the pivot causes the stored I-spans to become non-contiguous, and the subsequent query hits two of them, triggering exactly the off-by-one in `onlinklist`.

---

### Summary Table

| # of I-spans hit by query | Entries in link list | Reported count |
|--------------------------|---------------------|----------------|
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 2 | **2 (one duplicate)** | **2** |
| 3 | **2 (one duplicate)** | **2** |
| N ≥ 2 | **2 (one duplicate)** | **2** |

The answer: **the count contributes one per overlapping spanfilade entry for the first two hits (no dedup on the second), then deduplicates correctly from the third hit onward — yielding exactly two entries whenever two or more I-spans match, regardless of the total count N.**
