## Question 12 [gregory]

> When a cut point falls in the interior of an existing POOM bottom crum (not on a boundary), does `rearrangend` split the crum into two pieces before applying offsets, or does it treat the entire crum as belonging to one region?

## KB Synthesis

The KB does not describe a crum-splitting phase for `rearrangend`, and the evidence strongly indicates there is none.

**REARRANGE does not split crums at cut points.** It classifies each existing crum as a whole and displaces it as a unit.

The key evidence:

**Finding 0056** (`ST-REARRANGE`) explicitly states: *"No new I-addresses are allocated, no content is duplicated in the permascroll, and the same enfilade nodes (crums) are retained."* The operation calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], ...)` — updating each crum's V-displacement by the offset for whatever section the crum falls into. The crum structure is not restructured.

**Contrast with DELETE.** `PRE-DELETE` (Finding 0075) documents that DELETE *does* have a Phase 1 cutting step: `makecutsbackuptohere()` calls `slicecbcpm` whenever `whereoncrum() == THRUME` (strictly interior). This splits boundary-straddling crums before classifying them. REARRANGE has no equivalent Phase 1 — `rearrangecutsectionnd()` classifies crums directly and `tumbleradd` displaces them, with the code references limited to `edit.c:78-184` and no mention of `slicecbcpm`.

**Practical consequence.** If a cut point falls in the interior of a crum, the entire crum is classified into one section (based on where its grasp falls relative to the cuts) and displaced by that section's offset. Content at the other end of the crum — which logically belongs to a different region — moves with it. This is consistent with `EC-PIVOT-LINK-FRAGMENTATION` (Finding 0019), which documents unexpected endset fragmentation and duplication after pivot, suggesting the rearrangement produces internally fragmented state when crum boundaries don't align with cut points.

The KB does not specify the exact criterion `rearrangecutsectionnd()` uses to classify a straddling crum (e.g., whether it uses the crum's grasp or reach), but since crums are never split, any straddling crum is assigned wholesale to one of the regions.

---

## Code Exploration

Now I have everything I need. Let me trace the full execution path carefully.

---

## Answer

**`rearrangend` splits the crum first, then applies offsets. A cut through a crum's interior is never ignored — it is a hard precondition that must be resolved before any offset arithmetic begins.**

Here is the complete call sequence with line citations.

---

### Step 1: `rearrangend` calls `makecutsnd` before touching any offsets

`edit.c:110`:
```c
makecutsnd (fullcrumptr, &knives);
```

This is the very first substantive operation in `rearrangend`, called *before* the loop that applies offsets at `edit.c:113–136`. The offset application loop only runs after `makecutsnd` returns.

---

### Step 2: `makecutsnd` recursively ensures no crum straddles any knife

`ndcuts.c:15–31`:
```c
int makecutsnd(typecuc *fullcrumptr, typeknives *knives) {
    makecutsdownnd(fullcrumptr, &offset, knives);
    for (...; sonsarecut(fullcrumptr, &offset, knives); ...) {
        makecutsdownnd(fullcrumptr, &offset, knives);
    }
}
```

`sonsarecut` (`ndcuts.c:359–371`) tests every son with `whereoncrum == THRUME`. The outer loop keeps calling `makecutsdownnd` until no son is cut through. The function terminates only when the tree is clean.

---

### Step 3: At the bottom crum, `makecutsbackuptohere` detects THRUME and physically splits

`ndcuts.c:77–91`:
```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset,
                        &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new,
                       &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
        }
    }
    return(0);
}
```

`THRUME` is defined in `common.h:88` as `0` — the return value of `whereoncrum` when the address lies **strictly inside** the crum (left boundary < address < right boundary). When that condition fires for a bottom crum (height == 0), the crum is not skipped or approximated — a new sibling is allocated and `slicecbcpm` is called immediately.

---

### Step 4: `slicecbcpm` performs the physical split

`ndcuts.c:373–450`:
```c
int slicecbcpm(typecorecrum *ptr, typewid *offset, typecorecrum *new,
               tumbler *cut, INT index)
{
    prologuend(ptr, offset, &grasp, NULL);
    // guard: must be THRUME
    if (whereoncrum(ptr, offset, cut, index) != THRUME)
        gerror("Why are you trying to slice me?\n");
    // guard: must be single-story width
    if (!lockis1story(ptr->cwid.dsas, widsize(enftype)))
        gerror("Not one story in POOM wid\n");

    tumblersub(cut, &grasp.dsas[index], &localcut);  // cut point relative to crum start

    movewisp(&ptr->cwid, &newwid);
    for (i = 0; i < widsize(enftype); i++) {
        newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
        tumblerjustify(&newwid.dsas[i]);
    }
    locksubtract(&ptr->cwid, &newwid, &new->cwid, widsize(enftype));  // right half width
    movewisp(&newwid, &ptr->cwid);                                     // left half stays in ptr
    dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);              // right half starts at cut
    move2dinfo(&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
    adopt(new, RIGHTBRO, ptr);  // insert new as right sibling
}
```

The arithmetic is precise:
- `localcut = cut − grasp.dsas[index]` — the cut position relative to the crum's own left edge
- The original crum `ptr` is truncated to width `localcut` (left piece)
- `new` gets width `original_width − localcut` (right piece)
- `new->cdsp` is set so it starts exactly at the cut point

After `slicecbcpm`, the one crum that spanned the cut has become two adjacent crums, with the boundary between them sitting exactly on the knife.

---

### Step 5: After `makecutsnd`, the tree is guaranteed clean — THRUME is a fatal error

Back in `rearrangend`, the classification loop calls `rearrangecutsectionnd` on every child:

`edit.c:113–136`:
```c
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = rearrangecutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case -1:
        gerror ("rearrangend can't classify crum\n");  // edit.c:118
      case 0:  case 4:
        break;
      case 1:  case 2:  case 3:
        tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified(ptr);
        break;
    }
}
```

`rearrangecutsectionnd` at `edit.c:191–204`:
```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives) {
    for (i = knives->nblades - 1; i >= 0; --i) {
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)
            return (-1);          // → gerror in caller
        else if (cmp <= ONMYLEFTBORDER)
            return (i+1);
    }
    return (0);
}
```

If any crum still returns `THRUME` here, the code aborts with `gerror`. The `-1` / `gerror` path is not a fallback — it is a correctness assertion. The design contract is: *`makecutsnd` must eliminate all THRUME bottom crums before the offset loop runs.*

---

### Step 6: Tree-structure cleanup follows offset application

`edit.c:141`:
```c
(void)splitcrumupwards(fullcrumptr);
```

`split.c:16–44` handles the case where the slicing added children and a parent now has too many sons. This is structural balancing, not further splitting of crums at the cut boundary.

---

## Conclusion

When a cut point falls in the interior of a POOM bottom crum, `rearrangend` **physically splits that crum into two pieces** before applying any offsets. The split is performed by `slicecbcpm` (`ndcuts.c:373`), called from `makecutsbackuptohere` (`ndcuts.c:84`), called from `makecutsnd` (`ndcuts.c:15`) — which `rearrangend` invokes at `edit.c:110` as its very first action. After `makecutsnd` completes, every bottom crum lies entirely within one inter-knife region. The offset-application loop (`edit.c:113–136`) then assigns each such crum to a region (0–4) and adjusts its displacement accordingly. A crum that straddles a knife at offset-application time is a fatal invariant violation, caught by the `gerror` at `edit.c:118`.
