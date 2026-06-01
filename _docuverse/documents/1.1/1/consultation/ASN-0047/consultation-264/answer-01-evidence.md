## Question 1 [evidence]

> When DELETEVSPAN removes an interior link, does the POOM leave a gap at that V-position or compact-and-renumber every subsequent link's V-address, and is the surviving order otherwise preserved?

## KB Synthesis

## DELETEVSPAN on an Interior Link: Gap, Not Compaction

**A gap is left.** Subsequent links retain their original V-addresses unchanged.

### Mechanism

When `DELETEVSPAN(2.2, width=0.1)` removes the second link from a document containing links at `2.1`, `2.2`, `2.3`:

**Phase 1 (cutting):** The crum covering `[2.2, 2.3)` has its boundaries exactly aligned with the deletion range. `whereoncrum` returns `ONMYLEFTBORDER` at `2.2` and `ONMYRIGHTBORDER` at `2.3`, so `slicecbcpm` is never called — no splitting occurs [PRE-DELETE, Finding 0075].

**Phase 2 (classify/remove):** The aligned crum is classified as Case 1 (fully within deletion range) and removed via `disown` + `subtreefree` [ST-DELETE, Finding 0064].

**The shift non-event:** `deletend` Case 2 would normally subtract the deletion width from subsequent entries. For links at `2.3`, `2.4` (displacement exponent = 0) and deletion width `0.1` (exponent = -1), `strongsub` fires its exponent guard: `width.exp(-1) < entry.vpos.exp(0)` → returns the entry's displacement unchanged [FC-SUBSPACE, Finding 0055]. This is the same incidental arithmetic guard that prevents text deletions from shifting link entries, documented in [INT-DELETE-SUBSPACE-ASYMMETRY].

### Result

After removing the link at `2.2`:
- Link at `2.1` stays at `2.1`  
- Link formerly at `2.3` stays at `2.3` (gap at `2.2`)
- `retrieve_vspanset` no longer shows a span at `2.2`
- The surviving link order is fully preserved; only the deleted entry is absent

This behavior is the same incidental protection described for text-delete's effect on the link subspace [FC-SUBSPACE, Finding 0055], applied within the link subspace itself. Unlike INSERT (which uses a deliberate two-blade knife to enforce subspace boundaries [SS-TWO-BLADE-KNIFE]), DELETE relies entirely on `strongsub`'s exponent arithmetic — the gap behavior is structurally accidental, not designed.

---

## Code Exploration

All citations confirmed. Here is the complete answer.

---

## DELETEVSPAN and POOM V-Address Behavior

**Answer: compact-and-renumber (b).** No gap is left. Every node whose V-address falls *after* the deleted span has its V-address decremented by the deleted width. Surviving order is preserved.

---

### Call Chain

**`fns.c:333` — FEBE entry point**
```c
void deletevspan(typetask *taskptr)
{
    (void) getdeletevspan (taskptr, &docisa, &vspan);  // fns.c:339
    putdeletevspan (taskptr);                          // fns.c:340
    if (!dodeletevspan (taskptr, &docisa, &vspan))     // fns.c:341
```

**`do1.c:158` — `dodeletevspan`**
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)   // do1.c:164
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)        // do1.c:165
```

**`orglinks.c:145` — `deletevspanpm`**
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // orglinks.c:149
    logbertmodified(docisaptr, user);
    return (TRUE);
```

The three arguments to `deletend` are: the POOM root, the deletion start (V-stream origin), the deletion width, and the dimension index `V`. This is the point where POOM topology is modified.

---

### Core Logic in `deletend` (`edit.c:31`)

**Knife setup** — two boundary addresses divide V-space into three regions:

```c
movetumbler (origin, &knives.blades[0]);          // edit.c:40 — left boundary
tumbleradd (origin, width, &knives.blades[1]);    // edit.c:41 — right boundary
knives.nblades = 2;                               // edit.c:42
knives.dimension = index;                         // edit.c:43
makecutsnd (fullcrumptr, &knives);                // edit.c:44 — split nodes at boundaries
```

`makecutsnd` pre-splits any nodes that straddle a boundary so that every surviving node falls cleanly into one of three regions: entirely before, entirely within, or entirely after the deletion range.

**Classification and action loop** (`edit.c:47–73`):

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {    // edit.c:47
    next = (typecuc *) findrightbro((typecorecrum*)ptr);            // edit.c:48
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 0:
        break;                        // before deletion — no action
      case 1:
        disown ((typecorecrum*)ptr);  // edit.c:59 — overlaps deletion — detach
        subtreefree ((typecorecrum*)ptr); // edit.c:60 — and free
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); // edit.c:63
        break;                        // after deletion — RENUMBER
    }
}
```

**`edit.c:63` is the decisive line.** For every node whose V-address lies entirely *after* the deleted region (case 2), the code subtracts the deleted `width` from `ptr->cdsp.dsas[V]` in-place. There is no conditional, no gap-leave path. Renumbering is unconditional.

---

### Classification Logic in `deletecutsectionnd` (`edit.c:235`)

```c
INT deletecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    for (i = knives->nblades-1; i >= 0; --i) {         // iterate blades right-to-left
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);                               // address inside crum — error
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);                              // which side of blade[i] we're on
        }
    }
    return (0);                                        // all blades to the right — crum before deletion
```

With two blades (at `origin` and `origin+width`):
- **Return 0**: crum entirely before `origin` → no action
- **Return 1**: crum's right edge crosses `origin` but not `origin+width` → delete (overlaps)
- **Return 2**: crum entirely after `origin+width` → renumber by `tumblersub`

---

### Symmetry Confirms Design Intent

Insertion (`insertnd.c:124`, `makegappm`) performs the exact inverse. When a gap is opened, nodes *after* the insertion point are shifted *forward*:

```c
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]); // insertnd.c:162
```

Deletion subtracts the width; insertion adds it. The design consistently maintains dense, gapless V-addressing in both directions.

---

### Order Preservation

The loop at `edit.c:47` iterates via `findleftson` → `findrightbro`, which traverses children strictly left-to-right in V-order. Renumbering only adjusts address values, never moves nodes between positions in the tree. The relative order of surviving crums is therefore unchanged: a node that was the k-th entry before deletion remains the k-th surviving entry after.

---

### Summary

| Region | Action at `edit.c:49–72` |
|---|---|
| Before deletion (`case 0`) | No change |
| Within deleted span (`case 1`) | `disown` + `subtreefree` — node removed |
| After deleted span (`case 2`) | `tumblersub` shifts V-address back by `width` |

The POOM never leaves a gap. Deletion of an interior link closes the hole immediately by renumbering every subsequent link downward by the deleted width. Surviving link order is preserved.
