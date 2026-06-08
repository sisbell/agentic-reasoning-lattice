## Question 12 [evidence]

> For a boundary-aligned DELETE where cut points exactly match existing crum boundaries, is `slicecbcpm` skipped entirely, and does this guarantee no zero-width POOM pieces are ever produced?

## KB Synthesis

Yes on both counts, with the guarantee being structural rather than asserted.

## Boundary-Aligned DELETE Skips `slicecbcpm`

[PRE-DELETE / Finding 0075] establishes this precisely. `makecutsbackuptohere()` in `ndcuts.c:77-90` guards the call to `slicecbcpm` with:

```
whereoncrum(blade, crum) == THRUME
```

`whereoncrum` [SS-WHEREONCRUM] returns five values: `TOMYLEFT` (−2), `ONMYLEFTBORDER` (−1), `THRUME` (0), `ONMYRIGHTBORDER` (+1), `TOMYRIGHT` (+2). Only `THRUME` — meaning `grasp < cut < reach` (both strict) — triggers `slicecbcpm`. When a cut falls exactly on a crum's grasp (`ONMYLEFTBORDER`) or reach (`ONMYRIGHTBORDER`), the guard is not satisfied and `slicecbcpm` is never called. The crum is handled whole in Phase 2 classification.

## Why This Guarantees No Zero-Width Pieces

[INV-NO-ZERO-WIDTH-CRUM / Finding 0075] derives the guarantee from the `THRUME` precondition itself. When `slicecbcpm` is invoked, the local cut offset satisfies:

- `localcut = cut − grasp`, where `grasp < cut` (strict), so `localcut > 0`  
- remaining width = `cwid − localcut`, where `cut < reach = grasp + cwid` (strict), so remaining `> 0`

Both resulting pieces have strictly positive width. The assertions at `ndcuts.c:398` and `ndcuts.c:410` would catch any violation.

Because boundary-aligned cuts never reach `slicecbcpm`, they contribute zero new pieces — the crum is simply classified and removed or left intact by Phase 2. The only pieces produced are from strictly interior cuts, and those are provably non-zero-width.

## The Proof Chain

1. `slicecbcpm` is only called when `whereoncrum == THRUME` [PRE-DELETE]
2. `THRUME` requires `grasp < cut < reach` (strict) [SS-WHEREONCRUM, SS-INTERVAL-CMP]
3. Strict interiority forces `localcut > 0` and `cwid − localcut > 0` [INV-NO-ZERO-WIDTH-CRUM]
4. Boundary-aligned cuts produce `ONMYLEFTBORDER` or `ONMYRIGHTBORDER`, so `slicecbcpm` is skipped entirely [PRE-DELETE / Finding 0075]

The guarantee is structural: the five-way classification system makes zero-width crum creation algebraically impossible, not merely empirically absent.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Boundary-Aligned DELETE: Is `slicecbcpm` Skipped, and Are Zero-Width POOM Pieces Prevented?

### Short answer

**Yes on both counts.** When all cut points are boundary-aligned, `slicecbcpm` is skipped by a hard `== THRUME` guard, and that same guard is what structurally prevents zero-width POOM pieces from being produced.

---

### Execution path for DELETE

```
fns.c:deletevspan()
  → do1.c:dodeletevspan()
      → orglinks.c:deletevspanpm()     ← zero-width input guard
          → edit.c:deletend()
              → ndcuts.c:makecutsnd()
                  → ndcuts.c:makecutsbackuptohere()   ← slicecbcpm guard lives here
```

---

### 1. The sole call site of `slicecbcpm`

`slicecbcpm` is defined once (active version: `ndcuts.c:373`) and called from exactly **one place** in the entire codebase:

```c
// ndcuts.c:77-90
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset,
                        &knives->blades[i], knives->dimension) == THRUME) {  // :79
            new = (typecuc *)createcrum(...);
            slicecbcpm(...);   // :84  ← ONLY call site
        }
    }
}
```

There is no other call. Every path to a physical crum split goes through this single `if`.

---

### 2. What `THRUME` means: the `whereoncrum` contract

`whereoncrum()` is defined at `retrie.c:345`. For POOM/SPAN nodes (`ptr->cenftype == POOM`):

```c
// retrie.c:356-372
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
cmp = tumblercmp(address, &left);
if (cmp == LESS)        return(TOMYLEFT);       // -2
else if (cmp == EQUAL)  return(ONMYLEFTBORDER); // -1   ← exact left edge
tumbleradd(&left, &ptr->cwid.dsas[index], &right);
cmp = tumblercmp(address, &right);
if (cmp == LESS)        return(THRUME);          //  0   ← strictly interior
else if (cmp == EQUAL)  return(ONMYRIGHTBORDER); // +1   ← exact right edge
else                    return(TOMYRIGHT);        // +2
```

The five-way enum is defined at `common.h:86-90`:

```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER 1
#define TOMYRIGHT       2
```

`THRUME` (= 0) is returned **only** when `left < address < right` — i.e., the address falls strictly in the interior of the crum's span. An address on either boundary returns `-1` or `+1`.

Therefore: if a cut point lands exactly on a crum's left or right edge, `whereoncrum()` returns `ONMYLEFTBORDER` or `ONMYRIGHTBORDER`, the `== THRUME` test at `ndcuts.c:79` is **false**, and `slicecbcpm` is never invoked.

---

### 3. `slicecbcpm` enforces the contract internally too

The first substantive act inside `slicecbcpm` is to re-run the same test and treat violation as a fatal error:

```c
// ndcuts.c:383-388
if (whereoncrum(ptr, offset, cut, index) != THRUME)
#ifndef DISTRIBUTION
    gerror("Why are you trying to slice me?\n");
```

This is a double-check: the outer guard (`ndcuts.c:79`) prevents the call; the inner guard (`ndcuts.c:383`) kills the process if it is ever called incorrectly. The message "Why are you trying to slice me?" is the author's explicit documentation of the invariant.

---

### 4. Why boundary-alignment prevents zero-width pieces

When `slicecbcpm` does run (strictly interior cut), it computes:

```c
// ndcuts.c:396
tumblersub(cut, &grasp.dsas[index], &localcut);
```

`localcut` is the cut's position relative to the crum's left edge. Because `THRUME` guarantees `0 < localcut < cwid`, both resulting pieces have strictly positive width:

- Left piece gets `ptr->cwid ← localcut` (> 0 by THRUME)
- Right piece gets `new->cwid ← ptr->cwid - localcut` (> 0 because `localcut < cwid`)

If the cut were on the left boundary, `localcut` would be zero → left piece would have zero width. If on the right boundary, `localcut` would equal `cwid` → right piece would have zero width. The `THRUME` guard is precisely what excludes both of those cases.

`slicecbcpm` additionally asserts `is1story(&localcut)` at `ndcuts.c:410` — the cut must be a "simple" tumbler with no secondary mantissa digits — another structural check that would fail before any bad split could propagate.

---

### 5. Upstream zero-width guard at the API boundary

Before any tree operation begins, `deletevspanpm` rejects zero-width spans outright:

```c
// orglinks.c:147-148
if (iszerotumbler(&vspanptr->width))
    return(FALSE);
```

This is a separate, earlier defense that stops degenerate operations before they ever reach `makecutsnd`.

---

### Summary of guarantees

| Layer | File:Line | Mechanism |
|---|---|---|
| API input validation | `orglinks.c:147` | Reject zero-width delete spans |
| Cut dispatch guard | `ndcuts.c:79` | `== THRUME` skips `slicecbcpm` when boundary-aligned |
| Internal contract check | `ndcuts.c:383` | `whereoncrum != THRUME` → fatal error inside slice |
| Structural arithmetic | `ndcuts.c:396,444` | THRUME guarantees `0 < localcut < cwid`, so both halves > 0 |
| Tumbler sanity | `ndcuts.c:410` | `is1story` check rejects malformed cut positions |

**Conclusion**: For a boundary-aligned DELETE, `slicecbcpm` is skipped entirely — not by convention, but by the hard equality test at `ndcuts.c:79`. The same test is what guarantees no zero-width POOM leaves are produced: `slicecbcpm` is only ever called when a cut is strictly interior, and strict interiority mathematically bounds both output widths away from zero.
