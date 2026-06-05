## Question 11 [evidence]

> When a content region is supplied as a V-span, is it first converted to an I-span via the POOM before any spanfilade search for touching endsets, and what is returned if part of the region maps to no POOM entry?

## KB Synthesis

## V-span → I-span conversion for endset retrieval

**Yes, the V-span is converted to I-spans through the POOM before any spanfilade search.**

The call chain for RETRIEVEENDSETS is:

> `retrieveendsetsfromspanf()` converts the input specset to a sporglset (V-to-I translation), then for each endset type calls `retrievesporglsetinrange()` which searches the spanfilade with SPANRANGE and ORGLRANGE restrictions. [SS-RETRIEVE-ENDSETS]

The V-to-I path runs: V-specset → `specset2sporglset()` → `vspanset2ispanset()` → `permute()` → `span2spanset()` → `retrieverestricted()`, producing sporgls that carry both the resolved I-addresses and the source document ISA. [SS-VSPAN-TO-SPORGL]

---

**For V-positions with no POOM entry, silent exclusion applies.**

There is a universal invariant covering all I-to-V and V-to-I conversions:

> unreferenced I-addresses are silently excluded from V-address results. No operation that performs I-to-V conversion will ever return a V-address for an unreferenced I-address. [INV-ITOV-FILTERING]

The same NULL-drop mechanism is visible in FOLLOWLINK's path through `span2spanset()`: if `retrieverestricted` returns NULL (no POOM mapping for a given address), the entry is silently dropped with no error. [SS-FOLLOWLINK]

The consequence for RETRIEVEENDSETS: V-span regions that have no POOM mapping (e.g., positions that were deleted) contribute no I-addresses to the sporglset. The spanfilade search therefore operates only over the I-addresses resolved from the *mapped* portions of the input V-span. Partial coverage produces no error — the operation finds links touching whatever content identity survives. [EC-SEARCH-SPEC-BEYOND-BOUNDS]

---

## Code Exploration

I now have all the code needed. Let me compile the full answer.

---

## V-span to I-span Conversion: Complete Analysis

### Short answer

**Yes.** Every content-retrieval or link-finding path that receives a V-span (`VSPECID`) converts it to an I-span through the POOM *before* any spanfilade search. If part of the region maps to no POOM crum, the unmapped portion is **silently dropped** from the result — no error, no partial match — and the caller receives a shorter I-span set than the region nominally covers.

---

### The call chain — retrieval path

Entry point: `fns.c:175-187` (`retrievev`)

```
fns.c:183        → doretrievev(taskptr, specset, &vstuffset)
do1.c:343-345    → specset2ispanset(taskptr, specset, &ispanset, READBERT)
                   && ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr)
```

`specset2ispanset` (`do2.c:14-46`) is the gate. It walks the specset list and branches on item type:

```c
// do2.c:24-26 — I-span passes through unchanged
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;
    ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;

// do2.c:27-38 — V-span is converted before anything else happens
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (iszerotumbler (&((typevspec *)specset)->docisa))
        qerror ("retrieve called with docisa 0\n");
    if (!(
      findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
           return (FALSE);
    }
}
```

`findorgl` locates the document's POOM. `vspanset2ispanset` (`orglinks.c:397-402`) then delegates immediately to `permute` with the coordinate axes swapped to V→I:

```c
// orglinks.c:397-402
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

---

### `permute` and `span2spanset` — the POOM search

`permute` (`orglinks.c:404-422`) iterates over each V-span in the input set, calling `span2spanset` for each:

```c
// orglinks.c:414-416
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

`span2spanset` (`orglinks.c:425-454`) fires the actual POOM search:

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```

`retrieverestricted` (`retrie.c:56-85`) unpacks the span into start/end tumblers and calls `retrieveinarea` → `findcbcinarea2d`, which walks POOM crums testing each against the V-range with `crumqualifies2d`. Every qualifying crum produces a `context` record holding the intersecting V-coordinates and corresponding I-coordinates.

`context2span` then maps each context record back into a concrete I-span, which `onitemlist` appends to the accumulator.

---

### What happens when part of the region maps to no POOM entry

The critical guard is in `span2spanset` (`orglinks.c:446-448`):

```c
// orglinks.c:446-453
if(!context){
    return(targspansetptr);
}
/* ... */
contextfree (context);
return (&nextptr->next);
```

When `retrieverestricted` finds no POOM crums touching a portion of the V-span, `context` is `NULL`. `span2spanset` returns the accumulator pointer **unchanged** — nothing is appended for the unmatched region. No error is signaled. Execution continues normally into the next iteration of `permute`'s loop.

The result is that the unmapped portion of the V-span **produces no I-span entries**. The caller receives a *partial* I-span set covering only those sub-regions that had POOM crums.

---

### The link-finding path (`findlinksfromtothree`)

For link searching the path goes through `specset2sporglset` instead of `specset2ispanset`, but the POOM conversion happens just as early:

```
fns.c:198        → dofindlinksfromtothree(taskptr, fromvspecset, ...)
do1.c:352        → findlinksfromtothreesp(taskptr, spanf, ...)
spanf1.c:71      → specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED)
```

Inside `specset2sporglset` (`sporgl.c:14-33`), for a `VSPECID` item:

```c
// sporgl.c:25
sporglsetptr = vspanset2sporglset(taskptr, &((typevspec *)specset)->docisa,
                                  ((typevspec *)specset)->vspanset, sporglsetptr, type)
```

`vspanset2sporglset` (`sporgl.c:35-65`) calls `findorgl`, then for each V-span calls:

```c
// sporgl.c:48
(void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
```

This is the same `vspanset2ispanset` → `permute` → `span2spanset` → POOM search chain. The resulting I-spans are then wrapped into `typesporgl` structures (each tagged with `docisa` as `sporgladdress`). Only after the full V→I conversion is complete does `sporglset2linkset` fire `retrieverestricted` against the *spanfilade* (`spanf1.c:77-95` / `sporgl.c:259`).

---

### Summary

| Step | Function | File | What happens |
|---|---|---|---|
| 1 | `specset2ispanset` / `specset2sporglset` | `do2.c:14`, `sporgl.c:14` | Gate: detects VSPECID, calls POOM lookup |
| 2 | `vspanset2ispanset` | `orglinks.c:397` | Dispatches to `permute(…, V, …, I)` |
| 3 | `permute` | `orglinks.c:404` | Iterates each V-span |
| 4 | `span2spanset` | `orglinks.c:425` | Calls `retrieverestricted` on the POOM |
| 5 | `retrieverestricted` → `findcbcinarea2d` | `retrie.c:56`, `retrie.c:229` | Walks POOM crums for V-range hits |
| 6 | **No context → silent skip** | `orglinks.c:446` | Unmapped V-region yields nothing |
| 7 | Spanfilade search | `spanf1.c:77`, `sporgl.c:259` | Now fires on the I-span/sporgl result |

The spanfilade is **never** queried with V-space coordinates. The POOM lookup is a prerequisite — it is the coordinate transformation layer — and any gap in V→I mapping silently narrows the result set with no error propagated to the caller.
