## Question 12 [gregory]

> When `slicecbcpm` cuts a bottom crum at an interior point (THRUME case), how are the two resulting crums' I-displacements computed — does the second piece's I-displacement advance by exactly the V-offset of the cut within the original span?

## KB Synthesis

The KB does not directly document the I-displacement computation inside `slicecbcpm`. Here is what is known, and where the gap lies.

**What the KB documents about the cut:**

[INV-NO-ZERO-WIDTH-CRUM] covers `slicecbcpm` at `ndcuts.c:396-444` and establishes:
- `localcut = tumblersub(cut, &grasp, &localcut)` — this is the V-offset of the cut point within the original crum (strictly positive, since THRUME is required)
- The original crum retains V-width `localcut`
- The new crum receives V-width `locksubtract(cwid, localcut)` — the remainder

**What the KB documents about crum structure:**

[SS-POOM-BOTTOM-CRUM] establishes that each bottom crum holds dual-space coordinates:
```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

[INV-WIDTH-VALUE-EQUIVALENCE] establishes that `tumblerintdiff(crum.width.dsas[V], zero) == tumblerintdiff(crum.width.dsas[I], zero)` — both widths encode the same integer, just at different tumbler precisions.

**The inference the KB supports, but does not confirm:**

Since each bottom crum is a 1:1 linear mapping from a contiguous V-range to a contiguous I-range ([INV-POOM-BIJECTIVITY], [INV-SINGLE-CHAR-GRANULARITY]), and since V-widths and I-widths encode the same integer values, cutting at V-offset `localcut` should advance the second crum's I-origin by the same integer count. But no finding explicitly documents the `slicecbcpm` formula for the second crum's `dsas[I]` origin computation, and the code at `ndcuts.c:396-444` is not directly traced in any finding.

**Answer:** Not fully answerable from the KB. The V-side of the cut is documented — `localcut = cut - grasp`, first crum retains V-width `localcut`, second receives the remainder. The I-side advance is not directly stated in any finding. Based on [INV-WIDTH-VALUE-EQUIVALENCE] and the bijective structure of POOM crums [INV-POOM-BIJECTIVITY], the second crum's I-origin should advance by the same integer as `localcut`, but this would require reading `ndcuts.c:396-444` directly to confirm.

---

## Code Exploration

Now I have all the pieces. Let me write the full answer.

---

## How `slicecbcpm` Computes I-Displacements for the Two Resulting Crums

### Entry conditions and calling context

`slicecbcpm` is called from `makecutsbackuptohere` [ndcuts.c:84] when `whereoncrum` returns `THRUME` (the cut falls strictly inside the crum's span):

```c
// ndcuts.c:79-84
if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
    new = (typecuc *)createcrum((INT)ptr->height,(INT)ptr->cenftype);
    ...
    slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

The `dimension` field of `typeknives` is documented as *"always V, assigned by rearrange2d"* [ndenf.h:15], so `index = V = 1` for POOM.

---

### Step 1 — Compute `grasp`: absolute V-position of the crum's left edge [ndcuts.c:382]

```c
prologuend(ptr, offset, &grasp, NULL);
```

`prologuend` [retrie.c:334–338]:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    ...
}
```
`dspadd` calls `lockadd` over all `dspsize(POOM) = 2` components [wisp.c:15–17], so:
- `grasp.dsas[I] = offset.dsas[I] + ptr->cdsp.dsas[I]`
- `grasp.dsas[V] = offset.dsas[V] + ptr->cdsp.dsas[V]`

---

### Step 2 — `localcut`: V-offset of the cut within the crum [ndcuts.c:396]

```c
tumblersub(cut, &grasp.dsas[index], &localcut);
```

This subtracts the crum's absolute V-left-edge from the knife position:

```
localcut = cut − grasp.dsas[V]
         = cut − (offset.dsas[V] + ptr->cdsp.dsas[V])
```

`localcut` is the V-distance from the crum's own left edge to the cut point. Two sanity guards enforce its structure:
- **Line 398**: `localcut.exp` must equal `ptr->cwid.dsas[V].exp` — the cut is at the same tumbler level as the crum's V-width
- **Lines 410–430**: `is1story(&localcut)` must hold — only `mantissa[0]` is non-zero

---

### Step 3 — The wid split loop [ndcuts.c:438–445]

This is where both resulting widths and the I-displacement of the second piece are determined. The code author flagged it honestly:

```c
// ndcuts.c:438-445
movewisp(&ptr->cwid, &newwid);                        // newwid ← copy of ptr->cwid
for (i = 0; i < widsize(enftype); i++) {              // i ∈ {I=0, V=1} for POOM
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0]; // overwrite mantissa[0] only
    tumblerjustify(&newwid.dsas[i]);
}
locksubtract(&ptr->cwid, &newwid, &new->cwid, widsize(enftype)); // new->cwid = original−newwid
movewisp(&newwid, &ptr->cwid);                        // first piece gets newwid
```

**What the loop does per dimension:**

After `movewisp`, `newwid.dsas[i]` is a complete copy of `ptr->cwid.dsas[i]`, including its `exp` field. The loop then *only replaces* `mantissa[0]` with `localcut.mantissa[0]` — the `exp` of each dimension is left untouched.

For `i = V`: Since the assertion at line 398 guarantees `localcut.exp == ptr->cwid.dsas[V].exp`, the result is that `newwid.dsas[V] == localcut` as a tumbler value — the first piece gets exactly the V-distance to the cut as its V-width.

For `i = I`: `newwid.dsas[I]` gets `exp = ptr->cwid.dsas[I].exp` (the I-space exponent) but `mantissa[0] = localcut.mantissa[0]` (the V-cut count). **The I and V exponents are in general different**, because I-space and V-space live at different depths of the tumbler hierarchy.

This is visible from `insertpm` [orglinks.c:105–117], which is how POOM crums are created:

```c
movetumbler(&lwidth, &crumwidth.dsas[I]);              // I-wid = lwidth (at I-space exp)
shift = tumblerlength(vsaptr) - 1;
inc   = tumblerintdiff(&lwidth, &zero);                // inc = lwidth.mantissa[0]
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]); // V-wid: inc at V-space level
```

The I-wid is stored at `lwidth.exp` (an I-sequence address exponent); the V-wid is stored at `shift = tumblerlength(vsaptr) − 1` (a V-document exponent). These are the same **count** (`inc`) but at different tumbler levels.

The diagnostic function `widdiffs` [insertnd.c:114–122] confirms the invariant: `lastdigit[I] == lastdigit[V]`, i.e., `ptr->cwid.dsas[I].mantissa[0] == ptr->cwid.dsas[V].mantissa[0]`.

---

### Step 4 — `new->cdsp` for the second piece [ndcuts.c:446]

```c
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
```

At this point `ptr->cwid` has been updated to `newwid`. `dspadd` calls `lockadd` over both components:

```
new->cdsp.dsas[V] = ptr->cdsp.dsas[V] + newwid.dsas[V]
                  = ptr->cdsp.dsas[V] + localcut
                  = ptr->cdsp.dsas[V] + (cut − offset.dsas[V] − ptr->cdsp.dsas[V])
                  = cut − offset.dsas[V]

new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + newwid.dsas[I]
```

Where `newwid.dsas[I]` has:
- `mantissa[0] = localcut.mantissa[0]`   ← the V-cut's scalar count
- `exp         = ptr->cwid.dsas[I].exp`  ← the I-space exponent, NOT the V-space exponent

---

### Direct answer to the question

**The second piece's I-displacement does advance by `localcut.mantissa[0]` — the scalar count of the V-offset — but expressed in I-space coordinates, not in V-space coordinates.**

Numerically as a tumbler:
```
newwid.dsas[I] value = localcut.mantissa[0] × base^(ptr->cwid.dsas[I].exp)
localcut       value = localcut.mantissa[0] × base^(ptr->cwid.dsas[V].exp)
```

These are identical tumblers only if `ptr->cwid.dsas[I].exp == ptr->cwid.dsas[V].exp`. In practice, I-space and V-space live at different tumbler depths (I-space is sequential content addressing; V-space is document version addressing), so the two exponents differ and the I-displacement advance is **not the same tumbler** as the V-offset of the cut.

What the loop actually does — and this is what the comment `/* I really don't understand this loop */` [ndcuts.c:439] confesses to — is apply the same **scalar count** (`localcut.mantissa[0]`) to every dimension of the wid, using each dimension's pre-existing exponent as its scale. This correctly partitions the crum in all dimensions simultaneously while preserving the POOM invariant (`widdiffs == 0`): the count of I-units in each resulting piece equals the count of V-units.

In short: the I-displacement of the second piece advances by **the same count of atomic units** as the V-offset of the cut, but scaled by I-space's exponent rather than V-space's exponent. It is proportionally correct, not numerically identical to the V-offset tumbler.
