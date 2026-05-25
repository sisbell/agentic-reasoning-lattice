## Question 16 [evidence]

> If an endset's I-span crosses a non-contiguous boundary in the target document's POOM (the linked content has been split by REARRANGE), does the resolved VSpecSet contain one VSpec per contiguous V-run, or a single VSpec covering the bounding range?

## KB Synthesis

## Answer

**One VSpec per contiguous V-run**, sorted by V-address. Not a single bounding VSpec.

### Tracing the call chain

FOLLOWLINK's resolution path is: `link2sporglset()` (extracts the endset I-addresses from the link orgl) → `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` against the target document's POOM [SS-FOLLOWLINK].

`span2spanset()` queries the POOM via `ispan2vspanset()`, which delegates to `permute()` → `findcbcinarea2d()`. That B-tree traversal **iterates all siblings and recurses into all qualifying subtrees**, accumulating every matching leaf via `incontextlistnd()` — which performs insertion-sort and never replaces existing entries [SS-POOM-MULTIMAP]. The result is one context per leaf found, regardless of how many V-runs the I-addresses span.

### What REARRANGE does to the POOM

REARRANGE shifts V-position displacements without touching I-addresses [INV-REARRANGE-IDENTITY]. If the linked content occupies I-addresses α₁..α₁₀ contiguously, and a pivot moves half of them to a non-adjacent V-region, the POOM after the pivot has two separate bottom crums: one mapping α₁..α₅ → V-run A, another mapping α₆..α₁₀ → V-run B. The I-span in the endset is unchanged; the POOM's mapping of it has bifurcated.

### The result

`findcbcinarea2d()` finds both crums and accumulates both contexts. `incontextlistnd()` produces a V-sorted list of two entries [INV-RETRIEVAL-V-SORTED]. `linksporglset2specset()` converts each to a VSpec, yielding two separate VSpecs — one per contiguous V-run.

This is directly confirmed by [EC-PIVOT-LINK-FRAGMENTATION]: after a pivot on linked content, endsets "become fragmented into multiple spans" — the golden test shows four spans for a link whose content was split across two V-positions by the pivot.

### No bounding VSpec

The code has no aggregation step that would merge non-contiguous V-runs into a single bounding span. Each context returned by the B-tree traversal produces one VSpec independently [SS-CONTEXT-LIST]. The `retrieverestricted()` → `incontextlistnd()` pipeline is purely accumulative.

---

## Code Exploration

Now I have the complete picture. Let me write the definitive answer.

---

## Answer: I-Span to VSpecSet Resolution Across Non-Contiguous POOM Boundaries

**The resolved VSpecSet contains one VSpan per contiguous V-run — never a single bounding VSpec.**

---

### The Conversion Pipeline

The entry point is `ispan2vspanset` [`orglinks.c:389-394`]:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
  typespanset *permute();
  return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

This calls `permute` [`orglinks.c:404-422`], which iterates over every span in the I-span set and calls `span2spanset` for each:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

`span2spanset` [`orglinks.c:425-454`] is where the structure is determined:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

There are two questions: **how many contexts come back**, and **does `onitemlist` merge them**.

---

### How Many Contexts: `findcbcinarea2d`

`retrieverestricted` [`retrie.c:56-85`] → `retrieveinarea` [`retrie.c:87-110`] → `findcbcinarea2d` [`retrie.c:229-268`] for POOM type:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // retrie.c:263
    }
}
```

For every **leaf crum** (`height == 0`) that qualifies, a **separate context is created** and inserted into the list sorted by I-coordinate via `incontextlistnd` [`context.c:75-111`]. There is no merging of adjacent or non-adjacent crums here — each qualifing leaf produces its own entry.

After a `rearrangend` call, the POOM has had its leaf crums moved to new V-positions. If the I-span spans content that was split into non-contiguous V-regions by the rearrange, there will be **multiple qualifying leaf crums at distinct V-positions**, each generating a distinct context.

---

### Does `onitemlist` Merge? No.

`onitemlist` [`orglinks.c:464-537`] simply allocates a new item and appends it at the **tail** of the list:

```c
for (temp = *itemsetptr; temp && ((typeitemheader *)temp)->next;
     temp = (typeitem *)((typeitemheader *)temp)->next) ;
((typeitemheader *)temp)->next = (typeitemheader *)newitem;   // orglinks.c:534
```

No adjacency test. No width-merging. Each context becomes a separately-allocated VSpan node.

---

### What About `putvspaninlist`?

`putvspaninlist` [`orglinks.c:329-387`] *does* merge adjacent spans:

```c
if (!spancmp) {                                         // orglinks.c:346
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);  // merge
    return(0);
}
```

But `putvspaninlist` is **not called** in the `ispan2vspanset` path. It is called from `retrievevspansetpm` (the live version at `orglinks.c:173`) and from `walkorglonvpm` inside `#ifdef UnDEFined` (dead code, `orglinks.c:263-312`). The span-building path through `permute` → `span2spanset` → `onitemlist` never touches it.

Similarly, `cleanupvspanlist` [`orglinks.c:297-312`], which would merge adjacent VSpans into single entries, is also inside the `#ifdef UnDEFined` block and is **never executed**.

---

### Each Context Produces One Clipped VSpan

`context2span` [`context.c:176-212`] computes a single VSpan from each context, clipped to the restriction I-span:

```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);  // context.c:207
foundspanptr->itemid = index2itemid(idx2, context);                       // context.c:209
```

`index2itemid` [`context.c:223-238`] returns `VSPANID` when `idx2 == V` and `context->contexttype == POOM`. So each context produces exactly one VSpan covering one contiguous V-run.

---

### What REARRANGE Does to the POOM

`rearrangepm` [`orglinks.c:137-142`] calls `rearrangend((typecuc*)docorgl, cutseqptr, V)`, which moves leaf crums to new V-positions:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);  // edit.c:125
```

**Existing I-addresses are preserved** — the I-coordinates in the leaf crums are not changed. Only the V-coordinates (the positions in virtual document space) shift. An I-span that previously mapped to a single contiguous V-run will now map to multiple V-runs if the rearrange split those crums into non-adjacent positions.

---

### Summary

| Step | Location | Result |
|------|----------|--------|
| `ispan2vspanset` | `orglinks.c:389` | Entry; calls `permute(I→V)` |
| `permute` | `orglinks.c:414` | Loops per I-span; no post-merge |
| `span2spanset` | `orglinks.c:439-444` | **One VSpan per context**; uses `onitemlist` (no merge) |
| `findcbcinarea2d` | `retrie.c:262-263` | **One context per qualifying leaf crum** |
| `context2span` | `context.c:206-209` | Clips crum to I-restriction; emits one VSpan |
| `putvspaninlist` | `orglinks.c:346` | Merges adjacent VSpans — but is **not in this path** |
| `cleanupvspanlist` | `orglinks.c:297` | Would merge adjacent — but is `#ifdef UnDEFined` dead code |

**When an endset's I-span crosses a non-contiguous boundary introduced by REARRANGE, `ispan2vspanset` returns a linked list with one VSpan per contiguous V-run.** The list is ordered by the I-coordinate of the source leaf crums (as sorted by `incontextlistnd`), not by V-position. There is no consolidation step — a single bounding VSpec is never constructed.
