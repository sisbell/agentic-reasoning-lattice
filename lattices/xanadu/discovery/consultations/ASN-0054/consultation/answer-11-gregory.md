## Question 11 [gregory]

> In a well-formed POOM, can two bottom crums ever have overlapping V-displacement ranges, or does `insertpm` guarantee that V-spans are strictly non-overlapping — and if so, which code path enforces this?

## KB Synthesis

In a well-formed POOM after INSERT operations, bottom crums have strictly non-overlapping V-displacement ranges. There is no explicit overlap check — the invariant is maintained structurally through three cooperating code paths.

---

## The guarantee holds via implicit structural construction

### 1. Interior split: `makegappm` → `slicecbcpm`

When an INSERT point falls strictly inside an existing crum (`whereoncrum` returns `THRUME`, i.e., `crum.grasp < origin < crum.reach`), `makegappm` calls `slicecbcpm` to split the crum into two halves. The local cut offset satisfies `0 < localcut < cwid` with both strict inequalities, so the resulting halves are:

- Original crum retains `[grasp, grasp + localcut)` 
- New crum receives `[grasp + localcut, reach)`

These are non-overlapping by construction. [INV-NO-ZERO-WIDTH-CRUM] formalizes this: `slicecbcpm` is only reachable when `whereoncrum == THRUME`, guaranteeing both halves have strictly positive width. [PRE-DELETE, Finding 0075]

### 2. Post-insertion shift: two-blade knife in `insertcutsectionnd`

After cutting, all crums in the range `[blade[0], blade[1])` have their V-displacement incremented by exactly `insert_width`. This is a **uniform** additive shift — the relative order of crums is preserved, so pre-existing non-overlap is carried forward. Crums outside the knife range are untouched. [SS-TWO-BLADE-KNIFE, ST-INSERT Finding 0054]

The shift operation `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], ...)` at `insertnd.c:162` applies identically to every eligible crum, so no two crums can collide through this step alone.

### 3. Boundary extension: `isanextensionnd`

When the INSERT point equals an existing crum's `reach` (ONMYRIGHTBORDER), `makegappm` exits early without any cut [PRE-INSERT, Finding 0062]. `isanextensionnd` then checks if the new content is contiguous with the existing crum's I-address range and same `homedoc`; if so, the existing crum's width is extended in place. No new crum is created, so no overlap arises.

---

## No explicit overlap check exists

The KB contains no documentation of a runtime assertion or predicate that checks `crum_i.reach <= crum_j.grasp` for all pairs. The invariant is maintained entirely by construction — the split/shift/extend trio ensures new crum boundaries are always placed at positions that cannot collide with survivors.

---

## Caveat: DELETE can break the bijection

[INV-POOM-BIJECTIVITY] (Finding 0053) notes that DELETE's Case 2 shift via `tumblersub` can produce negative V-positions when same-exponent arithmetic underflows. However, [Finding 0055] corrects this: the `strongsub` exponent guard prevents cross-subspace subtraction entirely, so only same-exponent within-subspace deletions can produce negative results. Negative-position crums are invisible to queries but still occupy tree space. A subsequent INSERT into such a state could encounter them during `whereoncrum` traversal — they sort before all valid addresses (per [SS-TUMBLER] Finding 0053), so they would classify as `TOMYLEFT` and not be shifted. They represent a form of leaked state rather than a genuine overlap.

---

**Summary**: The enforcing code path is `insertpm` → `insertnd` → `makegappm` (at `insertnd.c:137`) which either (a) calls `slicecbcpm` for interior insertions, (b) exits early at boundary, or (c) delegates to the extension path. The subsequent `insertcutsectionnd` shift at `insertnd.c:207` preserves ordering for all survivors. Non-overlap is a structural invariant of the INSERT operation, not an explicit predicate check.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Answer: V-displacement non-overlap in the POOM

**Short answer:** Two bottom crums in a well-formed POOM cannot have overlapping V-displacement ranges. The guarantee is structural, enforced by a three-step protocol executed on every call to `insertpm`.

---

### The code path that enforces non-overlap

**`insertpm`** (`orglinks.c:75`) is the entry point. For each item in `sporglset`, it packs `vsaptr` into `crumorigin.dsas[V]` and `crumwidth.dsas[V]`, then delegates:

```c
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);   /* advance V-cursor */
```
[`orglinks.c:130-131`]

The `index=V` argument is the key: it tells `insertnd` this is a V-dimension insertion. After each item, `vsaptr` is advanced by `crumwidth.dsas[V]`, so within a single `insertpm` call, consecutive items are packed at non-overlapping V-addresses by construction.

The deeper guarantee — protecting against overlap with *previously existing* crums — is inside `insertnd`.

---

### Step 1: `makegappm` — splitting and shifting

`insertnd` (`insertnd.c:15`) handles POOM by calling `makegappm` **before** `doinsertnd`:

```c
case POOM:
    makegappm(taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
```
[`insertnd.c:53-57`]

`makegappm` (`insertnd.c:124`) does three things:

**1a. Guard: skip if origin is outside the current V-range**

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
|| tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```
[`insertnd.c:140-143`]

The comment here is `/* this if for extensions to bc without calling cut */`. If the origin is entirely outside the current V-range (left extension or right append), no existing crums need shifting; non-overlap is trivially preserved.

**1b. Place two knife cuts, then call `makecutsnd`**

```c
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```
[`insertnd.c:144-148`]

`findaddressofsecondcutforinsert` (`insertnd.c:174`) computes a second cut position that is "just past" `origin->dsas[V]` in tumbler arithmetic. The purpose of the two-knife bracketing is to ensure that a crum whose V-range straddles exactly `origin->dsas[V]` can be split cleanly.

`makecutsnd` (`ndcuts.c:15`) walks the tree and, for any bottom crum that is THRUME (straddles) a knife, calls `slicecbcpm` (`ndcuts.c:373`):

```c
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);  /* new starts at old's end */
locksubtract(..., &ptr->cwid, &newwid, &new->cwid);   /* old width shrinks */
movewisp(&newwid, &ptr->cwid);
adopt(new, RIGHTBRO, ptr);
```
[`ndcuts.c:444-448`]

After slicing, the left half ends at the knife and the right half starts at the knife — adjacent, strictly non-overlapping.

**1c. Shift all crums at or past `origin->dsas[V]` rightward**

After cutting, `makegappm` traverses children of the intersection ancestor and applies `insertcutsectionnd` (`edit.c:207`) to classify each crum:

- **Case 0**: crum ends before `blades[0]` — no action
- **Case 1**: crum starts between `blades[0]` and `blades[1]` (i.e., at `origin->dsas[V]` or just after) — **shift right**
- **Case 2**: crum starts at or past `blades[1]` — no action (already past the gap)

The shift for case 1 is:

```c
case 1: /*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified(ptr);
    break;
```
[`insertnd.c:161-164`]

The `9-17-87 fix` comment flags this as a corrected bug — the operand order had been wrong. Every crum whose absolute V-start is ≥ `origin->dsas[V]` gets its relative displacement increased by `width->dsas[V]`, opening an exact gap of width `width->dsas[V]` at `origin->dsas[V]`.

---

### Step 2: `makeroomonleftnd` — the "extend left" case

When the insertion origin is *less* than the current V-start of the POOM (the case `makegappm` skips), `insertmorend` (`insertnd.c:219`) calls `makeroomonleftnd` (`makeroom.c:13`):

```c
if (tumblercmp(&origin->dsas[i], &grasp->dsas[i]) == LESS) {
    tumblersub(&grasp->dsas[i], &origin->dsas[i], &base);
    tumblersub(&origin->dsas[i], &offset->dsas[i], &newdsp.dsas[i]);
    expandcrumleftward((typecorecrum*)father, &newdsp.dsas[i], &base, i);
    ...
}
```
[`makeroom.c:26-42`]

`expandcrumleftward` (`makeroom.c:52`) shifts the parent's V-start leftward to `origin`, grows its V-width by `base`, and shifts all existing children's V-displacements rightward by `base`. This ensures no existing child overlaps with the new left-extension content.

---

### Step 3: `insertcbcnd` — placing the new crum

`insertcbcnd` (`insertnd.c:242`) first tries `isanextensionnd` (`insertnd.c:301`):

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```
[`insertnd.c:301-309`]

This merges only when the new origin exactly equals the existing crum's `reach` (end), with the same `homedoc`. Zero gap, zero overlap — strict adjacency.

If no extension matches, a new bottom crum is created and placed:

```c
new = createcrum(0, (INT)father->cenftype);
reserve(new);
adopt(new, SON, (typecorecrum*)father);
dspsub(origin, grasp, &new->cdsp, (INT)father->cenftype);
movewisp(width, &new->cwid);
```
[`insertnd.c:260-266`]

The new crum's displacement is `origin - grasp` (relative to its parent), and its width is exactly `width`. After step 1 opened the gap, this crum fills it exactly — no overlap with left neighbors (they end ≤ origin) and no overlap with right neighbors (they were shifted to start ≥ `origin + width`).

---

### Does `recombine` preserve the invariant?

Yes. `recombinend` (`recombine.c:104`) may call `takenephewnd` (`recombine.c:235`), which re-parents crums:

```c
disown(nephew);
dspadd(&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype);   /* make absolute */
adopt(nephew, RIGHTMOSTSON, me);
...
dspsub(&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);     /* re-relativize */
```
[`recombine.c:242-248`]

This converts from relative-to-old-parent to absolute, then back to relative-to-new-parent. Absolute V-positions are unchanged. Non-overlap is preserved.

---

### Summary of the enforcement chain

| Step | Function | File | What it does |
|------|----------|------|--------------|
| Split straddling crums | `makecutsnd` → `slicecbcpm` | `ndcuts.c:15`, `ndcuts.c:373` | Splits any bottom crum spanning the insertion point; left half ends at cut, right half starts at cut — no gap, no overlap |
| Open gap (insert within range) | `makegappm` case 1 | `insertnd.c:161-164` | Shifts all crums with V-start ≥ origin rightward by +width |
| Open gap (insert left of range) | `makeroomonleftnd` → `expandcrumleftward` | `makeroom.c:26-42`, `makeroom.c:52-74` | Shifts all existing children rightward by `grasp - origin` |
| Place new crum | `insertcbcnd` | `insertnd.c:242-275` | Places new crum at exactly origin with exactly width |
| Extend adjacent crum | `isanextensionnd` | `insertnd.c:301-309` | Widens existing crum iff `reach == origin` and same `homedoc` — no gap, no overlap |

The structural invariant — bottom crums' absolute V-ranges `[grasp_V, grasp_V + cwid_V)` are strictly non-overlapping and non-adjacent-except-where-merged — is maintained across every insertion. The primary enforcement is in **`makegappm`** (`insertnd.c:124`), which is called exclusively for POOM inserts and whose sole purpose is to open a precise gap at the insertion V-address before the new content is placed.

The suspicious comment at `orglinks.c:114` — `/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/` — concerns the V-*width* calculation (`shift = tumblerlength(vsaptr) - 1`), not the placement logic. A wrong width there would affect how much V-space a crum occupies, but would not by itself create overlap between two crums: `makegappm` would still shift existing crums by whatever width was computed, so the gap would match the new crum's computed width exactly.
