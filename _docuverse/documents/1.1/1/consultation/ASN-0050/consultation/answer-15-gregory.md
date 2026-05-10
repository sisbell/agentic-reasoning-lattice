## Question 15 [gregory]

> When a link's source endset spans I-addresses `[.0.1.3, .0.1.7]` and a DELETE removes the V-mapping for `[.0.1.4, .0.1.6]` from the only document containing that content, does `span2spanset` during FOLLOWLINK return two disjoint V-spans for the surviving fragments, or does it return an empty result because the I→V conversion finds no current POOM entry covering the interior range?

## KB Synthesis

## Answer: Two Disjoint V-Spans

`span2spanset` returns **two disjoint V-spans** — one for each surviving I-address fragment. It does not return empty.

### Mechanism

FOLLOWLINK converts endset I-addresses to V-addresses via `link2sporglset()` → `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` [SS-FOLLOWLINK]. The critical behavior is in `span2spanset`: it queries the POOM for every I-address in the endset range, and **silently drops** those with no current POOM mapping [INV-ITOV-FILTERING].

After DELETE removes V-mappings for `[.0.1.4, .0.1.6]`:

- The POOM crums for those I-addresses are freed via `disown` + `subtreefree` [ST-DELETE, Finding 0064]
- The granfilade retains the bytes at those I-addresses — only the POOM is mutated [INV-IADDR-IMMUTABILITY]
- POOM entries for `.0.1.3` and `.0.1.7` survive (the latter at a shifted V-position due to DELETE's Case 2 shift) [ST-DELETE, Finding 0053/0055]

When `findcbcinarea2d` traverses the POOM with I-range `[.0.1.3, .0.1.7]` [SS-POOM-MULTIMAP]:

- `.0.1.3` → found, contributes V-span
- `.0.1.4`–`.0.1.6` → not found (freed), silently dropped
- `.0.1.7` → found, contributes V-span

The two contexts are accumulated via `incontextlistnd` in V-sorted order [INV-RETRIEVAL-V-SORTED], producing two separate entries.

### Why Not Consolidated

Although `.0.1.3` and `.0.1.7` may now be V-adjacent (deletion closed the gap), they are **not I-adjacent** — there is a gap between I:.0.1.4 and I:.0.1.7. The `isanextensionnd` consolidation requires contiguity in **both** V and I dimensions [ST-VCOPY, Finding 0046]. Without I-contiguity, the POOM retains two separate crums, and `span2spanset` reports one V-span per contiguous I-region [SS-LINK-ENDPOINT, Finding 0037]:

> "one per contiguous I-region"

### Why Not Empty

Empty results only occur when **all** endset I-addresses lack POOM mappings [EC-GHOST-LINK]. Here, two I-addresses survive. This is partial survival: the link is not orphaned, only fragmentary [EC-LINK-PARTIAL-SURVIVAL].

This is also consistent with [EC-ORPHANED-LINK] (Finding 0005): full orphaning requires deleting the content from *all* documents that reference those I-addresses. Deleting the middle fragment leaves the endpoints live.

### Summary

| I-address | POOM entry after DELETE | FOLLOWLINK result |
|-----------|------------------------|-------------------|
| `.0.1.3` | Exists (V-mapped) | Contributes V-span |
| `.0.1.4`–`.0.1.6` | Freed (`subtreefree`) | Silently dropped |
| `.0.1.7` | Exists (V-shifted) | Contributes V-span |

**Result: two disjoint V-spans.** The deletion creates a gap in the endset's V-space representation without orphaning the link.

---

## Code Exploration

I now have everything I need. Here is the complete answer with all code citations.

---

## Answer: `span2spanset` Returns Two V-Spans — Not Empty, and Not Disjoint

The answer is **neither** of the two alternatives as stated. `span2spanset` returns **two V-span objects**, but they are **adjacent in V-space** (not disjoint with a gap), because `deletend` collapses the V-address range at deletion time. Here is the full trace.

---

### Step 1 — How the Endset is Stored (`docreatelink`)

`docreatelink` [do1.c:195] converts the from/to V-specs to sporglsets via `specset2sporglset` [sporgl.c:14], which calls `vspanset2sporglset` [sporgl.c:35]:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        movetumbler(docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);   // I-span start
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);    // I-span width
```

The I-address equivalent of the V-span is stored permanently in the sporgl. Then `insertendsetsinorgl` [do2.c:130] → `insertpm` [orglinks.c:75] stores those I-spans in the link's own POOM at V-positions `1.1` (from-end) and `2.1` (to-end). The stored endset is **I-span `[.0.1.3, width=4]`** in the link's POOM.

---

### Step 2 — `deletend` Collapses V-Space

`dodeletevspan` [do1.c:158] → `deletevspanpm` [orglinks.c:145]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` [edit.c:31] sets up `knives.blades[0] = .0.1.4` and `blades[1] = .0.1.6`, calls `makecutsnd` to split crums at those V-positions, then for each child of the intersection node calls `deletecutsectionnd` [edit.c:235]:

```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    for (i = knives->nblades-1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)               return (-1);   // spans a knife — error
        else if (cmp <= ONMYLEFTBORDER)  return (i+1);  // returns 1 or 2
    }
    return (0);   // entirely left of deletion — no change
}
```

Assuming the document originally had a single identity-mapped POOM leaf I:`[.0.1.3,.0.1.7]` ↔ V:`[.0.1.3,.0.1.7]`, after `makecutsnd` splits it into three:

| Crum | V-range | I-range | `deletecutsectionnd` result | Action |
|------|---------|---------|----------------------------|--------|
| A | `[.0.1.3,.0.1.4)` | `[.0.1.3,.0.1.4)` | 0 (left of deletion) | unchanged |
| B | `[.0.1.4,.0.1.6)` | `[.0.1.4,.0.1.6)` | 1 (inside deletion) | **disowned + freed** |
| C | `[.0.1.6,.0.1.7)` | `[.0.1.6,.0.1.7)` | 2 (right of deletion) | **V-displacement shifted** |

Case 2 [edit.c:63]:
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

Crum C's V-displacement: `.0.1.6 − .0.0.2 = .0.1.4`.

**Post-delete POOM state:**
- Crum A: I:`[.0.1.3,.0.1.4)` ↔ V:`[.0.1.3,.0.1.4)` (unchanged)
- Crum C: I:`[.0.1.6,.0.1.7)` ↔ V:`[.0.1.4,.0.1.5)` (shifted left by deleted width)

The V-space is now **contiguous** — the hole has been collapsed.

---

### Step 3 — FOLLOWLINK Retrieves the Stored I-Spans

`followlink` [fns.c:114] → `dofollowlink` [do1.c:223] → `link2sporglset` [sporgl.c:67]:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // V-position for from-end
tumblerincrement (&zero, 0, 1, &vspan.width);
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
```

`contextintosporgl` [sporgl.c:205] extracts `context->totaloffset.dsas[I]` (the stored I-origin) and `context->contextwid.dsas[I]` (the stored I-width). Result: sporgl with `sporglorigin = .0.1.3`, `sporglwidth = .0.0.4`.

---

### Step 4 — I→V Conversion: `sporglset2vspanset` → `ispan2vspanset` → `span2spanset`

`linksporglset2specset` [sporgl.c:97] → `linksporglset2vspec` → `sporglset2vspanset` [sporgl.c:141]:

```c
findorgl (taskptr, granf, homedoc, &orgl, type);
movetumbler (&sporglptr->sporglorigin, &ispan.stream);   // .0.1.3
movetumbler (&sporglptr->sporglwidth, &ispan.width);     // .0.0.4
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

`ispan2vspanset` [orglinks.c:389] → `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex=I,
                              (typespan*)NULL, targindex=V, (typeisa*)NULL);
```

---

### Step 5 — `retrieverestricted` Finds Both Surviving Crums

`retrieverestricted` [retrie.c:56] sets:
- `span1start = .0.1.3`, `span1end = .0.1.7` (I-restriction)
- `span2start = zero`, `span2end = zero` (V, unconstrained — NULL input)

→ `retrieveinarea` → `findcbcinarea2d` [retrie.c:229] → `crumqualifies2d` [retrie.c:270]:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);

endcmp = iszerotumbler(span2end) ? TOMYRIGHT : whereoncrum(..., span2end, index2);
if (endcmp < ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum(crumptr, offset, span2start, index2);   // zero vs positive V → TOMYLEFT
if (startcmp > THRUME) return(FALSE);                          // TOMYLEFT < THRUME → pass
```

For the V dimension: `iszerotumbler(span2end=0)` → `TOMYRIGHT` (always passes), and `whereoncrum(crum, zero, V)` returns `TOMYLEFT` for any crum with positive V-displacement, and `TOMYLEFT < THRUME` so the second guard never fires. **The V dimension is entirely unconstrained.**

For the I dimension: both Crum A (I:`[.0.1.3,.0.1.4)`) and Crum C (I:`[.0.1.6,.0.1.7)`) overlap with the restriction `[.0.1.3,.0.1.7]`. **Both qualify.** There is no crum for I:`[.0.1.4,.0.1.6)` — Crum B was freed by `deletend`.

---

### Step 6 — `context2span` Extracts Two V-Spans

`context2span` [context.c:176] clips each context's V-range to the I-restriction:

```c
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    // adjust V-start by the I-overhang
}
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    // adjust V-end by the I-overhang
}
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

**Crum A** (I:`[.0.1.3,.0.1.4)`, V:`[.0.1.3,.0.1.4)`):
- `grasp.I = .0.1.3 == lowerbound .0.1.3` → no V-start adjustment
- `reach.I = .0.1.4 < upperbound .0.1.7` → no V-end adjustment
- **Output:** V-span `{stream=.0.1.3, width=.0.0.1}`

**Crum C** (I:`[.0.1.6,.0.1.7)`, V:`[.0.1.4,.0.1.5)`):
- `grasp.I = .0.1.6 > lowerbound .0.1.3` → no V-start adjustment
- `reach.I = .0.1.7 == upperbound .0.1.7` → no V-end adjustment
- **Output:** V-span `{stream=.0.1.4, width=.0.0.1}`

---

### Step 7 — `onitemlist` Appends Without Merging

`span2spanset` [orglinks.c:444]:
```c
nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
```

`onitemlist` [orglinks.c:464] just allocates and appends items. Unlike `putvspaninlist` [orglinks.c:329], it has **no adjacency-merging logic**. Both V-spans are appended as separate objects.

---

## Conclusion

`span2spanset` returns **two V-span objects**, not empty. The I→V conversion succeeds for both surviving I-ranges. The "interior" I-range `[.0.1.4, .0.1.6)` has no POOM entry, so it contributes nothing to the output — but the two flanking I-ranges `[.0.1.3,.0.1.4)` and `[.0.1.6,.0.1.7)` do, and they produce valid V-spans.

**Critically, the V-spans are adjacent, not disjoint.** `deletend` [edit.c:63] performs `tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])` on every POOM node to the right of the deletion, collapsing V-space. Content originally at V:`[.0.1.6,.0.1.7)` is shifted left by the 2-unit deleted width and lands at V:`[.0.1.4,.0.1.5)` — immediately adjacent to the surviving V:`[.0.1.3,.0.1.4)`. The two returned spans tile contiguously:

```
Span 1: stream=.0.1.3, width=.0.0.1  ← from I:[.0.1.3,.0.1.4)
Span 2: stream=.0.1.4, width=.0.0.1  ← from I:[.0.1.6,.0.1.7) (shifted)
```

The second alternative — "empty result because the I→V conversion finds no current POOM entry covering the interior range" — is incorrect. `findcbcinarea2d` does not require a single contiguous POOM entry spanning the entire restriction. It independently qualifies each surviving leaf crum against the restriction range and collects them all. The absence of a POOM entry for I:`[.0.1.4,.0.1.6)` silently produces no output for that sub-range; it does not abort or suppress output for the ranges that do have entries.
