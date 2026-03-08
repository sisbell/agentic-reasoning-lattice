## Question 12 [gregory]

> After DELETE removes a V-span that covers only part of a POOM bottom crum, does `slicecbcpm` preserve the exact I-displacement of the surviving portion, or does it recompute it from the V-side cut point?

## KB Synthesis

The KB does not contain the complete `slicecbcpm` source code, but the answer can be derived from what it does document.

## The I-displacement is recomputed from the V-side cut point

**The mechanics, from the KB:**

[PRE-DELETE / Finding 0075] establishes that `slicecbcpm` is only invoked when the cut falls strictly interior to a bottom crum (`whereoncrum() == THRUME`). The key computation is:

```
localcut = tumblersub(cut, &grasp)   // ndcuts.c:396 — V-side offset from crum grasp to cut
```

This `localcut` is a **V-space** quantity — the number of bytes from the crum's left edge to the cut point.

[INV-NO-ZERO-WIDTH-CRUM] confirms the split produces:
- Left crum: retains width `localcut` (the portion before the cut)
- Right crum: receives width `cwid - localcut` via `locksubtract` (the surviving portion)

**Why the I-displacement follows from V:**

[SS-POOM-BOTTOM-CRUM] establishes that each POOM bottom crum carries `origin.dsas[V]`, `width.dsas[V]`, `origin.dsas[I]`, and `width.dsas[I]` as separate fields. The V-width and I-width encode the same integer value at different tumbler precisions [INV-WIDTH-VALUE-EQUIVALENCE].

Because POOM crums maintain a 1:1 V-to-I correspondence (one I-address per byte of content), the right (surviving) crum's I-origin must be:

```
new_I_origin = old_I_origin + localcut
```

where `localcut` carries the same integer byte count derived from the V-side cut arithmetic. The right crum's I-displacement is not preserved from the original — it is advanced by `localcut` from the original I-origin. There is no separate I-space cut computation; the V-side offset drives both.

**Supporting structure:**

[ST-INSERT / Finding 0031] confirms that I-addresses and V-addresses advance in lockstep for text content — `tumblerincrement(&lsa, 0, textset->length, &lsa)` uses `rightshift=0`, advancing I-addresses by the same integer count as byte length. `slicecbcpm` uses the same integer quantity (`localcut`) to advance the I-origin of the right fragment.

**Summary:** `slicecbcpm` recomputes the I-displacement of the surviving right portion by adding `localcut` (the V-side integer offset) to the original crum's I-origin. The original I-displacement of the right fragment is not directly preserved — it is derived from the V-side cut point, consistent with the 1:1 V↔I byte correspondence that POOM crums maintain.

---

## Code Exploration

Now I have everything needed. Here is the full answer.

---

## Answer: `slicecbcpm` and I-Displacement After Partial POOM Crum Delete

### Execution path: DELETE → `slicecbcpm`

**`dodeletevspan`** [do1.c:158–166] calls `deletevspanpm`, which calls `deletend` [orglinks.c:145–151]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

**`deletend`** [edit.c:31–76] sets two knife blades — `knives.blades[0] = origin`, `knives.blades[1] = origin + width` — then calls `makecutsnd`. When either blade falls `THRUME` (through the middle of) a height-0 POOM crum, `makecutsbackuptohere` [ndcuts.c:77–91] fires:

```c
if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
    new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
    ...
    slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
    ...
}
```
[ndcuts.c:79–84]

---

### Inside `slicecbcpm` [ndcuts.c:373–450]

The function splits crum `ptr` into a left part (kept in `ptr`) and a new right part (`new`).

**Step 1 — compute absolute grasp (I-start of this crum):**
```c
prologuend(ptr, offset, &grasp, NULL);   // line 382
```
`prologuend` [retrie.c:334–339] does:
```c
dspadd(offset, &ptr->cdsp, grasp, enftype);   // grasp = offset + ptr->cdsp
```
So `grasp.dsas[index]` is the absolute V-address of the crum's left edge.

**Step 2 — compute `localcut` (the V-cut offset within the crum):**
```c
tumblersub(cut, &grasp.dsas[index], &localcut);   // line 396
```
`localcut` = (absolute V-cut address) − (absolute V-start of crum) = V-distance from the crum's left edge to the cut.

**Step 3 — guard: the crum must be "1 story":**
```c
if (!lockis1story(ptr->cwid.dsas, widsize(enftype))) gerror(...)  // line 389–393
```
`is1story` [tumble.c:237–247] returns true only if `mantissa[i] == 0` for all `i >= 1` — meaning all dimensions have a single-digit width. This enforces that V-width == I-width numerically for this bottom POOM crum.

**Step 4 — split the width, then derive the right crum's I-displacement:**
```c
movewisp(&ptr->cwid, &newwid);                                        // line 438: copy original width

for (i = 0; i < widsize(enftype); i++) {                             // line 439
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];               // line 440
    tumblerjustify(&newwid.dsas[i]);                                  // line 441
}
// newwid now holds the left-portion width in ALL dimensions = V-cut offset

locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid,
             (tumbler*)&new->cwid, widsize(enftype));                 // line 444
// new->cwid = original_width − newwid (the right portion's width)

movewisp(&newwid, &ptr->cwid);                                        // line 445
// ptr->cwid ← newwid (left portion's new, truncated width)

dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);                 // line 446
// new->cdsp = ptr->cdsp + ptr->cwid_new
```

`dspadd` [wisp.c:15–18] does element-wise `lockadd` across all DSP slots:
```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype) {
    lockadd(a->dsas, b->dsas, c->dsas, dspsize(enftype));
}
```

---

### The Answer

**`slicecbcpm` does NOT preserve the right crum's I-displacement from any stored field. It recomputes it from the V-side cut point.** Specifically:

| Crum | `cdsp` (I-displacement) | `cwid` (width) |
|------|------------------------|----------------|
| **Left (`ptr`)** | **Preserved verbatim** — `ptr->cdsp` is never written | Set to `localcut.mantissa[0]`, derived from V-cut |
| **Right (`new`)** | **Recomputed**: `ptr->cdsp + ptr->cwid_new` [line 446] | `original_width − newwid`, residual after left split |

The right crum's I-displacement is assembled from two sources, both V-derived: `ptr->cdsp` (unchanged original left-edge I-displacement, which was itself originally set when the crum was inserted) plus `ptr->cwid_new` (the left portion's new width, which equals `localcut.mantissa[0]`, the V-distance from the crum's left edge to the cut).

**Why this is correct, not lossy**: The loop at lines 439–442 sets all dimensions of `newwid` (including the I-dimension) to `localcut.mantissa[0]`. This works because the guard at line 389 (`lockis1story`) enforces that all dimensions of the POOM bottom crum have the same single-digit width — V-span and I-span are the same number at the same tumbler level. Under that invariant, `localcut` (a V-offset) is numerically identical to the I-offset at the same point; there is no separate I-coordinate to consult or preserve.

The original author's comment at line 439 — `/* I really don't understand this loop */` — suggests even he found this multi-dimension overwrite surprising, but it is the mechanism that propagates the 1-story invariant into the split crums.

---

### After the cut: surviving portions in DELETE

After `makecutsnd` cuts both boundaries of the deleted span, `deletend` [edit.c:47–73] classifies each child:

- **Section 1** (entirely inside the deleted span): `disown` + `subtreefree` — **gone**
- **Section 2** (entirely to the right of the deleted span): `tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])` — its V-displacement is decremented by the deleted width. Its **I-displacement is untouched** here. The I-displacement it carries is the one set (or recomputed) by `slicecbcpm` at the right boundary cut.

So the surviving left crum has its I-displacement exactly as it was before the cut — `slicecbcpm` left `ptr->cdsp` alone. The surviving right crum has an I-displacement that was recomputed by `dspadd` at line 446, derived from the V-cut point via `localcut`, not read from any independently stored I-address.
