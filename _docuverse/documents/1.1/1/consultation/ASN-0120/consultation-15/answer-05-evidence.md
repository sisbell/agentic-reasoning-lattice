## Question 5 [evidence]

> Does CREATELINK (via `vspanset2sporglset`/`permute`) require an input V-span to sit at the document's common content depth, or does it resolve spans at other depths and spans containing inactive/deleted positions, emitting sporgls only for the active positions?

## KB Synthesis

## CREATELINK V-Span Resolution: No Depth Requirement, Active-Only Emission

CREATELINK via `vspanset2sporglset`/`permute` does **not** require the input V-span to sit at any particular "common content depth." The resolution is a pure POOM query that emits sporgls only for positions that are currently active (have live POOM entries).

---

### The Resolution Chain

The call chain is [ST-LINK-CREATE (Finding 0037)]:

```
domakelink → vspanset2sporglset → vspanset2ispanset → permute → span2spanset → retrieverestricted
```

`permute()` executes a 2D B-tree query via `findcbcinarea2d()` over the document's POOM, searching for all leaf crums whose V-dimension overlaps the input V-range [SS-POOM-MULTIMAP (Finding 0039)]:

> The search algorithm `findcbcinarea2d()` traverses all siblings at each B-tree level and recursively descends into all qualifying subtrees, accumulating every matching leaf node.

---

### Inactive/Deleted Positions: Silent Omission

DELETE removes POOM bottom crums via `disown` + `subtreefree` [ST-DELETE (Finding 0064)]:

> DELETE operates exclusively on the POOM enfilade — it removes V-to-I mappings by pruning bottom crums (height-0 nodes) via `disown` + `subtreefree`.

Once a crum is freed, it produces no output when the POOM is queried. A V-span that spans both live and deleted positions will only produce sporgls for the live portions — the deleted positions have no crums to find. The universal filtering invariant confirms this [INV-ITOV-FILTERING (Finding 0048)]:

> **Unreferenced I-addresses are silently excluded from V-address results**. No operation that performs I-to-V conversion will ever return a V-address for an unreferenced I-address.

The analogous principle applies in V-to-I direction: `retrieverestricted()` returns only what exists in the POOM. From [SS-FOLLOWLINK (Finding 0048)]:

> If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is silently dropped — no V-span is added to the result.

---

### No Subspace Depth Restriction

`permute()` is explicitly type-agnostic [SS-DUAL-ENFILADE (Finding 0011)]:

> `permute()`, `retrieverestricted()`, and `docopy()` functions are all type-agnostic.

A V-span over the text subspace (`1.x`) resolves to permascroll I-addresses; a V-span over the link subspace (`2.x`) resolves to link orgl ISAs. CREATELINK does not validate which subspace the input spans target — the subspace convention is caller-enforced, not storage-enforced [PRE-SUBSPACE-CONVENTION (Finding 0010)].

---

### Fragmentation from Multi-Source Content

When the V-span covers content transcluded from multiple sources (non-contiguous I-address regions), `vspanset2sporglset` automatically splits the span into multiple sporgls — one per contiguous I-address region [ST-LINK-CREATE (Finding 0037)]:

> When `domakelink` receives a V-span that maps to non-contiguous I-addresses (due to transclusion from multiple sources), the backend automatically splits the V-span into multiple I-spans (sporgls) in the link endset — one per contiguous I-address region.

---

### Summary

| Scenario | Behavior |
|---|---|
| V-span over fully live content | Emits one sporgl per contiguous I-region |
| V-span over fully deleted content | Emits no sporgls (POOM has no crums there) |
| V-span over partially deleted content | Emits sporgls only for surviving regions |
| V-span spanning text subspace (`1.x`) | Emits sporgls with permascroll I-addresses |
| V-span spanning link subspace (`2.x`) | Emits sporgls with link orgl ISAs |
| V-span over multi-source transcluded content | Emits multiple sporgls, one per I-region |

There is no precondition about "common content depth." The function is a mechanical POOM query: whatever leaf crums overlap the V-range contribute sporgls; absent crums (deleted content) contribute nothing.

---

## Code Exploration

I now have all the evidence needed. Let me compose the complete answer.

---

## Answer: How CREATELINK Resolves V-Spans via `vspanset2sporglset`/`permute`

### Complete Call Chain

```
createlink [fns.c:100]
  → docreatelink [do1.c:195]
    → specset2sporglset [sporgl.c:14]   (called 3×, for from/to/three)
      → vspanset2sporglset [sporgl.c:35]
        → findorgl [granf1.c]            (open the doc's POOM)
        → vspanset2ispanset [orglinks.c:397]  (for each V-span)
          → permute [orglinks.c:404]
            → span2spanset [orglinks.c:425]
              → retrieverestricted [retrie.c:56]
                → retrieveinarea [retrie.c:87]
                  → findcbcinarea2d [retrie.c:229]
                    → crumqualifies2d [retrie.c:270]
              → context2span [context.c:176]  (for each found crum)
        → pack typesporgl from (docISA, I-origin, I-width)
```

---

### 1. Does CREATELINK Require V-Spans at the "Common Content Depth"?

**No. There is no depth check anywhere in the chain.**

`docreatelink` [do1.c:214–216] passes each specset to `specset2sporglset` verbatim:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset,&threesporglset,NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:19–28] iterates every VSPEC item and passes its `vspanset` straight through:

```c
for (; specset; specset = ...) {
    ...
    if (!(sporglsetptr = vspanset2sporglset(taskptr,
                &((typevspec*)specset)->docisa,
                ((typevspec*)specset)->vspanset,
                sporglsetptr, type)))
        return (FALSE);
```

`vspanset2sporglset` [sporgl.c:47] iterates raw V-spans:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
```

`vspanset2ispanset` [orglinks.c:397–403] calls `permute(taskptr, orgl, vspanset, V, ispansetptr, I)`. `permute` [orglinks.c:414] calls `span2spanset` for each span, which calls `retrieverestricted` [retrie.c:56].

The decisive test is inside **`crumqualifies2d` [retrie.c:270–305]**, which checks only:

> Does this crum's V-interval intersect the query V-span?  
> Does this crum's I-interval intersect the (unconstrained) I-range?

No tumbler-depth check. No "is this a text-subspace position?" check. Only geometric interval comparisons.

The **text subspace** (`V ≥ 1.0`, mantissa[0]=1, mantissa[1]=0) and **link subspace** (`V ≥ 2.0`) distinction, visible in `findvsatoappend` [orglinks.c:37–48]:

```c
tumblerincrement(&linkspacevstart, 0, 2, &linkspacevstart);  /* 2.0 */
```

…is used only to compute where to *insert* new content. It plays no role in V→sporgl conversion.

---

### 2. Does It Resolve Spans at Other Depths?

**Yes.** `retrieverestricted` [retrie.c:56] → `findcbcinarea2d` [retrie.c:229] performs a raw traversal of the POOM enfilade, collecting every crum whose V-interval overlaps the query span. POOM crums for link-subspace V-positions (e.g., a link's V-address at 2.x) are just as eligible as text-subspace crums. The function returns all overlapping crums regardless of which depth they occupy.

---

### 3. Does It Handle Inactive / Deleted Positions?

**Yes — implicitly and structurally, by emitting sporgls only for active positions.**

When content is deleted via `dodeletevspan` [fns.c:333] → `deletevspanpm` [orglinks.c:145]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` removes the POOM crums that covered those V-positions. The POOM then has a **gap** at those V-addresses.

When `vspanset2sporglset` later asks for V-spans that fall entirely (or partially) within deleted regions:

- `findcbcinarea2d` [retrie.c:252–265] traverses crum siblings and visits children only when `crumqualifies2d` returns TRUE. For deleted V-positions there are **no crums** — the loop finds nothing.
- `vspanset2ispanset` returns an empty `ispanset`.
- The inner loop in `vspanset2sporglset` [sporgl.c:49–58]:

  ```c
  for (; ispanset; ispanset = ispanset->next) {
      sporglset = (typesporgl*) taskalloc(...);
      ...
      *sporglsetptr = sporglset;
  }
  ```

  …simply **does not execute**. No sporgl is allocated or linked.

For a V-span that **partially overlaps** active and deleted regions: only the sub-ranges covered by surviving POOM crums produce contexts. `context2span` [context.c:176] clips each found context to the V-restriction boundaries (lines 191–202), yielding I-spans corresponding only to the active portion. Deleted sub-ranges produce nothing.

The function never errors, warns, or returns FALSE due to "dead" V-positions. The call continues and `sporglsetptr` (the trailing NULL pointer of the sporgl list) is returned normally.

---

### 4. What Happens Downstream with an Empty Sporglset?

`insertendsetsinspanf` [spanf1.c:15] and `insertspanf` [spanf1.c:15]:

```c
for (; sporglset; sporglset = ...) {
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
return (TRUE);
```

When `sporglset` is NULL, the loop body never runs. The function returns TRUE. CREATELINK **succeeds** even when an entire endpoint resolves to zero sporgls — the link document is created, but that endpoint occupies no slots in the spanfilade.

Similarly, `insertpm` [orglinks.c:100]:

```c
for (; sporglset; sporglset = ...) {
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

No sporgls → no POOM crums inserted for that endpoint → the link's V-space for that end is empty.

---

### Summary

| Question | Answer |
|---|---|
| Must V-spans sit at the "common content depth"? | **No** — no depth check exists anywhere in the conversion chain |
| Are spans at non-text depths resolved? | **Yes** — if POOM crums exist at those V-positions, they are found |
| Are deleted/inactive positions handled? | **Yes** — silently and structurally: deleted V-positions have no POOM crums, so they produce no sporgls |
| Are only active positions emitted as sporgls? | **Yes** — because the POOM is the authoritative record of active content; absent crums → absent output |
| Does CREATELINK fail on "dead" V-spans? | **No** — it succeeds with a smaller (or empty) sporglset; no error is raised |

The filtering is not an explicit guard but a structural consequence: `vspanset2sporglset` asks the POOM "which I-positions correspond to these V-positions?" and the POOM answers only for content that currently exists. Deleted content has been excised from the POOM by `deletend`, so it is invisible to the conversion pipeline.
