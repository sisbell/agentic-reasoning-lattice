## Question 11 [gregory]

> When `docopy` calls `vspanset2sporglset` on the source document, does the conversion split a single V-span into multiple sporgls if the underlying POOM maps that V-range to non-contiguous I-addresses (e.g., after a prior insertion created a gap), and if so, how many DOCISPAN entries does the target receive — one per sporgl or one for the whole operation?

## KB Synthesis

Yes, the split happens, and the target receives one DOCISPAN entry per sporgl.

**Step 1: vspanset2sporglset splits on I-address contiguity**

[SS-LINK-ENDPOINT] Finding 0037 documents the exact mechanism:

> The conversion chain is: V-span → `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → separate I-span per contiguous I-address region → separate sporgl per I-span.

The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) iterates over every I-span returned by `vspanset2ispanset` and creates one sporgl per contiguous I-address region. If the POOM maps a V-range to N non-contiguous I-address regions — whether due to prior insertions interleaving content from multiple sources, or a link orgl allocation creating a gap ([INT-LINK-INSERT] Finding 0063) — then N sporgls are produced from that single V-span input.

**Step 2: insertspanf creates one DOCISPAN entry per sporgl**

[SS-DOCISPAN] Finding 0047 and [ST-COPY] Finding 0047 are direct:

> DOCISPAN entries have per-span granularity, not per-byte. `insertspanf` loops over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct.

> COPY of fragmented source content (3 non-contiguous regions) creates 3 DOCISPAN entries.

The call chain in `docopy` (`do1.c:45-65`) is: `specset2ispanset` (converts V-specs to I-spans, same fragmentation logic) → `insertpm` (updates POOM) → `insertspanf(..., DOCISPAN)` (one `insertnd` per I-span).

**Concrete answer**

If the source V-span maps to N non-contiguous I-address regions:
- `vspanset2sporglset` produces N sporgls
- `insertspanf` makes N `insertnd` calls → N DOCISPAN entries in the target

[INV-SPANF-GROWTH] captures the cost implication: `|new_DOCISPAN_entries| = |ispanset(source_content)|`, proportional to I-space fragmentation, not byte count. Heavily edited source content (many small I-spans) is more expensive to COPY than pristine content (one large I-span).

---

## Code Exploration

I have all the information needed. Here is the full answer.

---

## Tracing `docopy`'s V→I Conversion and DOCISPAN Entry Count

### 1. Premise correction: `docopy` does not call `vspanset2sporglset`

`docopy` [do1.c:45-65] calls `specset2ispanset`, not `vspanset2sporglset`:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)    // do1.c:54
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // do1.c:60
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)      // do1.c:62
```

`vspanset2sporglset` [sporgl.c:35] is called from `specset2sporglset` [sporgl.c:14], which is used exclusively by link operations (`domakelink`, `docreatelink`, `findlinksfromtothreesp`). The two paths are structurally parallel but distinct.

---

### 2. The actual V→I conversion chain

**`specset2ispanset`** [do2.c:14-46] iterates over the specset. For each `VSPECID` item it calls:

```c
vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
// do2.c:36
```

**`vspanset2ispanset`** [orglinks.c:397-402] is a thin wrapper:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

**`permute`** [orglinks.c:404-422] iterates over every V-span in the vspanset, calling `span2spanset` for each one:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex,
                                  targspansetptr, targindex);  // orglinks.c:415
}
```

**`span2spanset`** [orglinks.c:425-454] is where the POOM query happens:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);  // orglinks.c:435

for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);  // orglinks.c:444
}
```

---

### 3. Does a single V-span split into multiple I-spans?

**Yes.** The mechanism is `findcbcinarea2d` [retrie.c:229], called through `retrieverestricted` → `retrieveinarea`:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), &localoffset, ...);  // recurse into children
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);             // retrie.c:263
    }
}
```

`findcbcinarea2d` finds **every leaf crum** whose V-interval intersects the query V-span. If a prior `doinsert` split the mapping — creating two POOM leaf crums at non-contiguous I-addresses that together cover the original V-range — both leaf crums qualify and both produce a separate context entry. There is no merging step anywhere in this path.

Back in `span2spanset`, each context entry is converted by `context2span` [context.c:176] into a single I-span, clipped to the V-restriction bounds, and appended to the output ispanset via `onitemlist`. So **one V-span → N I-spans, one per qualifying leaf POOM crum**.

---

### 4. How many DOCISPAN entries does the target receive?

**One per I-span** — never one for the whole operation.

**In `insertpm`** [orglinks.c:100-132]:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);
    // ...compute crumwidth.dsas[V]...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance vsaptr for next item
}
```

Each I-span produces one `insertnd` call → one new POOM crum in the target document. The vsaptr is advanced by that crum's V-width before the next iteration, so the fragments land at successive but adjacent V-positions in the target.

**In `insertspanf`** [spanf1.c:15-54]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // unpack lstream, lwidth, linfo from each ISPANID item...
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
}
```

Same iteration, one `insertnd` on the spanfilade per I-span, all tagged `DOCISPAN`.

---

### Summary

| Step | What happens |
|------|-------------|
| `specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset` | Queries the source document's POOM via `findcbcinarea2d`, which returns **one context entry per leaf POOM crum** intersecting the V-span |
| `context2span` + `onitemlist` | Each context entry becomes a separate I-span in the ispanset; **no consolidation is performed** |
| `insertpm` loop | Calls `insertnd` once per I-span on the target's POOM; vsaptr advances after each, so fragments are laid consecutively |
| `insertspanf` loop (DOCISPAN) | Calls `insertnd` once per I-span on the spanfilade |

**Conclusion:** If the source document's POOM maps a single V-span to N non-contiguous I-regions (e.g., because a prior insertion interleaved foreign content), `vspanset2ispanset` produces N I-spans. `insertpm` inserts N POOM crums into the target, and `insertspanf` inserts **N separate DOCISPAN entries** into the spanfilade — one per I-region, not one for the whole operation.
