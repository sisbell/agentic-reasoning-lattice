## Question 18 [gregory]

> When DELETE slices a bottom crum that maps to a contiguous I-span, does the surviving fragment preserve exact I-displacement and I-width corresponding to the surviving V-range, or is there any rounding or alignment to tumbler boundaries?

## KB Synthesis

## What the KB Tells Us

The KB gives us the V-dimension arithmetic for `slicecbcpm` precisely, but is silent on the I-dimension implementation.

**What is documented:**

[PRE-DELETE/Finding 0075] describes the cut arithmetic in V-space:
- `localcut = tumblersub(cut, grasp)` — strictly positive because the THRUME guard ensures `grasp < cut < reach`
- Original crum retains V-width = `localcut`
- New (right) crum receives V-width = `cwid - localcut` via `locksubtract`
- Both results are strictly positive; no zero-width crums can result

[INV-WIDTH-VALUE-EQUIVALENCE] establishes that V-width and I-width encode the **same integer value**, just at different tumbler precisions. This is a crum-level invariant maintained at insert time.

[INV-SINGLE-CHAR-GRANULARITY] establishes the 1:1 linear mapping: every byte occupies exactly one V-position and one I-position. A POOM bottom crum therefore represents a bijective linear mapping — a contiguous V-range maps to an equally-sized contiguous I-range.

[SS-POOM-BOTTOM-CRUM/Finding 0076] confirms crums store independent `(origin, width)` pairs for both V and I dimensions.

**The gap:**

The KB has no finding that directly documents what `slicecbcpm` (`ndcuts.c:396-444`) does to the I-dimension coordinates. Finding 0075 only describes the V-width arithmetic. There is no finding confirming that when the left fragment's V-width is set to `localcut`, the implementation also:
1. Leaves the left fragment's I-origin unchanged
2. Sets the right fragment's I-origin to `i_origin + localcut` (i.e., `tumbleradd(i_origin, localcut)`)
3. Adjusts the right fragment's I-width to `i_width - localcut`

**What can be inferred:**

Given the linear 1:1 structure, *correct* behavior requires exact I-displacement preservation — any rounding or misalignment would violate [INV-WIDTH-VALUE-EQUIVALENCE] for the resulting fragments. The tumbler arithmetic involved (`tumblersub`, `tumbleradd`) is exact for same-exponent operands [SS-TUMBLER/Finding 0031], and text content at the bottom of a POOM crum is uniformly encoded at the same exponent level. So there is no representational forcing of alignment or rounding.

However, the specific implementation of `slicecbcpm`'s I-dimension handling is not in the KB. This is an answerable question from the source code at `ndcuts.c:396-444` but **not answerable from the KB as documented.**

---

## Code Exploration

Now I have enough to give a complete, precisely cited answer. Let me trace the full execution path.

---

## Answer

**The surviving fragment preserves exact I-displacement and I-width.** No rounding or alignment to tumbler boundaries occurs — the split is character-exact. Here is the full execution trace.

---

### 1. Entry Point: `deletevspanpm` → `deletend`

`dodeletevspan` [do1.c:158-167] calls `deletevspanpm` [orglinks.c:145-152]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend` [edit.c:31-76] sets up two knives at `origin` (V) and `origin+width` (V), then calls `makecutsnd` to split any crums that straddle those positions, then iterates over children:

```c
case 1:
    disown((typecorecrum*)ptr);
    subtreefree((typecorecrum*)ptr);          // entirely inside delete range
    break;
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // index = V only
    break;
```

**Case 2 is critical**: only `cdsp.dsas[V]` is adjusted (V-displacement closes the gap). The I-displacement `cdsp.dsas[I]` of surviving crums is left untouched — correct, because I-addresses are permanent.

---

### 2. Slicing the Bottom Crum: `slicecbcpm`

When a knife lands inside a bottom POOM crum (the `THRUME` case), `makecutsbackuptohere` [ndcuts.c:69-140] calls `slicecbcpm` [ndcuts.c:373-450].

**Step 1** — compute `localcut`, the V-distance from the crum's absolute V-start to the knife:

```c
prologuend(ptr, offset, &grasp, NULL);              // grasp = absolute position of crum
tumblersub(cut, &grasp.dsas[index], &localcut);     // index = V
```
[ndcuts.c:382, 396]

**Step 2** — three guards are asserted before any arithmetic:

```c
if (!lockis1story(ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror("Not one story in POOM wid\n");           // crum's width is single-story in ALL dims
if (localcut.exp != ptr->cwid.dsas[index].exp)
    gerror("Oh well, I thought I understood this1"); // cut is at the same level as V-width
if (!is1story(&localcut))
    gerror("Oh well, I thought I understood this2"); // cut has no sub-level components
if (tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index]))
    gerror("level mismatch");                        // cut and V-width agree on depth
```
[ndcuts.c:389-436]

These collectively enforce that the V-cut is at a **character boundary** — the smallest tumbler unit stored in this crum. A V-cut that falls mid-character (sub-story address) would fail `is1story`.

**Step 3** — the split loop (the one the programmer himself commented *"I really don't understand this loop"*):

```c
movewisp(&ptr->cwid, &newwid);          // copy both I and V widths into newwid
for (i = 0; i < widsize(enftype); i++) {    // widsize(POOM) = 2 → i=0 (I), i=1 (V)
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify(&newwid.dsas[i]);
}
```
[ndcuts.c:438-442]

The result for each dimension:
- `newwid.dsas[i].exp` = `ptr->cwid.dsas[i].exp` (unchanged, from `movewisp`)
- `newwid.dsas[i].mantissa[0]` = `localcut.mantissa[0]` (the V-cut character count)
- `newwid.dsas[i].mantissa[1..]` = 0 (guaranteed by `lockis1story` guard)

**Why this is exact**: From `wisp.h:19-20`, I = index 0, V = index 1. For a POOM crum inserted via `insertpm` [orglinks.c:100-131]:

```c
movetumbler(&lwidth, &crumwidth.dsas[I]);        // I-width = character count N at I-level exp
...
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = same count N at V-level exp
```

The V-width and I-width may have **different exponents** (`V.exp = -shift = -(tumblerlength(vsaptr)-1)`, `I.exp = lwidth.exp`), but they have the **same `mantissa[0]`** — both equal to N, the character count. This is the 1:1 V↔I invariant for text content.

So when the loop sets `newwid.dsas[I].mantissa[0] = localcut.mantissa[0]` while preserving `I.exp`, it produces exactly `localcut.mantissa[0]` I-characters — the same count as the surviving V-range. The differing exponents are not a problem: each exponent encodes the hierarchical address depth of that coordinate space, and the character count is the shared mantissa[0] value.

**Step 4** — assign the new crum's I-displacement:

```c
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, widsize(POOM));
movewisp(&newwid, &ptr->cwid);
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
```
[ndcuts.c:444-446]

After these three operations:

| Fragment | I-displacement | I-width |
|---|---|---|
| **Left** (`ptr`) | original I-start (unchanged) | `localcut.mantissa[0]` at `I.exp` |
| **Right** (`new`) | original I-start + left I-width = original I-start + K | original I-width − K |

`dspadd` operates element-wise via `lockadd` [wisp.c:15-18, 269-273], adding both I and V components independently. The I-displacement of the right fragment is set to `ptr->cdsp.dsas[I] + ptr->cwid.dsas[I]` (original start plus left fragment width) — exact, no rounding.

---

### 3. The Surviving Fragment's I-coordinates After Delete

After both knife positions have been sliced, `deletend`'s loop removes the crums inside the delete range (case 1) and shifts V-displacements of crums to the right (case 2, V only). The surviving left and right fragments have:

- **I-displacement**: Set exactly by `slicecbcpm`'s `dspadd` at the blade positions. Not modified again by `deletend`.
- **I-width**: Set exactly by the `localcut.mantissa[0]` loop in `slicecbcpm`. Equals the character count of the surviving V-range.
- **No rounding**: The `is1story` and `exp`-match assertions guarantee the cut is at a clean character boundary. The tumbler arithmetic (`tumblersub`, `tumbleradd`, `locksubtract`) is exact integer subtraction with no fractional remainder for 1-story tumblers.

---

### Summary of Guarantees and Preconditions

The code enforces exactness through three assertions in `slicecbcpm` [ndcuts.c:389-436]:

1. **`lockis1story`** on all crum wids — the crum spans a single story in every dimension, so character count is fully captured in `mantissa[0]`.
2. **`localcut.exp == ptr->cwid.dsas[V].exp`** — the knife lands at the same tumbler level as the crum's V-extent.
3. **`is1story(&localcut)`** — the cut position has no sub-character components; the cut is at a whole-character boundary.

If any precondition is violated, `gerror` fires and the process aborts. Within those preconditions, **the surviving fragment preserves exact I-displacement and I-width, with no rounding or alignment whatsoever**.
