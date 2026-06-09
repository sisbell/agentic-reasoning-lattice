## Question 18 [evidence]

> For content structurally unchanged but newly displaced (the middle region in a swap), does it receive a fresh POOM entry or is its existing crum's V-displacement simply adjusted by `tumbleradd`/`tumblersub`?

## KB Synthesis

The existing crum's V-displacement is adjusted in-place. No fresh POOM entries are created.

[ST-REARRANGE] (Finding 0056) is explicit: REARRANGE operates entirely by calling `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` on each affected crum. The code at `backend/edit.c:125` overwrites the V-address component of the displacement directly — the same crum node, modified in-place.

For the middle region (region 2 in a 4-cut swap), the offset is `diff[2] = (cut3 - cut2) - (cut1 - cut0)` — the size difference between the two swapped regions. If the swapped regions are equal in size, `diff[2] = 0` and `tumbleradd` with a zero offset leaves those crums untouched. If they differ, the middle crums shift by exactly that difference, but via the same in-place mechanism.

[INV-REARRANGE-IDENTITY] (Finding 0056) confirms the corollary: "No new I-addresses are allocated, no content is duplicated in the permascroll, and **the same enfilade nodes (crums) are retained**." The I-address stored in each crum is never touched; only `cdsp.dsas[V]` changes.

This contrasts with INSERT, which creates new bottom crums. REARRANGE is a pure V-displacement mutation — no crum is born or freed, only their V-coordinates shift.

---

## Code Exploration

The code is verified. Here is the definitive answer.

---

## Answer: V-Displacement Adjusted In-Place — No Fresh POOM Entry

For content that is structurally unchanged but newly displaced (the middle region in a swap), the existing crum's V-displacement is adjusted in-place via `tumbleradd`/`tumblersub`. No new POOM entry is created.

---

### The Swap Path: `rearrangend`

A swap is a rearrange operation. The entry point is `rearrangend` in `backend/edit.c:78`.

**Step 1 — Cuts are made at all swap boundaries** (`edit.c:110`):
```c
makecutsnd (fullcrumptr, &knives);
```

**Step 2 — Offsets are precomputed per region** (`edit.c:108`):
```c
makeoffsetsfor3or4cuts (&knives, diff);
```

For a 4-cut swap (blocks A and C swapping across middle block B, cuts at p0, p1, p2, p3) the offsets in `makeoffsetsfor3or4cuts` (`edit.c:169–176`) are:
```c
diff[1] = blade[2] - blade[0]          // A shifts rightward by (p2 - p0)
diff[2] = (blade[3]-blade[2]) - (blade[1]-blade[0])  // B shifts by |C| - |A|
diff[3] = -(blade[2] - blade[0])       // C shifts leftward by (p2 - p0)
```

Region 2 is the middle block B — structurally unchanged, but displaced by `diff[2]`.

**Step 3 — Each crum is classified and its displacement adjusted** (`edit.c:113–128`):
```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4:           /* stationary — no change */
          break;
      case 1:  case 2:  case 3:  /* displaced regions */
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
          ivemodified((typecorecrum*)ptr);
          break;
    }
}
```

The crum at case 2 (middle region, block B) has its `cdsp.dsas[V]` incremented by `diff[2]`. That's the complete operation — no `createcrum()` call, no `reserve()`, no `adopt()`.

---

### The Insert Path: `makegappm`

The same pattern holds for a simple insertion. `makegappm` (`insertnd.c:124`) makes two cuts around the insertion origin, then walks children of the intersection node. Crums in the gap region (case 1) have V-displacement bumped by the inserted width (`insertnd.c:161–165`):

```c
case 1:  /*9-17-87 fix */
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

Again: existing crum, in-place field update, no new entry.

---

### The Delete Path: `deletend`

For deletion (`edit.c:31`), crums after the deleted span (case 2) have V-displacement decremented (`edit.c:62–65`):
```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

---

### Why No New Entry

The enfilade's POOM crums encode *permascroll addresses* of content. Because the permascroll is append-only and content identity never changes, displacing content only changes where it appears in virtual address space, not what it is. The V-displacement (`cdsp.dsas[V]`) stored in the crum is a relative offset from the parent — adjusting it in-place with `tumbleradd`/`tumblersub` is sufficient to relocate the crum in the virtual space without touching its I-address or creating a new entry.

A new crum is only created (via `createcrum` + `reserve` + `adopt`, `insertnd.c:260–262`) when genuinely new content is being added to the POOM — not when existing content shifts position.
