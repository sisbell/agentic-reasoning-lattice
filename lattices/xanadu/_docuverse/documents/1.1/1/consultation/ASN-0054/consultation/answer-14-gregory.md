## Question 14 [gregory]

> Does `slicecbcpm` always produce exactly two pieces when cutting a bottom crum at an interior point, and are both pieces guaranteed to have positive widths, or can degenerate zero-width fragments survive?

## KB Synthesis

Yes on both counts. The KB gives a complete answer.

**`slicecbcpm` produces exactly two pieces**

When called, `slicecbcpm` splits one bottom crum into two: the original crum retains width `localcut`, and a new sibling crum receives the remainder `cwid - localcut`. There is no code path that produces more or fewer fragments from a single call [INV-NO-ZERO-WIDTH-CRUM].

**Both pieces are guaranteed to have strictly positive widths**

The guarantee comes from the call-site precondition, not from `slicecbcpm` itself. `makecutsbackuptohere()` (`ndcuts.c:77-90`) only invokes `slicecbcpm` when `whereoncrum() == THRUME`, meaning the cut satisfies `grasp < cut < reach` with **strict** inequalities on both sides [PRE-DELETE, Finding 0075].

Given strict interiority:

- `localcut = cut - grasp > 0` (because `cut > grasp`)
- `remaining = cwid - localcut = reach - cut > 0` (because `cut < reach`)

Both strict inequalities are mathematical consequences of the THRUME precondition. The assertions at `ndcuts.c:398` and `ndcuts.c:410` would catch any violation if somehow reached, but they cannot be reached through the normal call path [INV-NO-ZERO-WIDTH-CRUM].

**What happens at crum boundaries**

When a delete boundary aligns exactly with a crum's grasp (`whereoncrum == ONMYLEFTBORDER`) or reach (`whereoncrum == ONMYRIGHTBORDER`), `slicecbcpm` is **not called at all** — the crum is handled whole in Phase 2 classification [PRE-DELETE, Finding 0075]. Boundary alignment produces zero fragments from `slicecbcpm`, not zero-width fragments.

**Formal invariant**

`∀ crum ∈ bottom_crums(enf) : crum.width > 0` — no DELETE Phase 1 cutting operation can produce a degenerate zero-width crum [INV-NO-ZERO-WIDTH-CRUM]. This is enforced structurally by the guard in `makecutsbackuptohere`, making it a caller-enforced precondition on `slicecbcpm` rather than an internal check within `slicecbcpm` itself.

---

## Code Exploration

Now I have enough to give a thorough, cited answer.

---

## `slicecbcpm`: Two Pieces, Zero-Width Analysis

### Does it always produce exactly two pieces?

**Yes, unconditionally.** The function creates the left piece in-place (`ptr`, narrowed) and creates exactly one right piece (`new`), then links it into the tree with a single `adopt(new, RIGHTBRO, ptr)` call [`backend/ndcuts.c:448`]. There is no branching that could produce one piece or three — the split is structurally hardwired to two.

---

### Are both pieces guaranteed to have positive widths?

#### The Cut Dimension (`index`)

**Yes, for the cut dimension.** The chain of reasoning is tight:

**Step 1 — THRUME means strictly interior.**

`whereoncrum` [`backend/retrie.c:345-398`] computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
// left = offset[index] + cdsp[index]  (crum's absolute start)

tumbleradd(&left, &ptr->cwid.dsas[index], &right);
// right = left + cwid[index]          (crum's absolute end)

// Returns THRUME only when:  left < address < right  (strictly)
```

THRUME is returned only when `address > left && address < right` — both boundary values are excluded. If cut is at the left boundary, `whereoncrum` returns `ONMYLEFTBORDER`; at the right, `ONMYRIGHTBORDER`. Guard 1 [`ndcuts.c:383-388`] aborts with `gerror()` unless the result is exactly `THRUME`.

**Step 2 — `localcut` is therefore strictly positive and strictly less than the crum's width.**

```c
tumblersub(cut, &grasp.dsas[index], &localcut);
// localcut = cut - left
```
[`ndcuts.c:396`]

Since `left < cut < right = left + cwid[index]`, we get `0 < localcut < cwid[index]`.

**Step 3 — The width arithmetic cannot zero out either piece.**

```c
movewisp(&ptr->cwid, &newwid);                          // copy original width
for (i = 0; i < widsize(enftype); i++) {
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0]; // set lowest digit
    tumblerjustify(&newwid.dsas[i]);                    // normalize
}                                                        // [ndcuts.c:438-442]
```

`localcut` is 1-story (enforced by Guard 4, [`ndcuts.c:410-430`]), meaning it has only `mantissa[0]` nonzero. Since `localcut > 0`, `localcut.mantissa[0] != 0`. `tumblerjustify` [`tumble.c:289-313`] returns immediately when `mantissa[0] != 0` — it only shifts leading zeros — so `newwid.dsas[index]` = localcut, which is strictly positive.

```c
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid,
             (tumbler*)&new->cwid, (unsigned)widsize(enftype));
// new->cwid = ptr->cwid - newwid = cwid - localcut > 0

movewisp(&newwid, &ptr->cwid);
// ptr->cwid = newwid = localcut > 0
```
[`ndcuts.c:444-445`]

Both pieces have strictly positive width in dimension `index`.

---

#### The Non-Cut Dimensions (i ≠ index)

**This is where a latent gap exists.**

The loop at [`ndcuts.c:439-442`] sets `newwid.dsas[i].mantissa[0] = localcut.mantissa[0]` for **every dimension** `i`, not just the cut dimension. The comment at line 439 reads:

```c
for (i = 0; i < widsize(enftype); i++) {/* I really don't understand this loop */
```

For a 2D POOM (widsize = 2, dimensions I and V), both `newwid.dsas[0]` and `newwid.dsas[1]` get set to `localcut.mantissa[0]`. Then `new->cwid[i] = ptr->cwid[i] - localcut.mantissa[0]` for all i via `locksubtract`.

For the non-cut dimension, **nothing in the function explicitly prevents** `ptr->cwid[non-index] == localcut.mantissa[0]`, which would produce `new->cwid[non-index] == 0` via `tumblersub`'s `tumblerclear(cptr)` branch [`tumble.c:416-417`]:

```c
else if (tumblereq(aptr, bptr))
    tumblerclear(cptr);   // zero result — no guard here
```

The function's correctness in non-cut dimensions relies on an **implicit POOM structural invariant**: that all width dimensions are equal (or at least that the I-width is always ≥ the V-width at the cut). This invariant is enforced upstream by the enfilade construction, not within `slicecbcpm` itself.

---

### The Five Guards — What They Actually Protect

| Guard | Location | What it prevents |
|-------|----------|-----------------|
| `whereoncrum != THRUME` | `ndcuts.c:383` | Cut at or outside boundary → prevents zero-width in cut dimension |
| `!lockis1story(ptr->cwid)` | `ndcuts.c:389` | Multi-story widths (complex hierarchical values) |
| `localcut.exp != ptr->cwid.dsas[index].exp` | `ndcuts.c:398` | Exponent mismatch at wrong hierarchy level |
| `!is1story(&localcut)` | `ndcuts.c:410` | Multi-story cut value |
| `tumblerlength(cut) != tumblerlength(cwid)` | `ndcuts.c:431` | Level (precision) mismatch |

None of these guards explicitly check that `ptr->cwid[i] > localcut.mantissa[0]` for dimensions `i ≠ index`.

---

### Conclusion

`slicecbcpm` **always produces exactly two pieces**. For the cut dimension, **both pieces are guaranteed to have strictly positive widths**, enforced by the THRUME precondition (which establishes `0 < localcut < cwid[index]`) combined with the 1-story constraint (which ensures the width arithmetic operates on single-digit values without underflow ambiguity).

For non-cut dimensions, zero-width fragments **are theoretically possible** if the per-dimension width happens to equal `localcut.mantissa[0]`. The code relies on a POOM structural invariant — never locally checked — that all dimensions' widths are consistent relative to the cut. The author's own comment ("I really don't understand this loop") at [`ndcuts.c:439`] acknowledges the multi-dimensional behavior was not fully reasoned through at the time of writing.
