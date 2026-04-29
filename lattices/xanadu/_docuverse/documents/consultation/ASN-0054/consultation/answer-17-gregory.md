## Question 17 [gregory]

> After REARRANGE with a 3-cut pivot, can a single pre-existing bottom crum that straddled a cut boundary end up split into two non-contiguous entries in V-space while still referencing a contiguous I-address range — and if so, is there any post-rearrange coalescing pass?

## KB Synthesis

## Short Answer

No — REARRANGE does not split bottom crums at cut boundaries. A crum that straddles a cut moves as a whole unit and remains a single contiguous entry. There is no post-rearrange coalescing pass.

---

## Detailed Analysis

### REARRANGE has no pre-cutting phase

DELETE uses a two-phase algorithm: Phase 1 runs `slicecbcpm` to split any bottom crum whose interior is touched by a cut boundary (only when `whereoncrum == THRUME`), then Phase 2 classifies and removes/shifts the resulting clean crums [PRE-DELETE, Finding 0075].

REARRANGE has no equivalent Phase 1. The full algorithm described in [ST-REARRANGE] (Finding 0056) is:

1. `sortknives()` — sort cut points ascending
2. `makeoffsetsfor3or4cuts()` — compute a displacement vector per region
3. `rearrangecutsectionnd()` — assign each crum to a region (0, 1, 2, or 3)
4. `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V])` — apply displacement in-place

No slice, no copy, no content creation. Each POOM bottom crum is displaced as an atomic unit.

### What happens to a straddling crum

Say a crum covers V-range [1.3, 1.5) → {I_C, I_D}, and the pivot cuts are at [1.2, 1.4, 1.6]:

- Region 1 = [1.2, 1.4): `diff[1] = +0.2`
- Region 2 = [1.4, 1.6): `diff[2] = -0.2`

The crum's grasp (1.3) falls in region 1, so `rearrangecutsectionnd` classifies the whole crum as region 1. The entire crum is displaced by +0.2, landing at [1.5, 1.7). The bytes I_C and I_D remain in one contiguous crum. They do **not** get split into two entries.

The trade-off: I_D, which conceptually belongs to region 2 (its grasp 1.4 equals `cut1`), ends up at V 1.6 instead of V 1.2. The V-I mapping is distorted for the bytes that straddle the boundary, but the crum structure stays intact — one crum, contiguous in both V-space and I-space.

This is consistent with [INV-REARRANGE-IDENTITY]: "The code modifies only `ptr->cdsp.dsas[index]`... No I-addresses are touched, no content is copied." Identity is preserved; correctness of placement for straddling bytes is not.

### Source of the fragmentation in EC-PIVOT-LINK-FRAGMENTATION

The four-span endset fragmentation observed in [EC-PIVOT-LINK-FRAGMENTATION] comes from a different mechanism: *separate* crums that originally held adjacent bytes land at non-contiguous V-positions after pivot. For example, if "C" (in region 1) and "D" (in region 2) were in separate crums, C moves to V 1.5 and D moves to V 1.2 — previously adjacent, now disjoint. The link endset then reflects two separate V-ranges for what were originally contiguous I-addresses.

A single straddling crum, by contrast, moves together and never fragments internally.

### No post-rearrange coalescing pass

There is no documented coalescing step after REARRANGE. The `isanextensionnd` check that merges adjacent inserts fires during the INSERT path's `insertnd` flow [ST-INSERT, Finding 0062]; REARRANGE never calls this path — it only calls `tumbleradd` on existing crums. The structural rebalancer `recombinend` [ST-REBALANCE-2D] is a B-tree occupancy balancer, not a content-coalescing pass. Adjacent crums that happen to land at contiguous V- and I-positions after displacement are **not** automatically merged.

---

## Code Exploration

Now I have everything needed. Let me compile the complete answer.

---

## Answer

### Short Answer

**Yes** — a pre-existing bottom crum straddling a cut boundary is split into two by `slicecbcpm`, and after rearrangement those two halves receive different V-space displacement offsets, placing them at non-contiguous V-space addresses while their I-address content remains contiguous. **No** — there is no post-rearrange coalescing pass that redetects and merges them.

---

### Step 1 — Entry Point: `rearrangend` [edit.c:78–160]

`rearrangend` for a 3-cut rearrange:

1. Fills `knives` with 3 blades (A < B < C after sort) [edit.c:102–107]
2. Computes per-section displacement offsets [edit.c:108]:
3. **Makes the cuts**: `makecutsnd(fullcrumptr, &knives)` [edit.c:110]
4. Finds the intersection (trivially the fullcrum itself): `newfindintersectionnd` [edit.c:111, ndinters.c:38–42] just does `*ptrptr = fullcrumptr`
5. Iterates over all sons of the fullcrum, calls `rearrangecutsectionnd` [edit.c:113–136]
6. Applies `diff[section]` to V-displacement of each son [edit.c:125]
7. `setwispupwards(father, 1)` [edit.c:137]
8. `recombine(fullcrumptr)` [edit.c:139]
9. `splitcrumupwards(fullcrumptr)` [edit.c:141]

---

### Step 2 — Cutting Phase Splits the Straddling Crum

In `makecutsbackuptohere` [ndcuts.c:69–91], when `ptr->height == 0` (bottom crum):

```c
for (i = 0; i < knives->nblades; i++) {
    if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
        new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
        slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

`THRUME = 0` [common.h:88] means the knife address falls **strictly inside** the crum — it straddles the cut. `whereoncrum` [retrie.c:345–398] for SPAN/POOM computes `left = offset[index] + cdsp[index]`, `right = left + cwid[index]`, and returns THRUME when `left < address < right`.

#### What `slicecbcpm` does [ndcuts.c:373–450]

```c
tumblersub(cut, &grasp.dsas[index], &localcut);        // cut pos relative to crum start
// build newwid = left portion's width (up to cut)
locksubtract(&ptr->cwid, &newwid, &new->cwid, ...);    // new->cwid = remainder
movewisp(&newwid, &ptr->cwid);                          // ptr truncated to left portion
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);   // new starts right after
move2dinfo(&((type2dcbc*)ptr)->c2dinfo,
           &((type2dcbc*)new)->c2dinfo);                // same home-doc
adopt(new, RIGHTBRO, ptr);                              // new inserted to right
```

After `slicecbcpm`:

| Half | cdsp (V-origin) | cwid (V-width) | I-space |
|------|----------------|----------------|---------|
| Left (`ptr`) | original cdsp | `localcut` (up to cut) | same home-doc, first sub-range |
| Right (`new`) | `ptr->cdsp + localcut` | `original cwid - localcut` | same home-doc, second sub-range (contiguous) |

The two halves are **V-adjacent** (right-bro relationship) and reference **contiguous I-addresses** (same `c2dinfo.homedoc`, width split at the cut point).

---

### Step 3 — Rearrangement Displaces the Two Halves Differently

`makeoffsetsfor3or4cuts` [edit.c:177–183] for 3 blades:

```c
tumblersub(&knives->blades[2], &knives->blades[1], &diff[1]);  // diff[1] = C - B
tumblersub(&knives->blades[1], &knives->blades[0], &diff[2]);  // diff[2] = B - A
diff[2].sign = !diff[2].sign;                                   // negate → diff[2] = -(B-A)
tumblerclear(&(diff[3]));                                       // diff[3] = 0
```

`rearrangecutsectionnd` [edit.c:191–204] determines the section by iterating from the rightmost knife downward:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) return(-1);           // ERROR — must never happen post-cut
    else if (cmp <= ONMYLEFTBORDER) return(i+1);  // crum is at or right of this blade
}
return(0);
```

`ONMYLEFTBORDER = -1` [common.h:87], so `cmp <= ONMYLEFTBORDER` is true when the cut address is at or to the left of the crum.

For a crum originally straddling blade `k`, after cutting:

- **Left half** (ends exactly at blade[k]): `whereoncrum(..., blades[k])` → `ONMYRIGHTBORDER` (cut is on its right border, not ≤ ONMYLEFTBORDER). Loop continues to k-1, where the cut is to the left → returns **section k**.
- **Right half** (starts exactly at blade[k]): `whereoncrum(..., blades[k])` → `ONMYLEFTBORDER` (cut is on its left border, ≤ ONMYLEFTBORDER) → returns **section k+1**.

Then [edit.c:124–128]:
```c
case 1: case 2: case 3:
    tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
```

The displacement applied to each:

| Straddled blade | Left half section | Left half gets | Right half section | Right half gets |
|----------------|-------------------|-----------------|-------------------|-----------------|
| blade[0] = A | 0 | *no change* (case 0) | 1 | diff[1] = C−B |
| blade[1] = B | 1 | diff[1] = C−B | 2 | diff[2] = −(B−A) |
| blade[2] = C | 2 | diff[2] = −(B−A) | 3 | diff[3] = 0 |

In every non-degenerate case, the two halves receive **different offsets**. Their cdsp values diverge. They are no longer V-adjacent after rearrangement.

Their I-address content is unchanged: `move2dinfo` copied the home-doc reference at split time [ndcuts.c:447], and nothing in the rearrangement loop touches `c2dinfo`. The two bottom crums still reference the same underlying document at contiguous sub-ranges.

---

### Step 4 — Post-Rearrange Passes: No Coalescing

`rearrangend` ends with two calls [edit.c:137–141]:

```c
setwispupwards(father, 1);   // wisp bookkeeping only
recombine(fullcrumptr);
(void)splitcrumupwards(fullcrumptr);  /* can we move this before recombine ?*/
```

#### `recombine` [recombine.c:22–34, 104–131]

For SPAN/POOM, dispatches to `recombinend`:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2 || !father->modified) return(0);  // bails on height-1 and leaves
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend(ptr);
    getorderedsons(father, sons);
    for (i = 0; i < n-1; i++)
        for (j = i+1; ...; j++)
            if (ishouldbother(sons[i], sons[j]))
                takeovernephewsnd(&sons[i], &sons[j]);
```

`ishouldbother` [recombine.c:150–163] only checks whether the combined son count fits in a loaf and is not RESERVED. It has **no V-space adjacency check**. `takeovernephewsnd` [recombine.c:165–203] and `eatbrossubtreend` [recombine.c:205–232] move subtrees between upper-level nodes to consolidate partially-full loaves — they operate on **intermediate nodes**, not on bottom crums. The bottom crums themselves are not examined for V-space adjacency.

`getorderedsons` sorts by diagonal magnitude (`cdsp[0] + cdsp[1]`) [recombine.c:296–298], which is a spatial ordering heuristic, not an adjacency check. No merging of bottom crums occurs here.

#### `splitcrumupwards` [split.c:16–44]

```c
bool splitcrumupwards(typecuc *father)
{
    if (father->height <= 0) gerror("splitcrumupwards on bottom crum\n");
    for (; toomanysons(father); father = findfather(father)) {
        ...
        splitcrum(father);
    }
```

This only **splits** overfull nodes. It never merges.

**There is no coalescing pass.** The two fragments of the original crum remain as two separate bottom crums with non-contiguous V-space addresses and contiguous I-address content, indefinitely.

---

### Summary

1. **Splitting happens** in `slicecbcpm` [ndcuts.c:373–450] during the `makecutsnd` phase. A bottom crum straddling a 3-cut blade is bisected into two right-bro sibling crums sharing the same `c2dinfo.homedoc` and complementary widths — contiguous I-address content by construction.

2. **Non-contiguity in V-space follows** because `rearrangecutsectionnd` places the two halves in adjacent sections (k and k+1), and `makeoffsetsfor3or4cuts` assigns them different `diff[k]` and `diff[k+1]` values [edit.c:177–183], which are then applied directly to `cdsp` [edit.c:125].

3. **No coalescing pass exists** post-rearrange. `recombine` [recombine.c:104–131] reorganizes upper-level loaf occupancy using `takeovernephewsnd`/`eatbrossubtreend` but has no V-adjacency awareness and never touches bottom crum `cdsp` fields. `splitcrumupwards` [split.c:16–44] only splits. The comment at edit.c:141 — `/* can we move this before recombine ?*/` — reflects the author's own uncertainty about ordering, but neither ordering introduces coalescing.
