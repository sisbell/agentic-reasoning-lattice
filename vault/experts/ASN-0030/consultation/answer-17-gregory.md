## Question 17 [gregory]

> When `isanextensionnd` silently merges a COPY's I-span into an adjacent existing POOM entry, does the merged entry preserve the exact original I-address range boundaries, or does the extension alter the stored I-displacement or I-width of the pre-existing crum?

## KB Synthesis

When `isanextensionnd` triggers a merge, **only the width fields change — the original I-displacement (origin) is preserved exactly**.

The check in `isanextensionnd` (`insertnd.c:293-301`) verifies that the new content's origin equals the existing crum's reach in *both* V and I dimensions simultaneously. This means:

- Existing crum covers I-space: `[origin.dsas[I], origin.dsas[I] + width.dsas[I])`
- New content starts at: `origin.dsas[I] + width.dsas[I]` (the exact reach)
- After extension: crum covers `[origin.dsas[I], origin.dsas[I] + width.dsas[I] + new_width.dsas[I])`

The `insertnd.c:243` path — "Width extension: existing crum grows in place" — modifies only the crum's `width.dsas[I]` and `width.dsas[V]` fields. The `origin.dsas[I]` and `origin.dsas[V]` fields are untouched.

So the pre-existing crum's lower boundary is invariant. The extension is strictly rightward: the crum's stored I-displacement stays fixed at the original starting I-address, while the I-width grows to absorb the new content.

This is consistent with [ST-VCOPY] (Finding 0046):

> "If both hold, the existing crum's width is extended in place (`insertnd.c:243`). Otherwise, a new crum is created (`insertnd.c:252-260`). This means repeated COPYs of the same I-addresses produce either extended crums or separate crums depending on contiguity, **never duplicated entries within a single crum**."

And with [SS-POOM-BOTTOM-CRUM] (Finding 0076), which defines the crum structure as having independent `origin` and `width` tubblers per dimension — the extension operation writes only to the width slot.

One caveat from [SS-INSERT-VWIDTH-ENCODING] (Finding 0076): the V-width tumbler is re-encoded at V-address precision (not a direct copy of the I-width tumbler), but the numeric value they encode remains equal per [INV-WIDTH-VALUE-EQUIVALENCE]. So the extension correctly increments both width fields while preserving the invariant that `value(V-width) == value(I-width)`.

---

## Code Exploration

I now have all the code I need. Let me trace the complete execution path.

---

## Answer

**Short answer:** `isanextensionnd` preserves the pre-existing crum's I-displacement (`cdsp.dsas[I]`) exactly — the lower I-boundary is never touched. Only the I-width (`cwid.dsas[I]`) is increased. The upper I-boundary shifts outward to absorb the appended span; the lower boundary does not move.

---

## Full Trace

### Step 1 — Extension gate: `isanextensionnd` (`insertnd.c:301-309`)

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must both be true:
1. **Home document match** — the new span's `homedoc` tumbler equals the existing crum's `c2dinfo.homedoc`. `[insertnd.c:305]`
2. **Exact adjacency in both dimensions** — `lockeq` at `[insertnd.c:308]` iterates over `dspsize(POOM) = 2` tumblers (`wisp.h:26-27`: `DSPSIZEPM 2`), checking both I (`dsas[0]`) and V (`dsas[1]`) simultaneously. `reach` must equal `originptr` in both dimensions.

### Step 2 — How `reach` is computed: `prologuend` (`retrie.c:334-339`)

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = offset + ptr->cdsp
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype); // reach = grasp + ptr->cwid
}
```

`dspadd` at `wisp.c:15-18` calls `lockadd`, which iterates over both dimensions. So:
- `grasp.dsas[I] = offset.dsas[I] + ptr->cdsp.dsas[I]`  — absolute I-start
- `reach.dsas[I] = grasp.dsas[I] + ptr->cwid.dsas[I]`  — absolute I-end (exclusive)

The adjacency check at `[insertnd.c:308]` passes only when `reach.dsas[I] == originptr->dsas[I]`, i.e. the new span begins exactly at the existing crum's I-end.

### Step 3 — The merge: `insertcbcnd` (`insertnd.c:250-257`)

```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // [insertnd.c:251]
    ivemodified (ptr);
    setwispupwards (father,1);
    ...
    return(FALSE);
}
```

`dspadd` at `[insertnd.c:251]` expands to (`wisp.c:15-18`):

```c
lockadd(ptr->cwid.dsas, width->dsas, ptr->cwid.dsas, 2 /*DSPSIZEPM*/);
```

which executes two `tumbleradd` calls (`wisp.c:272`):
```
ptr->cwid.dsas[I] += width->dsas[I]   // I-width grows
ptr->cwid.dsas[V] += width->dsas[V]   // V-width grows
```

**`ptr->cdsp` is never touched.** There is no `dspsub`, no `movewisp`, no assignment to `ptr->cdsp.dsas[I]` anywhere in this merge path.

### Step 4 — Struct layout confirms the fields are independent

From `enf.h:127-128` (the `type2dcbc` bottom crum):
```c
typewid cwid;   // width in I and V
typedsp cdsp;   // displacement (origin offset) in I and V
```

`typewid` and `typedsp` are both `struct { tumbler dsas[2]; }` (`wisp.h:50-52`). They are separate fields. The merge at `[insertnd.c:251]` writes only to `cwid`.

---

## Conclusion

When `isanextensionnd` determines that the incoming COPY's I-span is exactly adjacent to an existing POOM bottom crum, the merge at `insertcbcnd:251` performs **only**:

```
ptr->cwid.dsas[I]  +=  width->dsas[I]     // upper I-boundary extends
ptr->cwid.dsas[V]  +=  width->dsas[V]     // upper V-boundary extends
```

The stored I-displacement `ptr->cdsp.dsas[I]` — which encodes the lower I-address boundary — is **not modified at all**. The pre-existing crum's lower I-boundary is preserved exactly as stored. Only the I-width grows to absorb the appended span, shifting the upper boundary outward by exactly `width->dsas[I]`.
