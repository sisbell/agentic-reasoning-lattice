## Question 19 [gregory]

> When a DELETE operation slices a bottom crum that maps a contiguous V-span to a contiguous I-span, does the surviving fragment preserve the exact I-displacement and I-width corresponding to the surviving V-range, or is there any rounding or alignment to tumbler boundaries?

## KB Synthesis

## DELETE Crum Slicing: I-Space Precision

The surviving fragment preserves the **exact** I-displacement and I-width with no rounding or alignment. Here is why:

**The linear 1:1 mapping within a crum**

A POOM bottom crum represents a linear V→I mapping: `poom(V_start + k) = I_start + k` for each byte offset `k` in `[0, width)`. This is guaranteed by [INV-SINGLE-CHAR-GRANULARITY] (one I-address per byte) and [SS-POOM-BOTTOM-CRUM]'s dual-origin structure.

**The slicing arithmetic**

When `slicecbcpm` is called (only when `whereoncrum == THRUME`, per [PRE-DELETE] Finding 0075), it computes:

```
localcut = tumblersub(cut, &grasp)   // V-space offset from crum start to cut
```

Because the V→I mapping is identity (offset `k` in V-space corresponds to offset `k` in I-space), `localcut` as an integer byte count simultaneously identifies the V-split and the I-split. The two resulting fragments are:

- **Left fragment**: V-span `[V_grasp, cut)`, I-span `[I_origin, I_origin + localcut)` — width = `localcut`
- **Right fragment**: V-span `[cut, V_reach)`, I-span `[I_origin + localcut, I_origin + cwid)` — width = `cwid - localcut` via `locksubtract` at `ndcuts.c:444`

**No representational ambiguity**

Both `localcut` and `cwid - localcut` are strictly positive (enforced structurally by the THRUME guard), per [INV-NO-ZERO-WIDTH-CRUM]. V-positions and I-positions in a text crum are both integer byte counts, so the arithmetic produces an exact representable integer with no fractional component.

[INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076) guarantees that V-width and I-width always encode the same numeric integer value, just at different tumbler exponents. When `slicecbcpm` re-encodes `localcut` for the I-dimension of the left fragment (using `tumblerlength(vsa)` as the precision anchor, per [SS-INSERT-VWIDTH-ENCODING]), the underlying integer is preserved exactly.

**Tumbler precision is not a constraint here**

The 16-digit mantissa limit [SS-TUMBLER] could theoretically be a concern, but byte-offset values within a single document's text span fit easily within this precision. The cut point within a crum is an integer in `[1, cwid-1]`, and these values are well within the representable range.

**Conclusion**: the cut is a clean integer partition of both the V-span and the I-span at the exact same byte offset. There is no sub-tumbler rounding.

---

## Code Exploration

I now have all the information needed. Here is the complete answer.

---

## Answer: I-Displacement and I-Width Preservation During Crum Slicing

**The surviving fragment preserves the exact I-displacement and I-width corresponding to the surviving V-range. There is no rounding or alignment to tumbler boundaries.**

Here is the full execution path and arithmetic proof.

---

### 1. Entry point: `dodeletevspan` → `deletevspanpm` → `deletend`

`dodeletevspan` [do1.c:158-167] calls `deletevspanpm` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` [edit.c:31-76] places two knife blades at `origin` and `origin+width` on the V-axis, calls `makecutsnd` to split crums at those positions, then iterates over affected crums and either deletes them (`case 1`: fully inside the deleted span) or adjusts their V-displacement (`case 2`: survivors to the right, via `tumblersub`). Case 2 only touches `cdsp.dsas[index]` — **not** the I dimension [edit.c:63]:

```c
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

The I-split happens earlier, inside `makecutsnd`.

---

### 2. Cutting: `makecutsnd` → `makecutsbackuptohere` → `slicecbcpm`

`makecutsnd` [ndcuts.c:15-31] drives `makecutsbackuptohere`, which at height == 0 (bottom crum level) does [ndcuts.c:77-91]:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

`THRUME` means "the knife passes through this crum's interior" — i.e., this is a crum that must be split.

---

### 3. The slice: `slicecbcpm` [ndcuts.c:373-450]

This is the key function. Walk through it step by step:

**Step A — Compute absolute V-start of the crum** [ndcuts.c:382]:
```c
prologuend(ptr, offset, &grasp, NULL);
// grasp.dsas[V] = offset->dsas[V] + ptr->cdsp.dsas[V]  (absolute V-origin)
// grasp.dsas[I] = offset->dsas[I] + ptr->cdsp.dsas[I]  (absolute I-origin)
```

**Step B — Compute `localcut`: the V-distance from the crum's left edge to the knife** [ndcuts.c:396]:
```c
tumblersub(cut, &grasp.dsas[index], &localcut);
// localcut = cut_V - crum_V_start
// = number of V-units from crum left-edge to the cut
// = V-width of the left fragment
```

**Step C — Precondition checks** [ndcuts.c:389-436]:

1. `lockis1story(ptr->cwid.dsas, widsize(enftype))` — all crum width dimensions must be 1-story (single non-zero mantissa digit). Confirmed for POOM: `WIDSIZEPM = 2` [wisp.h:27], both I and V widths checked.
2. `localcut.exp != ptr->cwid.dsas[index].exp` → fatal error. The knife falls within the crum's V-level.
3. `!is1story(&localcut)` → fatal error. The localcut is a simple single-level quantity.
4. `tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index])` → fatal error.

These guards ensure the cut arithmetic is unambiguous and exact.

**Step D — Compute left-fragment width `newwid`** [ndcuts.c:438-445]:

```c
movewisp(&ptr->cwid, &newwid);           // copy both V and I widths
for (i = 0; i < widsize(POOM)/*=2*/; i++) {
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify(&newwid.dsas[i]);
}
```

`widsize(POOM) = WIDSIZEPM = 2` [wisp.h:27, wisp.h:60]. `I = 0`, `V = 1` [wisp.h:19-20].

After the loop:
- `newwid.dsas[V]`: `exp` = `ptr->cwid.dsas[V].exp` (preserved from `movewisp`), `mantissa[0]` = `localcut.mantissa[0]`
- `newwid.dsas[I]`: `exp` = `ptr->cwid.dsas[I].exp` (preserved from `movewisp`), `mantissa[0]` = `localcut.mantissa[0]`

`tumblerjustify` [tumble.c:289-313] is a no-op when `mantissa[0] != 0` (returns immediately at line 296). Since `localcut.mantissa[0]` is the character-count of the left fragment and is non-zero (otherwise there's no left fragment to slice), justify does nothing.

This is the line the author himself flagged: `/* I really don't understand this loop */` [ndcuts.c:439]. The loop is correct because both V and I widths of a standard POOM text crum have the **same mantissa value** (same character count), just potentially different exponents. Writing `localcut.mantissa[0]` into both dimensions — with their existing exponents preserved — is exact.

**Step E — Compute right-fragment width** [ndcuts.c:444]:

```c
locksubtract(&ptr->cwid, &newwid, &new->cwid, widsize(enftype));
```

`locksubtract` [wisp.c:275-279] calls `tumblersub` for each dimension. For the I-dimension:
```
new->cwid.dsas[I] = ptr->cwid.dsas[I] - newwid.dsas[I]
                  = total_I_width - left_I_width
                  = right_I_width (exact)
```

`tumblersub` [tumble.c:406-440] is exact subtraction. No rounding.

**Step F — Assign left-fragment width** [ndcuts.c:445]:
```c
movewisp(&newwid, &ptr->cwid);
// ptr->cwid.dsas[I] = localcut.mantissa[0] at ptr->cwid.dsas[I].exp  (exact left I-width)
// ptr->cwid.dsas[V] = localcut.mantissa[0] at ptr->cwid.dsas[V].exp  (exact left V-width)
```

**Step G — Compute right-fragment displacement** [ndcuts.c:446]:
```c
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
// new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + ptr->cwid.dsas[I]
//                   = original_I_start + left_I_width
//                   = exact I-position of the cut (exact)
// new->cdsp.dsas[V] = original_V_start + left_V_width
//                   = cut_V (exact)
```

`dspadd` [wisp.c:15-18] calls `lockadd` [wisp.c:269-273] which calls `tumbleradd` per dimension. Exact addition, no rounding.

---

### 4. How crums are created: confirming the mantissa invariant

In `insertpm` [orglinks.c:75-133], a new POOM bottom crum is built with:

```c
movetumbler(&lstream, &crumorigin.dsas[I]);   // I-origin [line 105]
movetumbler(&lwidth,  &crumwidth.dsas[I]);    // I-width = lwidth [line 109]
movetumbler(vsaptr,   &crumorigin.dsas[V]);   // V-origin [line 113]
shift = tumblerlength(vsaptr) - 1;
inc   = tumblerintdiff(&lwidth, &zero);       // = lwidth.mantissa[0] = N chars
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = N at V's level [line 117]
```

So `crumwidth.dsas[I].mantissa[0] == crumwidth.dsas[V].mantissa[0] == N` (same character count), though their exponents may differ (`I.exp` is typically 0; `V.exp = -shift` where `shift = tumblerlength(vsaptr) - 1`).

The `slicecbcpm` loop propagates `localcut.mantissa[0]` (the character-count offset to the cut) into both dimensions, using each dimension's own preserved exponent. Because the exponents carry the level information separately, and the mantissa represents the count at that level, the split is exact in both V and I.

---

### 5. Summary

| Question | Answer |
|---|---|
| Does the right fragment's I-displacement equal exact original I-start + localcut? | **Yes** — `dspadd` at [ndcuts.c:446] |
| Does the right fragment's I-width equal exact original I-width − localcut? | **Yes** — `locksubtract` at [ndcuts.c:444] |
| Is there any rounding in `tumblerjustify`? | **No** — `tumblerjustify` is a no-op when `mantissa[0] != 0` [tumble.c:296] |
| Is there any alignment to tumbler boundaries? | **No** — all arithmetic (`tumblersub`, `tumbleradd`) is exact |
| Is this exact for arbitrary cut positions? | **Yes**, subject to preconditions: cut must be 1-story at the crum's V-level, and crum must be 1-story in all dimensions |

The surviving fragment — whether left or right — preserves the **exact I-displacement and I-width** corresponding to its surviving V-range. The implementation is purely exact tumbler arithmetic. The author's own confusion note (`/* I really don't understand this loop */` [ndcuts.c:439]) is the only rough edge: the loop is correct because the mantissa invariant (same character count in both dimensions) is established at insertion time and maintained by this exact split.
