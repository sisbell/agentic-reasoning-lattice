## Question 12 [gregory]

> When INSERT calls `insertspanf` to create the DOCISPAN entry, does it create exactly one entry covering the full contiguous I-span, or can a single INSERT produce multiple DOCISPAN entries if the POOM insertion splits an existing crum?

## KB Synthesis

A single INSERT always creates exactly one DOCISPAN entry. POOM crum splitting is irrelevant to DOCISPAN creation.

## Why

The call chain for INSERT is:

```
doinsert → inserttextingranf → docopy → insertpm (POOM)
                                      → insertspanf(..., DOCISPAN)
```

`insertspanf` receives the `ispanset` returned by `inserttextingranf`, not anything derived from POOM structure. These two paths are independent. [ST-INSERT, Finding 0036]

`inserttextingranf` for a single INSERT always produces one contiguous I-span. The allocation uses `tumblerincrement` to extend monotonically from the current maximum, so the freshly allocated range `[prev_max+1, prev_max+len]` is always a single contiguous block. [SS-ADDRESS-SPACE, Finding 0033; INV-MONOTONIC]

`insertspanf` iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. Since `inserttextingranf` returns one `typeispan`, exactly one `insertnd` call occurs — one DOCISPAN entry. [SS-DOCISPAN, Finding 0047]

## POOM splitting is irrelevant

`insertpm` handles the POOM tree (crum splitting, extension, rebalancing). These operations record the V→I mapping but have no effect on the `ispanset` that was already passed to `insertspanf`. The two subsystems receive the same input ispanset independently. Whatever structural tree operations occur — split, coalesce, extend — they do not feed back into the DOCISPAN write path.

This is confirmed by the frame condition [FC-CONTENT-SPANF-ISOLATION]: content operations modify the granfilade and DOCISPAN sub-index based on the I-span from allocation, not from POOM state.

## Summary

| Source of variation | Affects DOCISPAN count? |
|----|---|
| Number of bytes inserted | No (always 1 contiguous I-span from `inserttextingranf`) |
| POOM crum split | No (separate subsystem, independent of `insertspanf` input) |
| POOM crum extension | No (same reason) |
| CREATELINK between inserts | Yes — via a separate allocation that advances the I-address counter, breaking contiguity for *subsequent* inserts [INT-LINK-INSERT, Finding 0063] |

---

## Code Exploration

Now I have everything needed. Let me write the complete answer.

---

## Answer: INSERT, `insertspanf`, and DOCISPAN Entry Count

### The Call Path

**INSERT → `doinsert` → `docopy` → `insertspanf`**

`doinsert` [do1.c:87-123]:
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    ...
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

`docopy` [do1.c:45-64]:
```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // POOM insertion
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // spanfilade entry
&& asserttreeisok(docorgl)
);
```

The critical structural fact: the `ispanset` passed to `insertspanf` is determined entirely by `specset2ispanset` **before** `insertpm` is called. The POOM insertion and spanfilade insertion receive the **same, fixed** sporglset.

---

### How `insertspanf` Creates Entries

`insertspanf` [spanf1.c:15-54] loops over the sporglset and calls `insertnd` **once per item**:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // set lstream, lwidth, linfo from item type
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // [spanf1.c:51]
}
```

The number of DOCISPAN entries created equals the number of items in the sporglset. The loop itself adds no multiplicity — it creates exactly one `insertnd` call per item.

---

### What `insertnd` Does for the Spanfilade

The spanfilade is a `SPAN` enfilade (not POOM). `insertnd` [insertnd.c:62-66] for SPAN:
```c
case SPAN:
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
    setwispupwards(fullcrumptr,1);
    break;
```

No `makegappm` is called — that path is POOM-only [insertnd.c:53-54]. `doinsertnd` → `insertmorend` → `insertcbcnd` [insertnd.c:242-275] does one of two things:

- **Extension case** [insertnd.c:250-258]: if `isanextensionnd` is true (new I-span is contiguous with an existing crum's right edge and has the same `homedoc`), the existing crum is widened in place — no new entry.
- **New crum case** [insertnd.c:260-274]: if no extension is possible, one new bottom crum is created via `createcrum` + `adopt`.

`splitcrumupwards` [insertnd.c:272] may restructure internal nodes if a parent is full, but it cannot create additional **bottom** crums — it only splits internal tree nodes. No new DOCISPAN entries result from it.

---

### Why POOM Splitting Cannot Cause Multiple DOCISPAN Entries

`insertpm` [orglinks.c:75-134] inserts into the POOM (the V↔I permutation matrix) using `insertnd` with `V` as the index, calling `makegappm` [insertnd.c:54] to split POOM crums at the insertion V-position:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
knives.nblades = 2;
...
makecutsnd (fullcrumptr, &knives);
```
[insertnd.c:144-148]

This splits POOM crums to open a V-space gap. **But it operates entirely on the granfilade's POOM tree** — a completely separate data structure from the spanfilade. The `ispanset` is a heap-allocated linked list fixed at the point `specset2ispanset` returned; `insertpm` reads it but never writes to it.

By the time `insertspanf` is called (after `insertpm` on do1.c:62), the sporglset already has its final item count. POOM crum splitting has zero influence on that count.

---

### For a Simple Text INSERT: Exactly One DOCISPAN Entry

`inserttextingranf` allocates a single contiguous block of I-space for the inserted text and returns a single I-span in `ispanset`. That becomes a one-item sporglset. `insertspanf` loops once. `insertnd` either widens an adjacent existing DOCISPAN crum or creates one new one.

**Result: A single INSERT always produces exactly one DOCISPAN entry** (or extends one existing entry if the allocated I-space is contiguous with an already-recorded span for that document). The POOM crum splitting that occurs in `insertpm` [insertnd.c:54] is structurally confined to the granfilade and cannot cause `insertspanf` to create additional DOCISPAN entries.

The only way a single INSERT operation could produce multiple DOCISPAN entries would be if `inserttextingranf` returned a multi-item `ispanset` — which would require non-contiguous I-space allocation. The granfilade allocates sequentially and returns one span [do1.c:118], so this does not occur in practice.
