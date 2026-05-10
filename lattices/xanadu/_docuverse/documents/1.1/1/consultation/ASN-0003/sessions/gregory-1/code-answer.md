I now have everything needed for a complete answer. Let me synthesize all findings.

---

## REARRANGE

### Call Chain

```
fns.c:159     rearrange(taskptr)
  get1fe.c:65   getrearrange() → docisa tumbler + getcutseq()
  do1.c:34      dorearrange() → findorgl(WRITEBERT) + rearrangepm()
  orglinks.c:137  rearrangepm() → rearrangend(docorgl, cutseqptr, V)
  edit.c:78       rearrangend()     ← all real work here
```

### Wire Format

`get2fe.c:224-241` (`getcutseq`):
- The REARRANGE message contains: a `docisa` tumbler, then a count (must be exactly **3 or 4**), then that many tumbler addresses.
- `MAXCUTS = 4` [common.h:108].

```c
// get2fe.c:229-231
if (!(
   getnumber (taskptr, &ncuts)
&& (ncuts == 3 || ncuts == 4)))
    return (FALSE);
```

### What `rearrangend` Does

`edit.c:78-160`:

1. **Sort the cuts** [edit.c:107]: `sortknives()` — input order is irrelevant, cuts are sorted ascending by tumbler value before anything else.

2. **Compute displacement vectors** [edit.c:108]: `makeoffsetsfor3or4cuts(knives, diff)`.

3. **Cut the enfilade** [edit.c:110]: `makecutsnd()` — splits nodes at the cut boundaries so each crum falls cleanly within a single inter-cut region.

4. **Classify and shift each crum** [edit.c:113-136]: for each child crum of the intersection node, `rearrangecutsectionnd()` returns which region (0–4) the crum inhabits. Then:

```c
// edit.c:124-127
case 1: case 2: case 3:  /* 3 only moves in 4 cuts */
    tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
    ivemodified((typecorecrum*)ptr);
    break;
```

Only the V-displacement field (`cdsp.dsas[V]`) is modified. **I-addresses are untouched** — transclusion identity is fully preserved across a rearrange.

### 3-cut Mode: `pivot`

Cuts sorted as A < B < C. `makeoffsetsfor3or4cuts` [edit.c:177-181]:

```c
diff[1] = C - B   // blade[2] - blade[1]: width of region 2
diff[2] = -(B - A)  // negative width of region 1 (sign bit flipped)
diff[3] = 0
```

Region classification (from `rearrangecutsectionnd`):
- Region 0 (`< A`): no move (case 0)
- Region 1 (`[A, B)`): shifts by `+(C−B)`
- Region 2 (`[B, C)`): shifts by `−(B−A)`
- Region 3+ (`≥ C`): no move (case 3, diff[3]=0)

**Result** — the two adjacent segments exchange places:

```
Before:  [...][A...B)[B...C)[C...]
After:   [...][B...C)[A...B)[C...]
```

Total span [A, C) is preserved. This is a swap of two **contiguous** regions. `diff[1]` is the width of region 2 and `diff[2]` is the negative width of region 1 — each jumps exactly the width of the other. This is what the Python client exposes as `session.pivot(doc, A, B, C)` [docs/client-api.md:224-226].

### 4-cut Mode: `swap`

Cuts sorted as A < B < C < D. `makeoffsetsfor3or4cuts` [edit.c:169-176]:

```c
diff[1] = C - A          // blade[2] - blade[0]
a       = B - A          // width of region 1
b       = D - C          // width of region 3
diff[2] = b - a = (D-C) - (B-A)
diff[3] = -(C - A)       // negative of diff[1], sign flipped copy
// case 4 (≥ D): no move
```

Region classification:
- Region 0 (`< A`): no move
- Region 1 (`[A, B)`): shifts by `+(C−A)` → new start = A + (C−A) = C
- Region 2 (`[B, C)`): shifts by `(D−C) − (B−A)` (gap repositions)
- Region 3 (`[C, D)`): shifts by `−(C−A)` → new start = C − (C−A) = A
- Region 4 (`≥ D`): no move

**Result** — region 1 [A,B) lands at position C, region 3 [C,D) lands at position A, and the intervening gap [B,C) adjusts:

```
Before: [..][A..B)[B..C)[C..D)[D..]
After:  [..][C..D)[gap'][A..B)[D..]
```

Where the gap occupies `[A + (D−C), A + (D−C) + (C−B))` — it repositions to fill between the now-swapped regions.

**If the two regions have equal widths** (w₁ = w₃ = B−A = D−C): `diff[2] = 0`, so the gap doesn't move. The result is a clean swap of [A,B) and [C,D) with no discontinuity in V-space. This is what the Python client exposes as `session.swap(doc, A, B, C, D)` [docs/client-api.md:228-233].

**If the widths differ**: The gap repositions by `(D−C)−(B−A)`, and there is a discontinuity in V-space between region 1 (now at C) and region 4 (still at D). The document's V-space map becomes non-contiguous.

### Neither mode is a general permutation

Both the 3-cut and 4-cut forms are specific fixed permutations of 2 or 3 segments. The parameter structure (`typecutseq.cutsarray[MAXCUTS]` with MAXCUTS=4) physically prevents more than 4 cuts. You cannot express an arbitrary reordering of, say, 5 or more regions in a single REARRANGE operation.

---

## COPY

### Call Chain

```
fns.c:35       copy(taskptr)
  get1fe.c:54    getcopy() → docisa + vsa + specset
  do1.c:45       docopy()
    do2.c:14       specset2ispanset()   → convert V-specs to I-spans
    granf1.c       findorgl(WRITEBERT)  → get document's POOM orgl
    do2.c:110      acceptablevsa()      → always TRUE (stub!)
    orglinks.c:75  insertpm()           → insert into POOM
    spanf1.c       insertspanf()        → update spanfilade
```

### Wire Format

`get1fe.c:54-63` (`getcopy`):
```
docisa (tumbler) — target document
vsa    (tumbler) — V-address in target where content will be placed
specset          — source content specification (docid + V-spans)
```

### `acceptablevsa` is a stub

`do2.c:110-113`:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

There is **no precondition validation** on the target V-address. The function signature suggests it was meant to check that `vsaptr` falls within or at the boundary of the document's current V-span, but it was never implemented.

### What `insertpm` actually does

`orglinks.c:75-134` — for each span in the ispanset:

1. **Guard**: if `vsaptr` is zero, return FALSE [orglinks.c:86-91]. If negative, `gerror` [orglinks.c:93-98].

2. **Unpack source span**: extract I-stream (start address in permascroll), I-width, and `homedoc` info (which permascroll the content lives on) [orglinks.c:101].

3. **Build a 2D crum specification**:
   - `crumorigin.dsas[I] = lstream` — I-space start
   - `crumwidth.dsas[I] = lwidth` — I-space width
   - `crumorigin.dsas[V] = *vsaptr` — **V-space position = the target insertion address**
   - `crumwidth.dsas[V]` = computed to match the number of I-address units [orglinks.c:115-117]

4. **Call `insertnd(orgl, crumorigin, crumwidth, linfo, V)`** [orglinks.c:130] — inserts a new crum into the POOM.

5. **Advance the target vsa**: `tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr)` [orglinks.c:131] — so the next source span is placed immediately after the first.

### Does COPY shift subsequent content? Yes

`insertnd` → for POOM → calls `makegappm` first [insertnd.c:54]:

```c
// insertnd.c:53-61
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    doinsertnd(fullcrumptr, origin, width, infoptr, index);
    break;
```

`makegappm` [insertnd.c:124-172] — finds all crums whose V-displacement places them **at or after the insertion point** (case 1 in the switch), and shifts each one forward by the inserted width:

```c
// insertnd.c:161-164
case 1:
    tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
    ivemodified (ptr);
    break;
```

**COPY therefore shifts all subsequent V-content forward**, exactly as INSERT does. The only difference between INSERT and COPY is the source of I-addresses:

- **INSERT** [do1.c:87-123]: allocates fresh I-addresses in the granfilade via `inserttextingranf()`, then calls `docopy()` to place them.
- **COPY**: uses existing I-addresses from another document's content.

INSERT is literally implemented as `inserttextingranf` + `docopy`.

### Preconditions for COPY (actual)

| Precondition | Where enforced |
|---|---|
| Target document must be open with WRITE | `findorgl(WRITEBERT)` in `do1.c:55` |
| Source documents must be accessible | `specset2ispanset(NOBERTREQUIRED)` — somewhat permissive |
| Target vsa must not be zero | `insertpm` guard, `orglinks.c:86-91` |
| Target vsa must not be negative | `insertpm` gerror, `orglinks.c:93-98` |
| Target vsa within document bounds | **Not enforced** — `acceptablevsa` is a stub |
| Source spans must be non-empty | Implied by I-width check in `insertpm` (zero V-width causes gerror) |

There is no validation that the target V-address is within the document's current occupied V-span. You can COPY to an address beyond the current document end, creating a discontiguous V-space.

### Multiple source spans

If the source specset has multiple spans, `insertpm` processes them in sequence. Each span is placed at the then-current `vsaptr`, and `vsaptr` is advanced by that span's V-width before processing the next. Multiple spans from a source document are thus placed as a contiguous block in the target document, in source order.

---

## Summary

| | REARRANGE | COPY |
|---|---|---|
| New I-addresses? | No — existing crums only | No (reuses source I-addrs); INSERT does allocate via `docopy` |
| Shifts subsequent content? | No — only displaces selected regions | **Yes** — `makegappm` shifts everything after vsa forward |
| 3-cut form | Swap two adjacent regions [A,B)↔[B,C) | — |
| 4-cut form | Swap two non-contiguous regions [A,B)↔[C,D) + gap repositioning | — |
| General permutation? | **No** — limited to 2 or 3 contiguous segments | — |
| Source precondition | N/A | specset mapping to existing I-spans |
| Target precondition | — | vsa > 0; write-open doc; `acceptablevsa` is a stub (always TRUE) |