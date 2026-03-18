## Question 19 [gregory]

> In the case of self-transclusion — COPY within the same document creating two V-positions for the same I-addresses — does `incontextlistnd` accumulate both V-positions during I→V conversion, and does `find_links` return both V-positions as separate entries in the endset specset?

## KB Synthesis

Yes to both parts.

**`incontextlistnd` accumulates both V-positions.**

The POOM is a multimap, not a bijection [SS-POOM-MULTIMAP]. After self-transclusion, the two copies of the content sit at distinct V-positions but share the same I-addresses — they are separate leaf crums in the POOM tree. When `findcbcinarea2d` searches by I-address range, it traverses all siblings at every level and recurses into every qualifying subtree, collecting every matching leaf [SS-POOM-MULTIMAP]. `incontextlistnd` performs insertion-sort into a linked list and **never replaces** existing entries [SS-CONTEXT-LIST]. Both V-positions are discovered in tree-traversal order and both are inserted into the sorted result list. The output is a `SortedSeq<Context>` ordered by V-address, with one entry per matching crum — so both V-positions appear as distinct contexts [INV-RETRIEVAL-V-SORTED].

**The endset specset from follow-link and retrieve-endsets contains both V-positions as separate entries.**

The I→V conversion path shared by `FOLLOWLINK` and `RETRIEVEENDSETS` is: `link2sporglset`/`retrieveendsetsfromspanf` → `linksporglset2specset` → `span2spanset` → `retrieverestricted` [SS-FOLLOWLINK]. `retrieverestricted` calls down into the POOM query machinery, which uses `findcbcinarea2d` + `incontextlistnd` — the same multimap accumulation described above. Both V-positions produce separate contexts, and each context yields a separate entry in the output specset.

This is confirmed empirically in [INV-LINK-IDENTITY-DISCOVERY]: a link created at one copy is discoverable (and its endset resolves) from the other copy within the same document, and vice versa. [EC-MULTISPAN-LINK-DUPLICATION] and [EC-PIVOT-LINK-FRAGMENTATION] further show the system produces multiple spans when the same content identity appears at more than one V-position — self-transclusion is exactly this case.

**Important caveat:** `find_links` itself (`FINDLINKSFROMTOTHREE`) returns link ISAs, not endset specsets. The link ISA appears once in the spanfilade regardless of how many V-positions reference its endpoint I-addresses, so `find_links` returns the link once. The multiplicity surfaces only when you resolve endsets via `FOLLOWLINK`, `RETRIEVEENDSETS`, or the retrieve-endsets path [SS-RETRIEVE-ENDSETS].

---

## Code Exploration

Now I have a complete trace through the code. Let me compile the full answer.

---

## Self-Transclusion: `incontextlistnd` and `find_links` Behavior

### Background: What COPY creates in the POOM

`docopy` [do1.c:45-65] does two things:
1. Calls `insertpm` to write new V↔I mapping crums into the document's POOM
2. Calls `insertspanf` to record the I-spans in the spanfilade

After `docopy(taskptr, docisa, &v2, ispanset)` where `ispanset` encodes I-span `[i1..i1+w]` (originally at V-position `v1`), the POOM now contains two leaf crums that reference the same I-addresses:

- **Crum A**: `V=[v1..v1+w]`, `I=[i1..i1+w]` (original insertion)  
- **Crum B**: `V=[v2..v2+w]`, `I=[i1..i1+w]` (self-transclusion copy)

---

### Question 1: Does `incontextlistnd` accumulate both V-positions during I→V?

**Yes.** Here is the full call path:

```
ispan2vspanset         [orglinks.c:389]
  → permute            [orglinks.c:404]
    → span2spanset     [orglinks.c:425]
      → retrieverestricted  [retrie.c:56]
        → retrieveinarea    [retrie.c:87]
          → findcbcinarea2d [retrie.c:229]
```

In `span2spanset` [orglinks.c:435], `retrieverestricted` is called with:
- `span1ptr = restrictionspanptr` (the I-span to look up), `index1 = I`
- `span2ptr = NULL` (no V constraint), `index2 = V`

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
```

`retrieverestricted` [retrie.c:56-85] clears `span2start` and `span2end` to zero when `span2ptr` is NULL:

```c
// retrie.c:71-76
if (span2ptr) { ... } else {
    tumblerclear (&span2start);
    tumblerclear (&span2end);
}
```

Then `crumqualifies2d` [retrie.c:270-305] evaluates the V constraint:

```c
// retrie.c:292-300
endcmp = iszerotumbler (span2end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span2end, index2);
if ( endcmp < ONMYLEFTBORDER) { return(FALSE); }
startcmp = whereoncrum (crumptr, offset, span2start, index2);
if( (startcmp > THRUME)) { return(FALSE); }
```

When `span2end == 0`, `iszerotumbler` returns true → `endcmp = TOMYRIGHT` → check passes.  
When `span2start == 0`, `whereoncrum` returns `TOMYLEFT` for any crum with positive V-displacement → `TOMYLEFT < THRUME` → `startcmp > THRUME` is false → check passes.

The V constraint eliminates nothing. The I-span constraint (`span1`) matches both Crum A and Crum B, since they both map the same I-addresses. `findcbcinarea2d` [retrie.c:252-265] iterates all sibling crums:

```c
// retrie.c:252-264
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) { continue; }
    if (crumptr->height != 0) {
        ...findcbcinarea2d recursively...
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

`incontextlistnd` [context.c:75-111] inserts each context into a linked list ordered by their I-position (`index1 = I`). Since both Crum A and Crum B have the same I-address range, both are inserted — one will be placed before/after the other in sorted order. Both contexts appear in the returned list.

Back in `span2spanset` [orglinks.c:439-445]:

```c
// orglinks.c:439-445
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176-212] computes the V-span for each context by projecting the context's coverage onto the V-dimension (`targindex = V`). Crum A yields a V-span at `[v1..v1+w]`; Crum B yields a V-span at `[v2..v2+w]`. Both are appended via `onitemlist` [orglinks.c:464-537], which does **not** merge spans — it simply chains them as separate list items.

**`incontextlistnd` accumulates both V-positions. The resulting context list has two entries, one per crum.**

---

### Question 2: Does `find_links` return both V-positions as separate entries?

The relevant path for `RETRIEVE_ENDSETS` is:

```
doretrieveendsets         [do1.c:369]
  → retrieveendsetsfromspanf  [spanf1.c:190]
    → specset2sporglset        [sporgl.c:14]   V→I: converts link ISA vspec to I-sporgl
    → retrievesporglsetinrange [spanf1.c:237]  finds endset crums in spanfilade
    → linksporglset2specset    [sporgl.c:97]
        → linksporglset2vspec  [sporgl.c:127]
          → sporglset2vspanset [sporgl.c:141]
            → ispan2vspanset   [orglinks.c:389] I→V: converts I-span back to V-spans
```

In `retrieveendsetsfromspanf` [spanf1.c:237-266], `retrievesporglsetinrange` finds the spanfilade crums that store the endset's I-span. Each such crum was written by `insertspanf` [spanf1.c:15-54] during link creation, indexed by:
- `SPANRANGE`: I-span of the referenced content
- `ORGLRANGE`: link ISA prefixed with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`

The retrieved sporgl carries the raw **I-span** `[i1..i1+w]` of the referenced content.

Then `sporglset2vspanset` [sporgl.c:141-176] calls `ispan2vspanset` for that I-span:

```c
// sporgl.c:157
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

As traced above, `ispan2vspanset` → `permute` → `span2spanset` → `findcbcinarea2d` finds **both** Crum A and Crum B, yielding two V-span entries: `[v1..v1+w]` and `[v2..v2+w]`.

These are accumulated into `*vspansetptr` via `onitemlist`, which chains them without merging (since `v1 ≠ v2`, they are disjoint and would not be merged even by `putvspaninlist`'s merge logic).

The final specset returned to the client is a single `typevspec` with:
- `docisa` = the document ISA
- `vspanset` = `[v1..v1+w] → [v2..v2+w]` (two separate V-span entries)

**`find_links` / `RETRIEVE_ENDSETS` does return both V-positions as separate V-span entries within the endset specset.** The single `typevspec` item has a `vspanset` list with two elements, one for each V-position where the transcluded content appears.

---

### Summary

| Step | Both V-positions? | Mechanism |
|------|:-----------------:|-----------|
| `findcbcinarea2d` walks POOM crums | **Yes** | Iterates all siblings; both crums qualify when V-constraint is unconstrained |
| `incontextlistnd` accumulates them | **Yes** | Inserts both into sorted context list [context.c:75-111] |
| `ispan2vspanset` returns both V-spans | **Yes** | Both contexts survive `context2span` + `onitemlist` loop [orglinks.c:439-445] |
| `RETRIEVE_ENDSETS` endset specset | **Yes** | `sporglset2vspanset` → `ispan2vspanset` → two V-span entries in `vspanset` field |

The key architectural reason this works correctly: I-addresses are stable identifiers in the permascroll. The POOM records every V↔I mapping independently. I→V conversion does an unconstrained scan over the V-dimension, so **all** V-positions that share an I-address are found. Self-transclusion is not a special case — it falls out naturally from the enfilade structure.
