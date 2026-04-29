## Question 19 [gregory]

> In a 4-cut swap where the middle region `[b,c)` contains no POOM entries (a gap), does `rearrangend` still compute and apply offsets to the empty region, or does it skip the middle and only exchange the `[a,b)` and `[c,d)` regions?

## KB Synthesis

From [ST-REARRANGE] Finding 0056 and [EC-REARRANGE-EMPTY-REGION], the answer is clear:

**`rearrangend` always computes offsets for all regions from the cut geometry, but applies offsets only to the POOM entries that exist.**

The algorithm has two independent phases:

1. **Offset computation** (`makeoffsetsfor3or4cuts()`) — purely geometric, references only `knives->blades[]`. For a 4-cut swap at `cut0 < cut1 < cut2 < cut3`:
   - Region 1 `[cut0, cut1)`: `diff[1] = cut2 - cut0`
   - Region 2 `[cut1, cut2)`: `diff[2] = (cut3 - cut2) - (cut1 - cut0)`
   - Region 3 `[cut2, cut3)`: `diff[3] = -(cut2 - cut0)`

   This runs regardless of whether the middle is empty. The code at `edit.c:164-183` has no awareness of POOM state.

2. **Displacement application** — iterates over POOM entries, classifies each into a region via `rearrangecutsectionnd()`, then calls `tumbleradd` on the V-displacement. If no POOM entries fall in `[cut1, cut2)`, the middle offset is computed but never applied to anything.

[EC-REARRANGE-EMPTY-REGION] states this explicitly: "The algorithm operates per-span, and empty regions simply have no spans to process. This is correct behavior — the offset arithmetic is unaffected."

So for a swap where the middle is a gap: the two outer regions `[a,b)` and `[c,d)` are exchanged normally, and the empty middle contributes its size difference to the offset arithmetic but produces no displacement operations. The result is equivalent to a direct exchange of the two outer regions.

---

## Code Exploration

Now I have everything needed. Here is the complete analysis:

---

## Answer

### Short answer

`rearrangend` **always computes `diff[2]`** (the offset for the middle region), but **only applies it when nodes actually exist in `[b,c)`**. If the middle region is empty, `diff[2]` is silently a no-op. The `[a,b)` and `[c,d)` regions are swapped regardless.

---

### The computation: `makeoffsetsfor3or4cuts`

`rearrangend` calls `makeoffsetsfor3or4cuts` unconditionally before touching any nodes [`edit.c:108`]:

```c
makeoffsetsfor3or4cuts (&knives, diff);
```

For `nblades == 4` [`edit.c:169-176`]:

```c
tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));   // diff[1] = c - a
tumblersub (&knives->blades[1], &knives->blades[0], &a);            // a = b - a
tumblersub (&knives->blades[3], &knives->blades[2], &b);            // b = d - c
tumblersub (&b, &a, &(diff[2]));                                     // diff[2] = (d-c) - (b-a)
movetumbler (&diff[1], &diff[3]);
diff[3].sign = !diff[1].sign;                                        // diff[3] = -(c-a)
```

`diff[2]` is always computed. There is no guard checking whether any node occupies `[b,c)`.

---

### The classification: `rearrangecutsectionnd`

After cutting and finding the intersection father node, `rearrangend` iterates over all children and classifies each into a section number [`edit.c:113-114`]:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
```

`rearrangecutsectionnd` scans knives from highest to lowest and returns the first `i+1` where `knife[i] <= node.start` [`edit.c:195-203`]:

```c
for (i = knives->nblades -1; i >= 0 ; --i) {
    cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)       return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (i+1);
}
return (0);
```

`whereoncrum` for a POOM node with DSP `d` and WID `w` [`retrie.c:356-372`]:
- Returns `ONMYLEFTBORDER` (-1) when `address == node.start`
- Returns `THRUME` (0) when `node.start < address < node.end`
- Returns `TOMYRIGHT` (> 1) when `address > node.end`

So `cmp <= ONMYLEFTBORDER` is true when `address <= node.start` — the knife is at or before the node's left border.

For 4 knives `a < b < c < d`, the section assignments are:

| Node range | Section returned |
|---|---|
| `(-∞, a)` | 0 — never moves |
| `[a, b)` | 1 — shifted by `diff[1]` = `c−a` (moves right) |
| `[b, c)` | 2 — shifted by `diff[2]` = `(d−c)−(b−a)` |
| `[c, d)` | 3 — shifted by `diff[3]` = `a−c` (moves left) |
| `[d, ∞)` | 4 — never moves |

---

### The application: the switch in `rearrangend`

```c
switch (i) {
  case 0:  case 4: /* these never move */
      break;
  case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
      tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
      ivemodified((typecorecrum*)ptr);
      break;
```
[`edit.c:122-128`]

**The loop iterates only over existing children.** If the middle region `[b,c)` is empty, no child node will ever be classified as section 2, and thus `diff[2]` is never passed to `tumbleradd`. There is no explicit skip — the emptiness is simply handled by the fact that the iteration produces no case-2 nodes.

---

### Conclusion

1. **`diff[2]` is always computed** by `makeoffsetsfor3or4cuts`, regardless of whether `[b,c)` is populated [`edit.c:108`, `edit.c:173`].

2. **`diff[2]` is never applied when `[b,c)` is empty.** The application loop is node-driven, not region-driven. Zero nodes in section 2 → zero applications of `diff[2]`.

3. **The swap still executes correctly.** Nodes in `[a,b)` receive `diff[1] = c−a` (shift right) and nodes in `[c,d)` receive `diff[3] = a−c` (shift left). An empty middle region is transparently a no-op; `rearrangend` does not need to special-case it.
