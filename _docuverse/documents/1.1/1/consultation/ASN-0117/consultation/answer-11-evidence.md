## Question 11 [evidence]

> When DELETE targets a span, does `slicecbcpm` only fire for entries that partially overlap the cut boundaries (interior cuts where `whereoncrum == THRUME`), while entries entirely within the span are disowned and freed via `subtreefree`?

## KB Synthesis

Yes, that is exactly correct. The KB documents this two-phase DELETE mechanism precisely.

**Phase 1 — Cutting (`slicecbcpm`):**

`slicecbcpm` fires **only** when a cut boundary falls strictly interior to a crum. [PRE-DELETE/Finding 0075] establishes that `makecutsbackuptohere()` guards the call with `whereoncrum() == THRUME` — i.e., `grasp < cut < reach` with strict inequalities on both sides. When a boundary aligns exactly with a crum's grasp (`ONMYLEFTBORDER`) or reach (`ONMYRIGHTBORDER`), `slicecbcpm` is skipped entirely. The crum is instead processed whole in Phase 2. [INV-NO-ZERO-WIDTH-CRUM] confirms this structural guard ensures the split always produces two positive-width halves.

**Phase 2 — Classification (`deletend` case analysis):**

After any necessary boundary splits, each bottom crum falls into one of three cases:

- **Case 1** (crum falls entirely within the deletion range): `disown` + `subtreefree` — the crum is removed from the tree and its memory freed. This is how bulk deletion works. [ST-DELETE/Finding 0064]
- **Case 2** (crum falls entirely after the deletion end): V-position shifted backward via `tumblersub`. [ST-DELETE/Finding 0053, 0055]
- **Case 0** (crum falls entirely before the deletion start): no change.

[ST-DELETE/Finding 0058] confirms that after all bottom crums within the range are disowned and freed, `setwispupwards` and `recombine` rebalance the parent nodes. Crums at exact boundaries (post-Phase-1 split) are handled whole as Case 0 or Case 1, never split again.

---

## Code Exploration

I now have all the code needed to give a precise, cited answer.

---

## Answer

Yes — the characterization is exactly correct. Here is the complete traced evidence.

---

## Call Chain

```
fns.c:333      deletevspan()
  do1.c:165    dodeletevspan() → findorgl() && deletevspanpm()
  orglinks.c:149 deletevspanpm() → deletend(docorgl, &vspanptr->stream, &vspanptr->width, V)
  edit.c:31    deletend()
```

`deletend` operates in two distinct phases.

---

## Phase 1 — `makecutsnd`: Split Only the Boundary Nodes

`edit.c:40-44` sets up two knives and fires the cut machinery:

```c
movetumbler (origin, &knives.blades[0]);          // left boundary of delete zone
tumbleradd (origin, width, &knives.blades[1]);    // right boundary
knives.nblades = 2;
...
makecutsnd (fullcrumptr, &knives);               // edit.c:44
```

`makecutsnd` → `makecutsdownnd` → `makecutsbackuptohere` (`ndcuts.c:69`).

At leaf nodes (`height == 0`), `makecutsbackuptohere` iterates over every knife and checks [`ndcuts.c:77-91`]:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
              new = (typecuc *)createcrum((INT)ptr->height,(INT)ptr->cenftype);
              ...
              slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

**`slicecbcpm` is called if and only if `whereoncrum == THRUME`** — the knife falls strictly inside the leaf's interval.

`slicecbcpm` enforces this as a hard precondition at `ndcuts.c:383`:

```c
if (whereoncrum (ptr, offset, cut, index) != THRUME)
    gerror ("Why are you trying to slice me?\n");
```

`THRUME` is defined `common.h:88`:

```c
#define TOMYLEFT       -2  // address < crum_start
#define ONMYLEFTBORDER -1  // address == crum_start
#define THRUME          0  // crum_start < address < crum_end  (interior)
#define ONMYRIGHTBORDER  1  // address == crum_end
#define TOMYRIGHT        2  // address > crum_end
```

So `THRUME` means the address (knife position) falls **strictly inside** the crum's span — a genuine partial-overlap boundary case. `slicecbcpm` splits that leaf into two adjacent leaves; after the split, neither successor is `THRUME` for that knife. Nodes that do **not** straddle any knife are skipped entirely in this phase.

---

## Phase 2 — `deletecutsectionnd` + `subtreefree`: Classify and Free Interior Nodes

After `makecutsnd`, `deletend` calls `newfindintersectionnd` (which at `ndinters.c:38-42` in its current simplified form simply returns the fullcrum root), then iterates over children [`edit.c:47-73`]:

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case -1:  gerror ("deletend can't classify crum\n");   // THRUME: must never happen
      case  0:  break;                                        // before delete zone — untouched
      case  1:  disown ((typecorecrum*)ptr);                  // edit.c:59-61
                subtreefree ((typecorecrum*)ptr);             // entirely within zone — freed
                break;
      case  2:  tumblersub (&ptr->cdsp.dsas[index], width,   // edit.c:63
                            &ptr->cdsp.dsas[index]);          // after zone — offset adjusted
                break;
    }
}
```

`deletecutsectionnd` (`edit.c:235-248`) iterates knives in reverse (right-to-left):

```c
for (i = knives->nblades-1; i >= 0; --i) {   // i=1 first, then i=0
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME) {
        return (-1);          // error guard — must not happen after makecutsnd
    } else if (cmp <= ONMYLEFTBORDER) {   // knife is at or left of crum's start
        return (i+1);
    }
}
return (0);
```

For 2 knives (blades[0]=start, blades[1]=end of deleted span):

| Check | Meaning | Return | Action in `deletend` |
|---|---|---|---|
| `blades[1] <= ONMYLEFTBORDER` | crum starts at or after end cut → entirely **after** delete zone | `2` | Offset adjusted |
| `blades[0] <= ONMYLEFTBORDER` | crum starts at or after start cut but not past end cut → entirely **within** delete zone | `1` | `disown` + `subtreefree` |
| Neither | crum ends before or at start cut → entirely **before** delete zone | `0` | Untouched |
| `THRUME` for any knife | crum straddles a knife — shouldn't exist after `makecutsnd` | `-1` | `gerror` |

`subtreefree` (`credel.c:413`) recursively disowns and frees the entire subtree:

```c
void subtreefree(typecorecrum *ptr) {
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);               // credel.c:427
        }
    }
    freecrum (ptr);
}
```

---

## Conclusion

The two phases are cleanly separated by design:

1. **`slicecbcpm`** fires **only** during `makecutsnd`, **only** for leaf nodes where `whereoncrum == THRUME` — i.e., exactly the nodes whose span interval is crossed by a cut boundary. It splits such a node in two so the boundary aligns with a node edge.

2. After that surgical splitting, **no node straddles a knife**. `deletecutsectionnd` is guaranteed never to return `-1`. Nodes entirely within the deleted span return `1` and are disposed of exclusively via `disown` + `subtreefree` (`edit.c:59-61`). `slicecbcpm` is not involved in their disposal at all.
