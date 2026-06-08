## Question 12 [evidence]

> Does COPY shift existing target POOM entries at V-positions ≥ v to the right by the copied width, using the same makegappm machinery as text insertion?

## KB Synthesis

**Yes, with the same bounded shift semantics as INSERT.**

[ST-INSERT] Finding 0052 is the direct answer:

> "INSERT, COPY, and CREATELINK all share the same POOM insertion mechanism: `insertpm → insertnd → makegappm`. The `makegappm` function classifies existing POOM crums relative to the insertion point using `insertcutsectionnd`: case 0/2 (before or at boundary) are left unchanged, case 1 (THRUME — beyond insertion point) are shifted by adding the insertion width to their V-dimension displacement."

Two important qualifications:

**The shift is subspace-bounded, not global.** Per [SS-TWO-BLADE-KNIFE] / [FC-SUBSPACE] Finding 0054, `makegappm` uses a two-blade knife where `blade[1] = (N+1).1` — the next subspace boundary. Only POOM entries in `[v, (N+1).1)` shift; cross-subspace entries are classified as case 2 (no shift).

**Extension may replace splitting.** Per [ST-INSERT] Finding 0062 / [ST-VCOPY] Finding 0046, if the new content is contiguous with an existing crum and shares the same `homedoc`, `isanextensionnd()` widens the existing crum in place — no new crum created, no shift triggered.

So: COPY at position `v` in subspace `N` shifts all POOM entries in `[v, (N+1).1)` rightward by the copied width, using identical machinery to INSERT. Entries outside that range — including all cross-subspace entries — are unaffected.

---

## Code Exploration

I now have the complete picture. Here is my answer.

---

## Answer: Yes — COPY Uses Identical `makegappm` Machinery

### The Complete Call Chain

**FEBE `copy` handler** [fns.c:35–47]:
```c
void copy(typetask *taskptr) {
    if (getcopy(taskptr, &docisa, &vsa, &localspecset)
     && docopy(taskptr, &docisa, &vsa, localspecset))
        putcopy(taskptr);
```
→ **`docopy`** [do1.c:45–65]:
```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset) {
    ...
    return (
        specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
     && findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
     && acceptablevsa(vsaptr, docorgl)
     && asserttreeisok(docorgl)
     && insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)   // [do1.c:60]
     && insertspanf(...)
```
→ **`insertpm`** [orglinks.c:75]:
```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset) {
    ...
    for (; sporglset; sporglset = ...) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
        movetumbler(&lstream, &crumorigin.dsas[I]);
        movetumbler(&lwidth,  &crumwidth.dsas[I]);
        movetumbler(vsaptr,   &crumorigin.dsas[V]);
        /*I'm suspissious of this shift <reg> 3/1/85 zzzz*/   // [orglinks.c:114]
        shift = tumblerlength(vsaptr) - 1;
        inc   = tumblerintdiff(&lwidth, &zero);
        tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);   // [orglinks.c:117]
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);   // advance insertion point
    }
}
```
→ **`insertnd`** [insertnd.c:15], dispatching on `cenftype`:
```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);   // [insertnd.c:54] — gap FIRST
    checkspecandstringbefore();
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
    setwispupwards(fullcrumptr, 1);
    break;
case SPAN:
    bothertorecombine = doinsertnd(...);   // [insertnd.c:63] — NO makegappm for spans
    break;
```

`makegappm` runs **before** `doinsertnd` on POOM nodes. SPAN nodes get no gap machinery.

---

### What `makegappm` Does [insertnd.c:124–172]

```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr,
              typewid *origin, typewid *width) {
    ...
    clear(&offset, sizeof(offset));
    prologuend((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
    if (iszerotumbler(&fullcrumptr->cwid.dsas[V])          // [line 140]
     || tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS  // [line 141]
     || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) // [line 142]
        return(0);    // guard: insertion point outside POOM extent
    movetumbler(&origin->dsas[V], &knives.blades[0]);
    findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = V;
    makecutsnd(fullcrumptr, &knives);                      // [line 148] — cut at v
    newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);  // [line 149]
    prologuend((typecorecrum*)father, &foffset, &fgrasp, NULL);
    for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
        i = insertcutsectionnd(ptr, &fgrasp, &knives);     // [line 152]
        switch (i) {
          case 0:  break;  // BEFORE insertion point — no action
          case 2:  break;  // AT left cut boundary — no action
          case -1: gerror("makegappm can't classify crum\n");  // THRUME — fatal
          case 1:           // AFTER insertion point — SHIFT RIGHT
            tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V],
                       &ptr->cdsp.dsas[V]);                // [line 162]
            ivemodified(ptr);
            break;
        }
    }
    setwidnd(father);
    setwispupwards(findfather((typecorecrum*)father), 1);
}
```

`insertcutsectionnd` [edit.c:207–233] returns `1` when a crum's V-position places it **at or right of `knives.blades[1]`** (the second cut, just past the insertion point):
```c
cmp = whereoncrum(ptr, offset, &knives->blades[1], knives->dimension);
if (cmp <= ONMYLEFTBORDER)
    return(2);   // crum is to the left of second cut — no shift
...
cmp = whereoncrum(ptr, offset, &knives->blades[0], knives->dimension);
if (cmp <= ONMYLEFTBORDER)
    return(1);   // crum is at or right of first cut (origin) — SHIFT
```

The shift amount added to `ptr->cdsp.dsas[V]` is exactly `width->dsas[V]` — the V-width of the content being inserted.

---

### V-Width Derivation [orglinks.c:115–117]

```c
shift = tumblerlength(vsaptr) - 1;
inc   = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
```

The V-width of the gap is derived from the **integer part of the I-width** of each copied I-span, placed at the same tumbler depth as the V-insertion address. Gregory himself flagged this computation as suspicious in a comment dated 3/1/85 [orglinks.c:114], but it is what drives the gap size.

---

### COPY vs. Text INSERT: Same Path

Text INSERT via `doinsert` [do1.c:87–122] takes this path:
```
doinsert → inserttextingranf (allocates I-space) → docopy → insertpm → insertnd → makegappm
```

FEBE COPY [fns.c:35] takes:
```
copy → docopy → insertpm → insertnd → makegappm
```

`docopy` is the **common mechanism** for both operations. Text insert is literally implemented as "allocate in granf, then copy into the POOM." The `makegappm` call is identical in both cases; the only difference is where the I-spans originate (freshly allocated vs. existing permascroll addresses).

---

### Summary

**Yes.** COPY shifts existing target POOM entries at V-positions ≥ `v` rightward by the copied V-width, using `makegappm` [insertnd.c:124]. The path is:

```
fns.c:copy → do1.c:docopy:60 → orglinks.c:insertpm:130 → insertnd.c:insertnd:54 → insertnd.c:makegappm:162
```

The shift amount is `width->dsas[V]`, derived from the I-width of the copied content. This is the same `makegappm` machinery invoked by text INSERT; `docopy` is the shared implementation underpinning both operations.
