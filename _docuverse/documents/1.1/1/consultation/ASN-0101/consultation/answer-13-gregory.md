## Question 13 [gregory]

> When a deletion span partially overlaps a POOM crum (e.g., deleting the last 3 bytes of a 5-byte crum), does `slicecbcpm` produce a single shortened crum with adjusted V-width and I-width, or does it disown the original and create a fresh crum for the surviving portion?

## KB Synthesis

## Mechanics of `slicecbcpm` on Partial Overlap

`slicecbcpm` **modifies the original crum in-place and creates a new sibling** — it does not disown the original.

### Phase 1: The Cut

When a deletion boundary falls strictly interior to a crum (i.e., `whereoncrum() == THRUME`), `makecutsbackuptohere()` calls `slicecbcpm` [PRE-DELETE, Finding 0075]. The split works as follows (`ndcuts.c:396-444`):

1. Compute the local offset: `localcut = cut - grasp` (the surviving prefix width, guaranteed positive)
2. **Original crum**: width shrunk in-place to `localcut` — this is the portion *before* the cut point
3. **New sibling crum**: created with width `cwid - localcut` (via `locksubtract` at `ndcuts.c:444`) — this is the portion *after* the cut point

For your example — deleting the last 3 bytes of a 5-byte crum `[1.1, 1.6)` with cut at `1.3`:
- `localcut = 1.3 - 1.1 = 0.2`
- Original crum: modified in-place to `[1.1, 1.3)`, width `0.2` ← **survives**
- New crum: `[1.3, 1.6)`, width `0.3` ← created, then eliminated in Phase 2

Both resulting widths are strictly positive — `slicecbcpm` cannot produce zero-width crums because the `THRUME` guard enforces strict interiority [INV-NO-ZERO-WIDTH-CRUM].

### Phase 2: Removal

The newly created sibling covers the deletion range entirely (Case 1 in `deletend`): `disown` + `subtreefree` removes it. The original crum, now covering only the surviving prefix, is classified as Case 0 (outside the deletion range) and left intact [ST-DELETE, Finding 0075].

### Contrast: Boundary-Aligned Deletion

If the deletion boundary aligns exactly with the crum's grasp or reach (`ONMYLEFTBORDER` or `ONMYRIGHTBORDER`), `slicecbcpm` is never called — `makecutsbackuptohere()` guards on `THRUME` only. The crum is then handled whole in Phase 2 as either Case 0 (skip) or Case 1 (disown + free), without any splitting [PRE-DELETE, Finding 0075].

### Summary

| Scenario | `slicecbcpm` called? | Original crum | New crum |
|----------|---------------------|---------------|----------|
| Cut strictly interior (THRUME) | Yes | Modified in-place (shortened) | Created, then Phase 2 deletes it |
| Cut at boundary (ONMYLEFT/ONMYRIGHT) | No | Handled whole in Phase 2 | None created |

The original crum is never disowned by `slicecbcpm` — only shrunk. Disowning is a Phase 2 operation and applies to the *new* crum (or to fully-interior crums), not to the crum whose boundary was cut.

---

## Code Exploration

I have the full picture. Here is the complete answer.

---

## How `slicecbcpm` handles partial POOM crum overlap

**Short answer:** The original crum `ptr` *is* the surviving portion — its width is reduced in-place. A fresh crum is created for the *other* (to-be-deleted) portion. The original is never disowned during slicing.

---

### Step 0 — Caller pre-allocates a fresh crum

Before `slicecbcpm` is called, `makecutsbackuptohere` at `ndcuts.c:80` does:

```c
new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
```

`createcrum` → `createcruminternal` (`credel.c:541`) allocates `sizeof(type2dcbc)` for a POOM leaf crum and **zero-initializes both `cdsp` and `cwid`** (`credel.c:580–581`):

```c
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
```

For a GRAN crum, `ndcuts.c:82` copies the `infotype` from `ptr` into `new` before the call.

---

### Step 1 — Entry guards

```c
// ndcuts.c:382
prologuend(ptr, offset, &grasp, (typedsp*)NULL);
```
Computes `grasp`: the absolute V/I address where `ptr` starts in the enfilade.

```c
// ndcuts.c:383
if (whereoncrum(ptr, offset, cut, index) != THRUME)
    gerror("Why are you trying to slice me?\n");
```
The cut must fall *through* this crum (not before it or after it). If not, it's a hard abort.

```c
// ndcuts.c:389
if (!lockis1story(ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror("Not one story in POOM wid\n");
```
The crum's width must be a contiguous single-story span — i.e., it maps a contiguous V-range to a contiguous I-range.

---

### Step 2 — Compute local cut offset

```c
// ndcuts.c:396
tumblersub(cut, &grasp.dsas[index], &localcut);
```

`localcut = cut − grasp_start` — the offset of the cut *within* this specific crum. For the example of cutting after byte 2 of a 5-byte crum, `localcut` = 2.

Two more assertions check that the exponents match (`ndcuts.c:398`) and that `localcut` is itself 1-story (`ndcuts.c:410`).

---

### Step 3 — Partition the width

```c
// ndcuts.c:438
movewisp(&ptr->cwid, &newwid);          // newwid = ptr->cwid  (= 5)
```

`movewisp` is a macro (`wisp.h:58`): `#define movewisp(A,B) movmem((A),(B),sizeof(typewisp))` — a plain struct copy.

```c
// ndcuts.c:439–442
for (i = 0; i < widsize(enftype); i++) { /* I really don't understand this loop */
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify(&newwid.dsas[i]);
}
```

`newwid` is now set to `localcut` (= 2), preserving the exponent from `ptr->cwid`. The in-source comment "I really don't understand this loop" is verbatim in the original code at `ndcuts.c:439`.

```c
// ndcuts.c:444
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
```

`locksubtract` (`wisp.c:275`) calls `tumblersub` across each dimension:
`new->cwid = ptr->cwid − newwid = 5 − 2 = 3`
The **right (to-be-deleted) portion** gets width 3.

```c
// ndcuts.c:445
movewisp(&newwid, &ptr->cwid);          // ptr->cwid = 2
```

The **original crum `ptr` is shortened in-place**: its width drops from 5 to 2. `ptr` is not disowned. No new allocation is made for the surviving portion.

---

### Step 4 — Set displacement and 2D info for the new crum

```c
// ndcuts.c:446
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
```

`dspadd` (`wisp.c:15`) = `lockadd` across DSP dimensions:
`new->cdsp = ptr->cdsp + 2` — the new crum's displacement begins immediately after the surviving portion.

```c
// ndcuts.c:447
move2dinfo(&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
```

Copies the 2D span info (the I-space layout) from `ptr` into `new`.

---

### Step 5 — Insert new crum as right sibling

```c
// ndcuts.c:448
adopt(new, RIGHTBRO, ptr);
```

`adopt` (`genf.c:419`) splices `new` into the enfilade as `ptr`'s right sibling (`genf.c:460–462`):
```c
left = old;               // ptr stays in place
father = findfather(left);
right = findrightbro(left);
```

The original `ptr` remains in its position in the tree. `new` is inserted to its right.

---

### Step 6 — Back in the caller

```c
// ndcuts.c:85–86
ivemodified((typecorecrum*)ptr);
ivemodified((typecorecrum*)new);
```

Both crums are marked dirty. The deletion machinery (`deletecutsectionnd` via `edit.c`) subsequently walks the tree and `disown`s the crums that fall inside the deletion interval — that is `new`, the 3-byte right portion — not `ptr`.

---

### Summary

| | `ptr` (original) | `new` (fresh allocation) |
|---|---|---|
| Width after slice | 2 (shortened in-place) | 3 (the to-be-deleted portion) |
| Displacement | unchanged | `ptr->cdsp + 2` |
| Tree position | original position | inserted as `ptr`'s right sibling via `adopt` |
| Fate | **survives** — the shortened crum | **deleted** by subsequent deletion pass |

`slicecbcpm` does **not** disown the original crum and does **not** create a fresh crum for the surviving portion. It mutates `ptr->cwid` in-place to represent the surviving fragment, and the freshly `createcrum`'d `new` receives the complement width and is the one that gets removed. The surviving portion is, at all times, the identity-continuous original crum node with an adjusted width field.
