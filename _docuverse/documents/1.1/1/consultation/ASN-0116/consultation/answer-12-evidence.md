## Question 12 [evidence]

> After inserting at V-position v, does `makegappm` shift every existing POOM entry with V-position ≥ v rightward by width n via `tumbleradd`, while leaving entries before v untouched?

## KB Synthesis

No — `makegappm` does **not** shift every POOM entry with V-position ≥ v. The actual behavior is bounded by a two-blade knife with a subspace ceiling.

## The two-blade knife bounds the shift region

[SS-TWO-BLADE-KNIFE] (Finding 0054): `makegappm` constructs a knife with exactly two blades:

- `blade[0]` = the insertion V-position v
- `blade[1]` = `(N+1).1`, the start of the **next subspace** — computed by `findaddressofsecondcutforinsert()`

`insertcutsectionnd()` then classifies each POOM crum into **three** cases, not two:

| Case | Condition | Effect |
|------|-----------|--------|
| 0 | crum.vpos < `blade[0]` | **No shift** |
| 1 | `blade[0]` ≤ crum.vpos < `blade[1]` | **Shift right by n** |
| 2 | crum.vpos ≥ `blade[1]` | **No shift** |

So entries before v are untouched (correct), but entries **at or beyond the subspace boundary** are also untouched — even though their V-position > v.

## Practical consequence: cross-subspace entries are never shifted

[FC-SUBSPACE] (Finding 0054): INSERT at V-position `1.x` (text subspace) sets `blade[1] = 2.1`. Link entries stored at `2.x` fall into case 2 — they are classified as beyond the second blade and receive no displacement. [ST-INSERT] (Finding 0052) explicitly corrects any reading that all-entries-after-v shift: "The actual behavior is bounded: only crums in the same subspace as the insertion point are affected."

The postcondition is: `∀ entry ∈ poom(doc) : blade[0] ≤ entry.vpos < blade[1] ⟹ entry.vpos' = entry.vpos + n`, with all other entries unchanged.

## Additional early-exit: ONMYRIGHTBORDER triggers no cut at all

[SS-WHEREONCRUM] and [PRE-INSERT] (Finding 0062): `makegappm` has a prior early-exit check — if `origin ≥ crum.reach` (i.e., `whereoncrum == ONMYRIGHTBORDER`), the function returns 0 immediately. No knife is constructed, no entries are shifted. Instead, `isanextensionnd()` handles the insertion by extending the adjacent crum in place. This is the coalescing path for consecutive typing.

## Summary

`makegappm` shifts only POOM entries in the half-open interval `[v, (N+1).1)` — bounded above by the subspace boundary. Entries before v: untouched. Entries in other subspaces (V-position ≥ `blade[1]`): also untouched. And when the insertion point equals an existing crum's reach, `makegappm` exits before any shifting occurs.

---

## Code Exploration

Now I have everything. Let me compile the full answer.

---

## Answer

**No — `makegappm` does not shift every POOM entry with V-position ≥ v via `tumbleradd`. Only entries in the narrow range [v, v.1) are shifted. Entries strictly right of the second cut are left with their existing displacements unchanged.**

---

### Step-by-step trace

#### 1. Entry guard `insertnd.c:140-143`

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
|| tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

`makegappm` returns immediately if the POOM is empty, or if `origin` is outside the POOM's V-span. Only when origin falls strictly inside `[grasp, reach)` does the function proceed.

---

#### 2. Two-blade cut `insertnd.c:144-148`

```c
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```

`blade[0]` = v (the exact insertion point).  
`blade[1]` = computed by `findaddressofsecondcutforinsert` (`insertnd.c:174-183`):

```c
tumblerincrement(position, -1, 1, secondcut);   // embed a sub-digit
beheadtumbler(position, &intpart);
tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut);
tumblerincrement(secondcut, 1, 1, secondcut);
```

The comment says *"needs this to give it a place to find intersection of for text is 2.1."* So if v is integer position 2, `blade[1]` is 2.1 — the first sub-tumbler address inside 2. In the tumbler ordering, v < v.1.

`makecutsnd` splits the POOM tree precisely at both blade positions, creating a clean boundary in the tree at v and at v.1.

---

#### 3. Find the intersection father and loop `insertnd.c:149-169`

```c
newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 0:
      case 2:
          break;
      case -1:
          gerror("makegappm can't classify crum\n");
          break;
      case 1:  /* 9-17-87 fix */
          tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
          ivemodified(ptr);
          break;
      default:
          gerror("unexpected cutsection\n");
    }
}
```

The only displacement modification is at **`insertnd.c:162`** — `tumbleradd` — and it only fires for `case 1`.

---

#### 4. What `insertcutsectionnd` classifies as case 1 vs case 2 `edit.c:207-233`

`whereoncrum(ptr, offset, knife, dim)` (`retrie.c:345-373`) computes:

```
left  = offset->dsas[V] + ptr->cdsp.dsas[V]
right = left + ptr->cwid.dsas[V]
```

Then returns TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT for where `knife` falls relative to `[left, right)`.

`insertcutsectionnd` with `nblades==2` (always the case here):

```c
// Check blade[1] = v.1 first
cmp = whereoncrum(ptr, offset, &blade[1], V);
if (cmp == THRUME)       return -1;   // error: v.1 is inside the crum
if (cmp <= ONMYLEFTBORDER) return 2;  // crum's left border ≥ v.1 → TO THE RIGHT

// Fall through: blade[1] > left(ptr)
// Check blade[0] = v
cmp = whereoncrum(ptr, offset, &blade[0], V);
if (cmp == THRUME)       return -1;   // error: v is inside the crum
if (cmp <= ONMYLEFTBORDER) return 1;  // crum's left border ≥ v → AT THE BOUNDARY

return 0;   // crum's left border < v → TO THE LEFT
```

The three regions:

| `insertcutsectionnd` result | V-position range of child's left border | Action in `makegappm` |
|---|---|---|
| **0** | `left < v` | No action (entry is left of insertion point) |
| **1** | `v ≤ left < v.1` | **`tumbleradd` adds `width->dsas[V]`** — shifts displacement right |
| **2** | `left ≥ v.1` | No action — **no `tumbleradd` called** |

---

#### 5. Case 2 is deliberate — the mirror contrast with `deletend`

In `deletend` (`edit.c:31-76`), case 2 entries (to the right of the deleted region) are *explicitly* shifted left:

```c
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

In `makegappm`, case 2 does nothing. This is the architectural distinction: deletion must close the gap by pulling right-side entries leftward, but insertion places the new content between v and v.1, exploiting the tumbler sub-address hierarchy. Entries at v.1 and beyond sit in sub-tumbler addresses that are already beyond the insertion width — they don't need re-displacement because the new content is allocated in V-addresses that the existing entries never occupied.

---

### Summary

**The question's premise holds only for case 1 entries (those whose V-position falls in [v, v.1)).** These are the entries at the exact insertion boundary, and they receive `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` at `insertnd.c:162`.

Entries strictly to the right of the second cut (`blade[1]` = v.1, case 2) are **not shifted by `tumbleradd`** — their displacements are left unchanged. Entries before v (case 0) are likewise untouched.

The function does not perform a global "shift everything ≥ v" sweep. It shifts only the single narrow slice of tree nodes at the v-boundary, then `doinsertnd` (`insertnd.c:57`) places the new content into the resulting gap.
