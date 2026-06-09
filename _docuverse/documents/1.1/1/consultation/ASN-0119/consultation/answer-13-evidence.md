## Question 13 [evidence]

> Does the total root width (V-extent) of the document's text subspace remain invariant across REARRANGE, given that `rearrangend` only redistributes offsets among existing crums rather than allocating or freeing span?

## KB Synthesis

Yes, the total root V-extent (text subspace width) is invariant under REARRANGE.

**Mechanism**

[ST-REARRANGE] (Finding 0056) confirms that `rearrangend` applies `tumbleradd` to each crum's V-displacement — no crums are allocated, freed, or split. The full content set is permuted in place.

**The offsets are zero-net within the cut region.** For pivot with cuts `c₀ < c₁ < c₂`:

- `diff[1] = +(c₂ − c₁)` — region 1 moves right by region 2's width
- `diff[2] = −(c₁ − c₀)` — region 2 moves left by region 1's width

After displacement, region 2 occupies `[c₀, c₀+c₂−c₁)` and region 1 occupies `[c₀+c₂−c₁, c₂)` — together they still tile exactly `[c₀, c₂)`. The same tiling argument holds for swap (4-cut case). [FC-REARRANGE-EXTERIOR] confirms content outside `[c₀, c₂)` is untouched.

**Root width recalculation.** [INV-ENFILADE-RELATIVE-ADDRESSING] documents that `setwispupwards` recomputes `root.cdsp` as the minimum displacement across all children after any modification. Since REARRANGE is a permutation of positions — the minimum and maximum V-addresses across all crums are unchanged — `root.cwid = max_pos − min_pos` comes out identical.

This is structurally confirmed by [INV-REARRANGE-IDENTITY]: the multiset of I-addresses in the document (and by extension the total V-space occupied) is invariant under REARRANGE. No content is created or destroyed, only reordered.

---

## Code Exploration

I have all the evidence I need. Here is the complete analysis with line-level citations.

---

## V-Extent Invariance Across REARRANGE

**Verdict: Yes, the root V-extent is invariant across REARRANGE.** The code confirms this structurally, and Roger Gregory's own comment at `backend/edit.c:137` states it directly.

---

### Call Chain

```
FEBE REARRANGE command
  → dorearrange()          do1.c:34
  → rearrangepm()          orglinks.c:137
  → rearrangend()          edit.c:78
```

`rearrangepm` at `backend/orglinks.c:137-142` passes the `V` dimension index directly:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

---

### What `rearrangend` Actually Does

`backend/edit.c:78-160`. The critical section is the main loop over children of `father`:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
    i = rearrangecutsectionnd(...);          // classify which slice
    switch (i) {
      case 0: case 4:                        // never move
        break;
      case 1: case 2: case 3:               // move by adding diff[i]
        tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
        ivemodified((typecorecrum*)ptr);
        break;
    }
}
```
`backend/edit.c:113-135`

**Only `cdsp` (displacement) is modified. `cwid` (width) is never touched.** There are no calls to `freecrum`, no span content allocations, and no writes to any `cwid` field anywhere in `rearrangend`.

After the loop:

```c
setwispupwards (father,1); /* should do nothing, */
                           /* but, just on general principles.. */
recombine (fullcrumptr);
```
`backend/edit.c:137-139`

The comment **"should do nothing"** is Roger Gregory's own assertion that V-extent is invariant: the `setwispupwards` call is a defensive no-op, not a correctness fix.

---

### Offset Arithmetic Preserves the Span Partition

`makeoffsetsfor3or4cuts` at `backend/edit.c:164-184` computes `diff[]` values for 3-cut and 4-cut cases:

**3-cut case** (swapping slices 1 and 2):
```c
diff[1] = blades[2] - blades[1]    // slice 1 moves right by |slice_2|
diff[2] = -(blades[1] - blades[0]) // slice 2 moves left by |slice_1|
diff[3] = 0                         // unused
```

After redistribution:
- Slice 2 (B) moves to `[blades[0], blades[0] + (blades[2]-blades[1]))`
- Slice 1 (A) moves to `[blades[0] + (blades[2]-blades[1]), blades[2])`

The rightmost populated position after the swap is still `blades[2]`. Slices 0 and 4 (outside the cut range) never move (`case 0` and `case 4` at `backend/edit.c:122`), so the document's upper extent is unchanged.

**4-cut case** (`diff[3] = -diff[1]` at `backend/edit.c:175-176`) is constructed with the same conserved-extent property.

---

### Width Recalculation Confirms Invariance

`setwispnd` at `backend/wisp.c:171-228` recomputes node widths bottom-up:

```c
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
        (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));   // tempwid = cdsp + cwid
lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
        (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));    // newwid = max so far
```
`backend/wisp.c:213-214`

Root width = max over all children of `(child_cdsp + child_cwid)`.

Since:
1. Every leaf's `cwid` is unchanged (never written in `rearrangend`), and
2. The `diff[]` values redistribute positions without truncation or extension, and
3. The rightmost crum (in slice 4) never moves,

the maximum of `(cdsp + cwid)` is identical before and after the operation. This is precisely why the author wrote "should do nothing" — `setwispupwards` recalculates and confirms the root's `cwid` hasn't changed.

---

### Summary of Evidence

| Claim | Location |
|---|---|
| Only `cdsp` is written in the main loop | `backend/edit.c:125` |
| `cwid` is never written in `rearrangend` | `backend/edit.c:78-160` (no `cwid` assignment) |
| Slices 0 and 4 never move | `backend/edit.c:122` |
| `diff[]` values swap slices without growing total span | `backend/edit.c:164-184` |
| Author's own assertion: `setwispupwards` "should do nothing" | `backend/edit.c:137` |
| Root width = max(cdsp + cwid) over children | `backend/wisp.c:213-214` |
| Dispatch passes `V` index directly | `backend/orglinks.c:139` |

**Conclusion:** V-extent invariance is structural, not coincidental. `rearrangend` permutes the positions of existing crums (modifying only `cdsp`) without ever adding, removing, or resizing span content (`cwid`). The root width, computed as the maximum reach of any child, covers the same range before and after the operation. The design comment at `backend/edit.c:137` is the author confirming this property in the code itself.
