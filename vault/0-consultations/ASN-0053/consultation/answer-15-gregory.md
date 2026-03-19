## Question 15 [gregory]

> When splitting a span at an interior point, does the split always produce exactly two non-empty sub-spans whose widths sum to the original width, or can tumbler arithmetic rounding cause the parts to not reconstruct the whole?

## KB Synthesis

The KB gives a clear answer, though it comes from an implementation detail rather than an explicit arithmetic theorem.

## Split Reconstruction Is Exact by Construction

When `slicecbcpm` splits a crum at an interior cut point, the two resulting widths are computed as:

1. **Part 1:** `localcut = tumblersub(cut, grasp)` — the distance from the crum's left edge to the cut
2. **Part 2:** `cwid - localcut` via `locksubtract` — the *remainder*

This is the critical design choice. Part 2 is **not** computed independently as `tumblersub(reach, cut)`. It is computed as `original_width - part_1_width`. Mathematically:

```
part1 + part2 = localcut + (cwid - localcut) = cwid
```

This is exact and tautological — no tumbler arithmetic rounding can affect the sum because part2 is defined as the remainder from subtracting part1 from the original. [INV-NO-ZERO-WIDTH-CRUM]

## The Exponent Guard Is Not a Problem Here

The `strongsub` exponent guard (Finding 0055 in [SS-TUMBLER]) — which returns `a` unchanged when `b.exp < a.exp` — does not affect same-subspace splits. The precondition for `slicecbcpm` is `whereoncrum() == THRUME`, meaning `grasp < cut < reach` strictly. Interior points within a subspace (e.g., both at `1.x`) share the same exponent level, so the guard does not trigger. [PRE-DELETE], [SS-WHEREONCRUM]

## Strictly Positive Guarantee

The THRUME precondition also guarantees:
- `localcut = cut - grasp > 0` (cut is strictly above grasp)
- `cwid - localcut = reach - cut > 0` (cut is strictly below reach)

The assertions at `ndcuts.c:398` and `ndcuts.c:410` would catch any zero-width result. [INV-NO-ZERO-WIDTH-CRUM]

## Fixed Precision Caveat

Tumblers use a 16-digit mantissa (NPLACES=16). [SS-TUMBLER] Finding 0031. For very deep tumbler hierarchies with many significant digits, the 16-digit limit could theoretically cause truncation in `localcut`. The KB does not document any cases where this actually occurs for normal V-addresses (which use only 2–3 significant digits at text subspace positions like `1.3`). This remains an unverified edge case for pathologically long tumblers.

**Bottom line:** The split is designed to guarantee exact reconstruction by computing the second width as a remainder (`cwid - localcut`), not independently. Rounding cannot cause the parts to fail to sum to the original width — but only because the implementation avoids independent re-computation of the second part.

---

## Code Exploration

---

## Answer

The split **always produces exactly two non-empty sub-spans whose widths sum to the original** — but only because hard precondition checks in `slicecbcpm` abort the process if the preconditions for exact arithmetic are not met. There is no rounding. There is, however, a real truncation bug in `absadd` that exists for multi-story tumblers — it simply cannot be triggered by a legal span split.

---

### Where the Split Happens

The interior-point split of a bottom-level crum (height == 0) is performed by `slicecbcpm` [`ndcuts.c:373–450`], invoked from `makecutsbackuptohere` [`ndcuts.c:77–91`] when `whereoncrum` returns `THRUME` (address passes through this crum).

---

### The Tumbler Structure

From `common.h:59–65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;     /* 1 if negative, else 0 */
    short exp;         /* always <= 0; negative means leading zeros compressed */
    tdigit mantissa[NPLACES];  /* NPLACES = 16 unsigned ints */
} tumbler;
```

`iszerotumbler` is `!tumblerptr->mantissa[0]` [`common.h:72`]. A "1-story" tumbler has exactly one non-zero mantissa digit: `is1story` returns true iff `mantissa[1..15]` are all zero [`tumble.c:237–247`].

---

### What `slicecbcpm` Does

Starting at [`ndcuts.c:373`]:

**Step 1 — Validate and compute local cut position:**
```c
tumblersub(cut, &grasp.dsas[index], &localcut);  // [ndcuts.c:396]
```
`localcut` is the cut point expressed relative to the start of this crum.

**Step 2 — Hard preconditions (both abort with `gerror` if violated):**

```c
if (localcut.exp != ptr->cwid.dsas[index].exp)
    gerror("Oh well, I thought I understood this1\n");  // [ndcuts.c:403–408]

if (!is1story(&localcut))
    gerror("Oh well, I thought I understood this2\n");  // [ndcuts.c:410–430]

if (tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index]))
    gerror("level mismatch\n");                          // [ndcuts.c:431–436]
```

Additionally, the crum's own width must be 1-story — checked just before `slicecbcpm` is called:
```c
if (!lockis1story(ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror("Not one story in POOM wid\n");  // [ndcuts.c:389–394]
```

**These checks establish the invariant: both the original width and the split point are 1-story tumblers at the same `exp` level.**

**Step 3 — Construct left width:**
```c
movewisp(&ptr->cwid, &newwid);                     // [ndcuts.c:438] copy original width
for (i = 0; i < widsize(enftype); i++) {
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];  // [ndcuts.c:440]
    tumblerjustify(&newwid.dsas[i]);               // [ndcuts.c:441] no-op if [0] != 0
}
```
After this, `newwid` is 1-story with `mantissa[0] = localcut.mantissa[0]` and same `exp` as the original width (copied from `ptr->cwid`).

**Step 4 — Compute right width:**
```c
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, widsize(enftype));
// [ndcuts.c:444]
```
`locksubtract` calls `tumblersub` per dimension [`wisp.c:275–279`]. So `new->cwid = original_cwid - newwid`.

**Step 5 — Install the split:**
```c
movewisp(&newwid, &ptr->cwid);                     // [ndcuts.c:445] left part gets newwid
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype); // [ndcuts.c:446] right starts at cut
adopt(new, RIGHTBRO, ptr);                         // [ndcuts.c:448]
```

---

### Why the Arithmetic Is Exact for 1-Story Tumblers

**`tumblersub` for 1-story tumblers at equal `exp`:**

`tumblersub` [`tumble.c:406–440`] dispatches to `strongsub` via `tumbleradd(a, -b)` when neither argument is zero and they're unequal. In `strongsub` [`tumble.c:534–565`]:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) { --answer.exp; }
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // [tumble.c:556]
if (++i >= NPLACES) { movetumbler(&answer, cptr); return(0); }
for (j = 1; j < NPLACES && i < NPLACES;)
    answer.mantissa[j++] = aptr->mantissa[i++];               // [tumble.c:561–562]
```

For two 1-story tumblers at equal `exp`:
- `mantissa[0]` differs (since they're not equal), so `i = 0`, no decrement of `answer.exp`
- `answer.mantissa[0] = a.mantissa[0] - b.mantissa[0]` — exact integer difference
- `i` becomes 1, and `aptr->mantissa[1..N] = 0` (1-story), so the copy loop writes zeros

Result: `strongsub(a, b) = a.mantissa[0] - b.mantissa[0]` at the same `exp`. **Exact.**

**Reconstruction check:**

```
newwid.mantissa[0]     = localcut.mantissa[0]
new_cwid.mantissa[0]   = original.mantissa[0] - localcut.mantissa[0]
sum.mantissa[0]        = localcut.mantissa[0] + (original.mantissa[0] - localcut.mantissa[0])
                       = original.mantissa[0]  ✓
```

Both parts are 1-story at the same `exp` as the original. Their widths sum exactly to the original width.

---

### The Latent `absadd` Truncation (Does Not Apply to Span Splits)

`absadd` [`tumble.c:444–485`] is used by `tumbleradd`. In every branch, the final loop reads exclusively from `bmant`:

```c
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];   // [tumble.c:480–482]
}
```

In the equal-`exp` branch, after `ansmant[0] = amant[0] + bmant[0]`, the remaining digits `amant[1..N-1]` are **discarded** — only `bmant[1..N-1]` fills the tail. For a multi-story `a`, any sub-digits below the first level are silently lost.

This is a genuine truncation for multi-story tumblers: `absadd([2, 5, 3], [1, 0, 0]) = [3, 0, 0]`, not `[3, 5, 3]`.

However, `slicecbcpm` prevents this path via the `is1story` and `lockis1story` preconditions. All span widths entering `slicecbcpm` have `mantissa[1..N] = 0`. With only a single non-zero digit, `absadd` has nothing to truncate. The truncation bug is unreachable for any legal span split.

---

### The `strongsub` Early Return (Does Not Apply Either)

`strongsub` has a special case [`tumble.c:544–547`]:
```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr, cptr);
    return(0);
}
```

This returns `a` unchanged (as if `b = 0`) when `b` is at a coarser hierarchical level than `a`. For span splits, both widths are at the **same** `exp` level (validated at [`ndcuts.c:398–408`]), so `bptr->exp == aptr->exp` and this early return is never taken.

---

### Summary

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Split always produces exactly 2 non-empty sub-spans | **True, within preconditions** | Enforced by `slicecbcpm` structure |
| Sub-span widths sum to original | **Yes, exactly** | Integer arithmetic on 1-story tumblers |
| Tumbler arithmetic causes rounding | **No** | No fractional/floating arithmetic; only integer digit ops |
| `absadd` can truncate sub-digits | **Yes, but only for multi-story tumblers** | `ndcuts.c:480–482` drops `amant` tail |
| Multi-story tumblers can enter `slicecbcpm` | **No** | `gerror` aborts at `ndcuts.c:389–394` and `ndcuts.c:410–430` |

**The split is exact precisely because the code aborts rather than proceeding when the arithmetic would be approximate.** The preconditions (`is1story`, matching `exp`, matching `tumblerlength`) are not defensive programming — they are load-bearing constraints on a number system that does not support general multi-story subtraction. If a cut point cannot be expressed as a 1-story tumbler at the same level as the span width, the backend crashes rather than producing a split that does not reconstruct.
