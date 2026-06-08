## Question 14 [evidence]

> If copied content lands contiguous with existing I-addresses already in the target POOM, does isanextensionnd merge it into one bottom crum via reach==origin rather than creating a separate entry?

## KB Synthesis

Yes, but with three simultaneous conditions required.

`isanextensionnd()` at `insertnd.c:293-301` checks:
1. The new mapping's `homedoc` matches the existing crum's `homedoc` (I-address origin document)
2. The new content's I-space origin equals the existing crum's I-space reach (`reach == origin`)
3. Implicitly: the V-space insertion point equals the crum's V-space reach

When all three hold, the existing crum's width is extended in place rather than creating a new crum. [ST-VCOPY Finding 0046]

The extension is **rightward only** — `isanextensionnd` checks `reach == origin`, not `grasp == origin + width`. [ST-INSERT Finding 0062]

The homedoc condition is the critical constraint for COPY: content from two different source documents will never merge even if their I-addresses happen to be contiguous, because they carry different homedocs. [ST-VCOPY Finding 0046]

```
COPY same source at V=1.6 (contiguous, same homedoc):
  isanextensionnd() → TRUE → crum extended to [V 1.1..1.10 → i₁..i₁₀]

COPY different source at V=1.6 (contiguous, different homedoc):
  isanextensionnd() → FALSE → new crum created
```

---

## Code Exploration

Now I have everything. Let me compose the full answer.

---

## Answer

**Yes, but only when two independent guards both pass.** The merge path exists at `insertnd.c:249-258`, reached via the copy chain `docopy → insertpm → insertnd → doinsertnd → insertmorend → insertcbcnd`. The merge is not automatic — `isanextensionnd` enforces a two-part test before extending instead of creating.

---

### Execution Path: Copy to POOM Insertion

```
docopy [do1.c:45]
  └─ insertpm [orglinks.c:75]
       └─ insertnd [orglinks.c:130, insertnd.c:15]
            └─ doinsertnd [insertnd.c:185]
                 └─ insertmorend [insertnd.c:219]
                      └─ insertcbcnd [insertnd.c:242]   ← where the merge decision happens
```

`docopy` converts the specset to an ispanset via `specset2ispanset`, then calls `insertpm` [do1.c:60]:

```c
// do1.c:53-64
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

Inside `insertpm`, each sporgl item is unpacked [orglinks.c:100-131]:

```c
// orglinks.c:100-131
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address of source content
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);     // V-address in target document
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```

The `linfo.homedoc` is populated by `unpacksporgl` [sporgl.c:178-203]:

```c
// sporgl.c:184-187
} else if (((typeitemheader *)sporglptr)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglptr)->sporglorigin, streamptr);
    movetumbler (&((typesporgl *)sporglptr)->sporglwidth, widthptr);
    movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc /* should be sourcedoc */);
```

So `homedoc` = the **source document's orgl address** (the granfilade slot that holds the I-spans).

---

### The Merge Decision: `insertcbcnd`

At the bottom of the insertion tree (height == 1), `insertcbcnd` scans existing sibling crums [insertnd.c:249-274]:

```c
// insertnd.c:249-274
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // ← MERGE
        ivemodified (ptr);
        setwispupwards (father,1);
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);   // no split needed
    }
}
// fall through: create a new crum
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
```

If `isanextensionnd` fires, `dspadd` extends `ptr->cwid` by adding the incoming `width` (both V and I dimensions) to the existing crum's width. **No new crum is created.** The loop exits immediately.

---

### `isanextensionnd`: The Two Guards

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);                              // Guard 1: same source document
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
                                                     // Guard 2: reach == origin (all dimensions)
}
```

**Guard 1 — same `homedoc`** [insertnd.c:305-306]:
`infoptr->homedoc` (from the incoming copy, = source document's orgl address) must equal `ptr->c2dinfo.homedoc` (the existing crum's recorded source). If the existing crum's content came from a different source document, or was inserted as raw I-spans (ISPANID → `homedoc` zeroed at [sporgl.c:183]), this guard fails immediately and no merge occurs.

**Guard 2 — `reach == origin`** [insertnd.c:307-308]:
`prologuend` [retrie.c:334-339] computes:
```c
dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = left edge (V, I)
dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);    // reach = right edge (V, I)
```

Then `lockeq` [wisp.c:261-267] checks element-by-element equality across `dspsize(POOM)` tumblers — covering **both V and I dimensions**:

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
        if (!tumblereq (lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

For a POOM, this means the existing crum's right edge must equal the incoming content's left edge in **both V-space and I-space simultaneously**. V-space contiguity alone is not sufficient.

---

### What This Means for a Copy Operation

When content from Document A is copied into Document B at V-position `vsaptr`:

| Existing crum in target POOM | Incoming copy content | Result |
|---|---|---|
| `homedoc` ≠ source doc | any | No merge — Guard 1 fails |
| `homedoc` == source doc, `reach` ≠ `origin` in any dimension | I-space adjacent from same source | No merge — Guard 2 fails |
| `homedoc` == source doc, `reach.V == origin.V` AND `reach.I == origin.I` | I-space adjacent, V-space adjacent | **Merge: existing crum's `cwid` extended by `width`** |

The merge fires precisely when:
1. The existing POOM crum recorded content from the **same source document** (its `homedoc` matches)
2. The existing crum's right boundary is **I-space contiguous** with the incoming content (the copy is of the I-span immediately following the existing crum's last I-address)
3. The insertion is **V-space contiguous** (the copy lands at exactly the next V-position after the existing crum)

If all three hold, `isanextensionnd` returns TRUE, `dspadd` at [insertnd.c:251] merges the widths, and the function returns without creating a new bottom crum. Otherwise it falls through to `createcrum` [insertnd.c:260].

---

### Summary

`isanextensionnd` **does** implement merge-via-extension, and it uses `reach == origin` (via `lockeq` across all DSP dimensions) as Guard 2 — but `homedoc` equality is an independent prior Guard 1. A copy landing I-space-contiguous with an existing crum will merge into that crum only if both the source document address matches and the full 2D boundary aligns. Raw I-span insertions (ISPANID, `homedoc` cleared) never merge with anything, since Guard 1 fails unless the existing crum also has a zero `homedoc`.
