## Question 13 [evidence]

> For each returned VSpec, must its start position be the subspace's minimum occupied V-address and its width exactly span to the maximum occupied V-address, or can the reported span overshoot into unoccupied positions within that subspace?

## KB Synthesis

## RETRIEVEDOCVSPANSET: Bounding Box, Not Tight Coverage

The returned VSpec **starts at the minimum occupied V-address** and its width **spans to the maximum occupied reach** — a bounding box that can include unoccupied gaps within a subspace.

### Mechanism

`retrievevspansetpm()` constructs each subspace span by reading the POOM root's `cdsp.dsas[V]` (minimum V-address) and `cwid.dsas[V]` (extent from min to max) [SS-DUAL-ENFILADE, Finding 0043]. The 2D enfilade root's `cdsp`/`cwid` form a bounding box: `root.cdsp` is the minimum address across all content, `root.cdsp + root.cwid` is the maximum reach [SS-ENFILADE-TREE, Finding 0066]. `setwispnd` maintains this bounding box, not a tight per-occupied-position catalog.

The split between subspaces (1.x text, 2.x links) happens once via `is1story`, but **within each subspace there is only one returned VSpec** — the bounding box of everything in that subspace [SS-VSPAN-VS-VSPANSET, Finding 0017, 0035].

### Can the span overshoot?

Yes, if content within a subspace is non-contiguous (e.g., text inserted at 1.1 and 1.20 with nothing between), the reported span covers 1.1 through 1.20+width, including the unoccupied gap.

In **normal sequential use**, this doesn't arise: INSERT shifts existing content forward, keeping content contiguous. INV-VSPAN-CONSOLIDATION [SS-POOM-MULTIMAP] confirms consecutive adjacent inserts consolidate into one crum, producing a tight span. But the invariant guarantees consolidation for contiguous content, not that all content is always contiguous.

The `retrievedocumentpartofvspanpm` function is explicitly labeled "a kluge" in the source [SS-DUAL-ENFILADE, Finding 0043] — it reads raw root values precisely because they are the bounding box, not a computed tight extent.

**Summary:** Start = minimum occupied V-address (exact). Width = bounding box to maximum reach (can include gaps within the subspace if content is non-contiguous).

---

## Code Exploration

---

## Answer

The outer boundaries of a returned VSpec are **tight** — no overshoot beyond the minimum or maximum occupied V-address. However, the span's interior **can and does contain unoccupied positions** wherever the underlying enfilade children are non-adjacent.

---

### The Width Maintenance Invariant: `setwispnd()`

The core function is `setwispnd()` in `backend/wisp.c:171–228`, called via `setwispupwards()` after every insertion. It recalculates each POOM/SPAN node's bounding box from its children:

**Left boundary — minimum displacement across children** [`wisp.c:193–195`]:
```c
movewisp (&ptr->cdsp, &mindsp);            /* start with first child's dsp */
for (ptr = getrightbro(ptr); ptr; ...) {
    lockmin(&mindsp, &ptr->cdsp, &mindsp, ...);  /* take component-wise min */
}
```

**Right boundary — maximum right-edge across children** [`wisp.c:208–214`]:
```c
for (ptr = findleftson(father); ptr; ...) {
    dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ...);        /* re-origin children */
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, ...);      /* child_start + child_width */
    lockmax(&newwid, &tempwid, &newwid, ...);             /* running maximum right-edge */
}
```

**Stored back to node** [`wisp.c:224–225`]:
```c
movewisp (&newdsp, &father->cdsp);   /* father->cdsp = min occupied start */
movewisp (&newwid, &father->cwid);   /* father->cwid = max occupied end − min occupied start */
```

`setwispupwards()` [`wisp.c:83–111`] propagates this all the way to the root after every mutation, so the root node always holds exact outer boundaries.

---

### How the VSpec is Built from Those Bounds

`retrievevspanpm()` [`backend/orglinks.c:165–172`] constructs a VSpec by copying the root crum's fields directly:

```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  /* line 169 */
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   /* line 170 */
```

No adjustment or tightening occurs here. The VSpec stream is exactly the minimum occupied V-address and stream+width is exactly the maximum occupied V-address, as maintained by `setwispnd`.

The 1-story branch of `retrievevspansetpm()` [`orglinks.c:184–190`] does the same:
```c
movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
```

---

### Internal Gaps: Overshoot Within the Span

The critical point: `setwispnd` produces a **bounding box**, not an occupancy map. Consider a document with text crums at V-addresses 2–3 and 7–8 (gap at 4–6). After `setwispnd`, the parent node holds:
- `cdsp.dsas[V]` = 2 (minimum child start)
- `cwid.dsas[V]` = 6 (rightmost edge 8 − leftmost start 2)

The reported VSpec is [2, 2+6] = [2, 8]. Addresses 4–6 are **within the reported span but entirely unoccupied**. The code between `lockmin` and `lockmax` has no mechanism to detect or exclude these holes.

There is no insertion-time guard that prevents non-contiguous children. `insertcbcnd()` [`insertnd.c:242–274`] places nodes at arbitrary positions via `adopt()`, and the gap-making logic in `makegappm()` [`insertnd.c:124–172`] only shifts existing children to make room — it does not enforce contiguity.

---

### No Insertion-Time Occupancy Validation

`acceptablevsa()` [`backend/do2.c:110–113`] is called by `docopy()` to validate a target V-address before insertion:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

This is a stub that accepts any V-address unconditionally. There is no check whether the proposed address is already occupied, adjacent to occupied space, or creates a gap.

---

### The Multi-Story Exception (`retrievevspansetpm`)

For documents with link parts, `retrievevspansetpm()` [`orglinks.c:173–221`] diverges from the bounding-box pattern. It calls `maxtextwid()` [`orglinks.c:224–245`]:

```c
tumbleradd(voffset, &crumptr->cdsp.dsas[V], &tmpwid);  /* accumulate to leaf V-start */
tumblermax(&tmpwid, maxwidptr, maxwidptr);              /* track maximum leaf V-start */
```

`maxtextwid` computes the V-start of the farthest text leaf — **not** that leaf's end (V-start + cwid). The resulting VSpec gets `stream = 0` and `width = maxwid` with `mantissa[0]` zeroed [`orglinks.c:209–211`]. This path does **not** use the `setwispnd`-maintained bounds and in fact undershoots the far end by the width of the last text crum.

---

### Summary

| Property | Behavior | Evidence |
|---|---|---|
| VSpec start = min occupied V-address | **Yes** (tight left edge) | `setwispnd` `lockmin` loop [`wisp.c:193–195`] |
| VSpec end = max occupied V-address | **Yes** (tight right edge) | `setwispnd` `lockmax` loop [`wisp.c:213–214`] |
| Interior may contain unoccupied V-addresses | **Yes** (internal gaps preserved) | `setwispnd` is a bounding box, not occupancy set |
| Overshoot beyond max occupied address | **No** for `retrievevspanpm` path | `setwispnd` right edge is exact |
| Undershoot at far end | **Yes** for `retrievevspansetpm` multi-story path | `maxtextwid` reports leaf V-start, not leaf V-end [`orglinks.c:235`] |
| Any enforcement of occupancy at insertion | **No** | `acceptablevsa` is a stub returning TRUE [`do2.c:112`] |

**The definitive answer:** A returned VSpec's outer boundaries (start and start+width) are exactly the minimum and maximum occupied V-addresses in the subspace, as guaranteed by `setwispnd`'s bounding-box propagation. The span does **not** overshoot those outer edges. But the span is a bounding box, not a dense occupancy descriptor — it freely spans internal unoccupied gaps between non-adjacent occupied regions. Any code consuming a VSpec must not assume contiguous occupancy across the entire reported range.
