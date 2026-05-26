## Question 11 [gregory]

> When `deletend` constructs knives from the two cut points of a V-span, does it always produce exactly two knives, and what happens when a cut point falls exactly on an existing POOM crum boundary versus interior to a crum (`whereoncrum == THRUME`)?

## KB Synthesis

## DELETE Knife Construction

### Two knives, always

DELETE always constructs exactly two knife blades: `blade[0] = origin` (start of deletion) and `blade[1] = origin + width` (end of deletion). Unlike INSERT, which uses `findaddressofsecondcutforinsert()` to place the second blade at the next subspace boundary, DELETE's knife blades are simply the two endpoints of the deletion span — no subspace boundary computation occurs. [FC-SUBSPACE], [INT-DELETE-SUBSPACE-ASYMMETRY]

### Phase 1: cutting at each blade

For each of the two blade positions, `makecutsbackuptohere()` (`ndcuts.c:77-90`) consults `whereoncrum()` to classify the blade's position relative to each bottom crum:

**When the blade falls in the interior (THRUME):** `grasp < blade < reach`. `slicecbcpm` is called. This splits the crum at the local offset `blade - grasp`, producing two fragments with widths `blade - grasp` and `reach - blade` respectively. Both are strictly positive (the THRUME precondition guarantees it), so no zero-width crums are created. [PRE-DELETE], [INV-NO-ZERO-WIDTH-CRUM]

**When the blade aligns exactly with a crum boundary (ONMYLEFTBORDER or ONMYRIGHTBORDER):** `slicecbcpm` is NOT called. The crum is left structurally intact and passed to Phase 2 for whole-crum classification. This is a structural optimization: boundary alignment means no split is geometrically necessary. [PRE-DELETE], [INV-NO-ZERO-WIDTH-CRUM]

**When the blade falls outside the crum (TOMYLEFT or TOMYRIGHT):** no cutting, the crum is simply classified in Phase 2.

### Phase 2: classify and act

After Phase 1 cutting, each bottom crum is classified:
- **Before the deletion range (TOMYLEFT of `blade[0]`):** untouched — no displacement, no removal
- **Fully within `[blade[0], blade[1])`:** Case 1 — `disown` + `subtreefree` (crum freed from tree)
- **After `blade[1]` (Case 2):** V-displacement shifted by subtracting the deletion width via `tumblersub`

The shift in Case 2 uses `strongsub` under the hood, which has an exponent guard: if the deletion width's exponent is smaller than the crum's displacement exponent, the subtraction is a no-op. This is the mechanism by which DELETE in the text subspace (`1.x`) incidentally leaves link crums at `2.x` unshifted — not by deliberate design but by arithmetic. [FC-SUBSPACE], [ST-DELETE], [INT-DELETE-SUBSPACE-ASYMMETRY]

### Concrete example

```
Crum A: [1.1, 1.4)   Crum B: [1.4, 1.7)   Crum C: [1.7, 1.10)

DELETE [1.1, 1.7):  blade[0]=1.1, blade[1]=1.7

Phase 1, blade[0]=1.1:
  Crum A: whereoncrum(1.1, A) → ONMYLEFTBORDER  → no slicecbcpm
Phase 1, blade[1]=1.7:
  Crum C: whereoncrum(1.7, C) → ONMYLEFTBORDER  → no slicecbcpm

Phase 2:
  Crum A: fully within [1.1, 1.7) → disown + subtreefree
  Crum B: fully within [1.1, 1.7) → disown + subtreefree
  Crum C: after 1.7 → shift backward by 0.6

DELETE [1.2, 1.5):  blade[0]=1.2, blade[1]=1.5

Phase 1, blade[0]=1.2:
  Crum A [1.1,1.4): whereoncrum(1.2, A) → THRUME → slicecbcpm
  Splits A into [1.1,1.2) and [1.2,1.4)
Phase 1, blade[1]=1.5:
  Crum B [1.4,1.7): whereoncrum(1.5, B) → THRUME → slicecbcpm
  Splits B into [1.4,1.5) and [1.5,1.7)

Phase 2:
  [1.1,1.2): before blade[0] → unchanged
  [1.2,1.4): within [1.2,1.5) → remove
  [1.4,1.5): within [1.2,1.5) → remove
  [1.5,1.7): after blade[1]  → shift backward by 0.3
  Crum C [1.7,1.10): after blade[1] → shift backward by 0.3
```

---

## Code Exploration

I now have everything. Here is the full answer.

---

## `deletend`: Knife Count and Cut-Point Boundary Semantics

### 1. Does `deletend` always produce exactly two knives?

**Yes. Unconditionally.**

`edit.c:40–43`:
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
knives.nblades = 2;
knives.dimension = index;
```

`blades[0]` is set to `origin` (the left cut: start of the V-span to delete). `blades[1]` is set to `origin + width` (the right cut: end of the span). `nblades = 2` is hardcoded. There is no conditional path that produces 1 knife, 3 knives, or 4 knives from `deletend`. (Contrast with `rearrangend` at `edit.c:78`, which uses a `cutseq` of variable length and can fill up to `MAXCUTS = 4` knives [`common.h:108`].)

`newfindintersectionnd` at `ndinters.c:38–42` is a stub that simply sets `*ptrptr = fullcrumptr` and zeroes the offset — it does not descend to find a common ancestor. So `deletend` iterates over the direct children of the full root.

---

### 2. The two phases where `whereoncrum` matters

The cut points are used in two distinct phases: **cut-making** (`makecutsnd`) and **section classification** (`deletecutsectionnd`). THRUME means strictly different things in each.

#### Constants (`common.h:86–90`):
```c
#define TOMYLEFT       -2    // address < crum.left
#define ONMYLEFTBORDER -1    // address == crum.left
#define THRUME          0    // crum.left < address < crum.right (strictly interior)
#define ONMYRIGHTBORDER 1    // address == crum.right
#define TOMYRIGHT       2    // address > crum.right
```

`whereoncrum` for POOM/SPAN (`retrie.c:356–373`):
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // left = abs. crum start
cmp = tumblercmp(address, &left);
if (cmp == LESS)  return(TOMYLEFT);
if (cmp == EQUAL) return(ONMYLEFTBORDER);
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                // right = left + crum width
cmp = tumblercmp(address, &right);
if (cmp == LESS)  return(THRUME);
if (cmp == EQUAL) return(ONMYRIGHTBORDER);
else              return(TOMYRIGHT);
```

---

### Phase 1: `makecutsnd` — Splitting crums at cut points

`makecutsnd` calls `makecutsdownnd` → `makecutsbackuptohere`. At leaf crums (`height == 0`), `ndcuts.c:77–91`:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum(..., &knives->blades[i], ...) == THRUME) {
            new = createcrum(...);
            slicecbcpm(ptr, offset, new, &knives->blades[i], ...);
            ivemodified(ptr); ivemodified(new);
            setwisp(ptr);
        }
    }
    return(0);
}
```

**`whereoncrum == THRUME` (cut falls strictly inside the crum):**
`slicecbcpm` is invoked (`ndcuts.c:373–450`). It:
1. Guards that the cut is truly THRUME: `ndcuts.c:383–388` — `gerror` if not.
2. Computes `localcut = cut - grasp` (cut's position relative to crum start): `ndcuts.c:396`.
3. Validates `localcut.exp == ptr->cwid.dsas[index].exp` (same tumbler level) and `is1story(&localcut)`.
4. Derives `newwid` = the left-piece width by copying the crum's wid and setting the mantissa to `localcut.mantissa[0]`: `ndcuts.c:438–442`.
5. Computes right-piece width: `new->cwid = ptr->cwid - newwid` via `locksubtract`: `ndcuts.c:444`.
6. Shrinks original crum: `ptr->cwid = newwid`: `ndcuts.c:445`.
7. Sets right-piece start: `new->cdsp = ptr->cdsp + ptr->cwid` (after the shrink): `ndcuts.c:446`.
8. Copies 2D info (home document) to the new crum: `ndcuts.c:447`.
9. Inserts `new` as `RIGHTBRO` of `ptr`: `ndcuts.c:448`.

After `slicecbcpm`, the cut position is exactly `ONMYRIGHTBORDER` of the left piece and `ONMYLEFTBORDER` of the right piece. The crum interior has been subdivided at the cut.

**`whereoncrum != THRUME` (cut on or outside the crum boundary):**
The `if` at `ndcuts.c:79` is not entered. Nothing is done for that knife on that crum. The cut already aligns with an existing boundary (or is completely outside the crum's span), so no split is needed or warranted.

**The post-condition of `makecutsnd`:**
After all knife positions have been processed, every knife sits exactly at a crum boundary. No crum straddles any knife. This is the invariant required by the deletion phase.

---

### Phase 2: `deletecutsectionnd` — Classifying each crum for deletion

`edit.c:235–248`:
```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;
    for (i = knives->nblades-1; i >= 0; --i) {
           cmp = whereoncrum(ptr, offset, &knives->blades[i], ...);
           if (cmp == THRUME)             return (-1);
           else if (cmp <= ONMYLEFTBORDER) return (i+1);
    }
    return (0);
}
```

With `nblades = 2` and `blades[0] = origin < blades[1] = origin+width`, the loop scans right-to-left:

**i = 1 (right knife, `origin+width`):**

| `whereoncrum` result | Meaning | Action |
|---|---|---|
| `THRUME` | knife is strictly inside crum | return -1 — fatal: `makecutsnd` missed a cut |
| `TOMYLEFT` or `ONMYLEFTBORDER` | crum starts at or after `origin+width` | return 2 — crum is entirely RIGHT of deleted region |
| `ONMYRIGHTBORDER` or `TOMYRIGHT` | crum ends at or before `origin+width` | continue to i=0 |

**i = 0 (left knife, `origin`):**
Only reached when knife[1] is `ONMYRIGHTBORDER` or `TOMYRIGHT` (crum ends at or before the right cut).

| `whereoncrum` result | Meaning | Action |
|---|---|---|
| `THRUME` | knife is strictly inside crum | return -1 — fatal |
| `TOMYLEFT` or `ONMYLEFTBORDER` | crum starts at or after `origin` | return 1 — crum is entirely WITHIN deleted region |
| `ONMYRIGHTBORDER` or `TOMYRIGHT` | crum ends at or before `origin` | continue; fall through to return 0 |

**return 0:** Crum is entirely LEFT of the deleted region (both knives are at or past its right border).

Back in `deletend` (`edit.c:49–73`), these return values map to:

| Return | Case | Action |
|---|---|---|
| -1 | THRUME: unexpected cut interior | `gerror("deletend can't classify crum\n")` — program halt |
| 0 | Crum fully left of deleted span | `break` — untouched |
| 1 | Crum fully within deleted span | `disown(ptr); subtreefree(ptr)` — crum removed from tree |
| 2 | Crum fully right of deleted span | `tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index])` — displacement shifted left by `width` |

---

### Summary

`deletend` always produces **exactly two knives**, hardcoded at `edit.c:42`. The design is a two-phase protocol:

1. **`makecutsnd` guarantees no crum straddles a knife.** For any knife that falls THRUME (strictly interior to a leaf crum), `slicecbcpm` physically splits that crum into two at the cut point, consuming THRUME and creating two boundary-aligned pieces. For knives that already fall on a crum boundary (`ONMYLEFTBORDER` or `ONMYRIGHTBORDER`), nothing is done — the alignment is already correct.

2. **`deletecutsectionnd` then classifies crums assuming the THRUME invariant holds.** If THRUME appears here, it is a bug — `makecutsnd` failed to split something it should have — and the code calls `gerror` to halt. Under normal operation, THRUME never occurs in this phase: every crum either sits left-of, within, or right-of the two-knife window, and receives the corresponding treatment (untouched, deleted, or displaced).
