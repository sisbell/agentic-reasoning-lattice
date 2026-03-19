## Question 11 [gregory]

> When a POOM entry is split by INSERT (e.g., inserting into the middle of "ABCDE"), does the split produce two new bottom crums whose I-displacements and I-widths exactly partition the original I-span with no gaps or overlaps?

## KB Synthesis

## POOM Crum Splitting: V and I Dimensions

The KB directly addresses this, though from multiple angles that need combining.

### What the KB Confirms

**The V-dimension split is exact by construction.**

[INV-NO-ZERO-WIDTH-CRUM] (Finding 0075) describes `slicecbcpm` directly: when a cut falls strictly interior to a crum (`THRUME`), it computes:
- `localcut = tumblersub(cut, &grasp)` — the cut offset from the grasp
- Original crum retains width `localcut` (strictly positive)
- New crum receives `cwid - localcut` via `locksubtract` (also strictly positive)

These two widths sum to exactly `cwid` — no gap, no overlap in V-space.

**The I-width encodes the same count as the V-width.**

[INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076) states: `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` for every POOM bottom crum. The V and I widths are different tumbler representations of the same integer count.

**A crum is a contiguous bijective mapping.**

[INV-POOM-BIJECTIVITY] establishes the POOM is designed as a bijection from V-addresses to I-addresses. Within a single crum, [SS-POOM-BOTTOM-CRUM] (Finding 0076) shows each crum holds `origin` and `width` in both V and I dimensions, covering a single contiguous block in each. [INV-WIDTH-VALUE-EQUIVALENCE] confirms the two dimensions span the same count.

### The Inference

Given these three facts together: if V and I widths are always numerically equal within a crum, and the V-split produces `(localcut, cwid - localcut)`, then the I-split must produce `(localcut, cwid - localcut)` in the same numeric values — otherwise the crum's V-width and I-width would diverge, violating [INV-WIDTH-VALUE-EQUIVALENCE] on the resulting crums.

The resulting partition is:
- **Left crum**: I-origin = original I-origin, I-width = `localcut`
- **Right crum**: I-origin = original I-origin + `localcut`, I-width = `cwid - localcut`

Together they span `[I_origin, I_origin + cwid)` with no gaps or overlaps — exactly partitioning the original I-span.

### Caveat

The KB does not contain a finding that directly inspects `slicecbcpm`'s I-dimension handling (the code at `ndcuts.c:396-444`). The conclusion is a necessary consequence of [INV-WIDTH-VALUE-EQUIVALENCE] holding on both result crums, not a direct code observation. If `slicecbcpm` somehow applied different arithmetic to the I-origin of the new crum, that invariant would be violated.

**Short answer**: Yes — the I-span is exactly partitioned with no gaps or overlaps. The split must be `(localcut, cwid - localcut)` in both dimensions to preserve [INV-WIDTH-VALUE-EQUIVALENCE] on the resulting crums, and [INV-NO-ZERO-WIDTH-CRUM] guarantees both parts are positive.

---

## Code Exploration

I now have everything needed. Here is my full answer.

---

## Does INSERT Splitting Exactly Partition the Original I-Span?

**Short answer: Yes, exactly — no gaps, no overlaps.** The guarantee is structural and provable directly from `slicecbcpm` in `backend/ndcuts.c`.

---

## Call Path from INSERT to Slice

**`doinsert`** (`do1.c:87`) calls `inserttextingranf` to allocate fresh I-space for the new content, then calls `docopy` → `insertpm`. For the POOM, the relevant path is:

**`insertnd`** (`insertnd.c:15`) — POOM case at line 53–61:
```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);   // [insertnd.c:54]
    setwispupwards(fullcrumptr,0);
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

**`makegappm`** (`insertnd.c:124`) sets up two knife positions:
```c
movetumbler (&origin->dsas[V], &knives.blades[0]);                          // [insertnd.c:144]
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);         // [insertnd.c:145]
knives.nblades = 2;
knives.dimension = V;
makecutsnd (fullcrumptr, &knives);                                           // [insertnd.c:148]
```

Knife[0] is the insertion V-address. Knife[1] is "just after" it — computed so the insertion point is isolated as a degenerate slice. `makecutsnd` descends and calls **`slicecbcpm`** on any bottom crum that straddles knife[0].

---

## `slicecbcpm`: The Actual Split (`ndcuts.c:373–450`)

This is the function that does the work. I trace each step for "ABCDE" (original crum: V-span `[1, 6)`, I-span `[I₀, I₀+5)`, width W=5) being cut at V=3 (localcut = 2):

### Step 1 — Assert 1-story invariant (`ndcuts.c:389–394`)
```c
if (!lockis1story (ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror ("Not one story in POOM wid\n");
```
`lockis1story` (`wisp.c:298–304`) requires that every tumbler in the wid array has no second mantissa digit (`mantissa[1..] == 0`). For POOM, `widsize` = 2 (both V and I). This asserts `V_width == I_width` as a precondition. **Fatal error if violated.** For our example, both are W=5. ✓

### Step 2 — Compute the V-offset of the cut within this crum (`ndcuts.c:396`)
```c
tumblersub (cut, &grasp.dsas[index], &localcut);
```
`localcut = V_cut - V_crum_start` = 3 − 1 = **2**.

`is1story(&localcut)` is also checked (`ndcuts.c:410`); for integer offsets it must hold.

### Step 3 — Set both dimensions' widths of the left piece (`ndcuts.c:438–445`)
```c
movewisp (&ptr->cwid, &newwid);          // newwid = {V:5, I:5}  (original)
for (i = 0; i < widsize(enftype); i++) { // i = 0 (V), i = 1 (I)
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];   // both set to 2
    tumblerjustify (&newwid.dsas[i]);
}
// After loop: newwid = {V:2, I:2}
```
`tumblerjustify` (`tumble.c:289`) normalizes the mantissa (shifts leading zeros, adjusts exp). For our integer 2, this is a no-op. The loop uniformly assigns `localcut.mantissa[0]` to **every** dimension — both V and I get the same value.

### Step 4 — Right-piece width = original − left (`ndcuts.c:444`)
```c
locksubtract ((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, widsize);
// = {V:5, I:5} − {V:2, I:2} = {V:3, I:3}
```
`locksubtract` (`wisp.c:275–279`) iterates `loxize` times (= `widsize` = 2), calling `tumblersub(lock1++, lock2++, lock3++)` — once for V, once for I. `tumblersub` (`tumble.c:406`) is exact subtraction, no rounding. Result: `new->cwid = {V:3, I:3}`.

### Step 5 — Left piece takes its new width (`ndcuts.c:445`)
```c
movewisp (&newwid, &ptr->cwid);          // ptr->cwid = {V:2, I:2}
```

### Step 6 — Right piece displacement = left start + left width (`ndcuts.c:446`)
```c
dspadd (&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
// new->cdsp = {V:1, I:I₀} + {V:2, I:2} = {V:3, I:I₀+2}
```
`dspadd` (`wisp.c:15–18`) calls `lockadd` which calls `tumbleradd` for each of `dspsize(POOM)` = 2 dimensions. Applied uniformly to V and I simultaneously.

---

## Mathematical Proof of Exact Partition

After the slice, the two bottom crums are:

| | V-start | V-width | I-start | I-width |
|---|---|---|---|---|
| **Left** (ptr) | V₀ = 1 | 2 | I₀ | 2 |
| **Right** (new) | 3 | 3 | I₀ + 2 | 3 |

**No gap**: `right.I_start = left.I_start + left.I_width = I₀ + 2`. Follows directly from `dspadd` at `ndcuts.c:446`, applied to I-dimension.

**No overlap**: left covers `[I₀, I₀+2)`, right covers `[I₀+2, I₀+5)`. They share only the boundary point.

**Complete coverage**: `left.I_width + right.I_width = 2 + 3 = 5 = W_original`. Follows from `locksubtract` at `ndcuts.c:444`: `new_width = original_width − left_width`, so `left + new = original` by construction.

The same arithmetic applies in all dimensions simultaneously because `locksubtract` and `lockadd` both iterate over all `widsize` (= 2 for POOM) dimensions.

---

## What Happens to I-Displacements After the Gap-Make

Back in `makegappm` (`insertnd.c:151–168`), after `makecutsnd`, each son is classified by `insertcutsectionnd`:

- **Case 0** (to the left of the insertion point): no change.
- **Case 1** (the right half of the split, between knife[0] and knife[1]): only **V-displacement** is shifted:
  ```c
  case 1:
      tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);  // [insertnd.c:162]
  ```
  The **I-displacement is not touched**. "CDE" stays at `I₀+2` forever; only its V-address shifts to make room for the new text.

- **Case 2** (already past the cut): no change.

The I-addresses of the two halves are immutable after the split. The newly inserted text gets a separately allocated I-span from `inserttextingranf` (`do1.c:118`) — it does not fill any gap between the halves because there is no gap.

---

## Summary

Yes — **the split is an exact partition of the original I-span, with no gaps or overlaps**, guaranteed by the mechanics of `slicecbcpm`:

1. **Precondition** (`ndcuts.c:389`): The 1-story invariant asserts `V_width == I_width`, so a V-offset uniquely determines an I-offset of equal magnitude. Fatal error if violated.
2. **Left-piece widths** (`ndcuts.c:439–441`): The loop over `widsize` sets `mantissa[0]` to `localcut.mantissa[0]` in **every dimension** — V and I receive the identical value.
3. **Right-piece widths** (`ndcuts.c:444`): `locksubtract` subtracts element-wise across all dimensions: `right_width[i] = original_width[i] − localcut` for each i.
4. **Right-piece position** (`ndcuts.c:446`): `dspadd` adds element-wise across all dimensions: `right_start[i] = left_start[i] + left_width[i]` for each i.

The result is algebraically exact: `left.I_width + right.I_width = W`, and `right.I_start = left.I_start + left.I_width`, proven by the subtraction law (`locksubtract`) and the addition law (`dspadd`) that define the construction.
