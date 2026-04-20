## Question 17 [gregory]

> Does the tumbler total order guarantee that all positions within a span `[start, start+width)` form a contiguous interval under `tumblercmp`, or can the hierarchical digit structure create positions that compare as "inside" the range but are not logically part of the span?

## KB Synthesis

## Tumbler Span Contiguity and Hierarchical Addresses

The answer is **no** — the tumbler total order does not guarantee that `[start, start+width)` contains only "logically equivalent" positions. The hierarchical digit structure does create phantom elements that compare as interior to a span.

### The Core Issue

From [SS-TUMBLER] (Findings 0001, 0031): tumblers use `.0.` boundaries to encode hierarchy — `1.1.0.2.0.1` (a document address) and `1.1.0.2.0.1.1` (its child) are distinct tumblers. The total order on tumblers is lexicographic after exponent alignment.

From [INV-TUMBLER-TOTAL-ORDER]: comparison proceeds by exponent first, then mantissa digits left-to-right. This gives the ordering:

```
1.1.0.2 < 1.1.0.2.0.1 < 1.1.0.3
```

So a span `[1.1.0.2, 1.1.0.3)` — with width computed via `tumblersub` — classifies `1.1.0.2.0.1` as `THRUME` ([SS-INTERVAL-CMP]), even though `1.1.0.2.0.1` is a document address at a deeper hierarchy level, not a position within the span's intended range.

Similarly, within V-space: a span `[1.3, 1.4)` would admit any tumbler `t` satisfying `1.3 < t < 1.4` — including `1.3.0.5` or `1.35` (fractional addresses at different precision) — all classifying as THRUME under `intervalcmp` per [SS-WHEREONCRUM].

### Why This Does Not Break the System in Practice

The system avoids phantom-element problems through two mechanisms:

**1. Allocation at uniform precision.** From [SS-ADDRESS-SPACE] (Finding 0033): sequential text inserts get contiguous I-addresses at the same precision level (`2.1.0.1.0.1.3.1`, `2.1.0.1.0.1.3.2`, etc.). From [SS-POOM-BOTTOM-CRUM] (Finding 0076): V-positions are allocated as flat 2-digit tumblers (`1.1`, `1.2`, ..., `1.10`). No V-stream content is ever placed at mixed-precision addresses like `1.3.0.5` within a subspace. This is a **convention**, not a structural enforcement.

**2. Subspace isolation via knife bounds.** From [SS-TWO-BLADE-KNIFE] (Finding 0054): INSERT at `N.x` uses second blade `(N+1).1`. The shift region `[N.x, (N+1).1)` is bounded by a whole-number subspace boundary. Any address at `(N+ε)` for fractional ε would fall inside, but since no content exists at such addresses, no POOM crums are affected. The two-blade knife exploits the hierarchical ordering without being harmed by the phantom-element property.

**3. The containment property is intentionally used.** From [SS-TUMBLER-CONTAINMENT]: the system uses prefix-truncation + equality checks (not interval comparison) for the allocation algorithm's hierarchical containment predicate. The interval classifier is used only for POOM traversal over V-positions allocated at uniform precision.

### Formal Implication for the Spec

The spec cannot state "the set of tumblers in `[start, start+width)` is exactly the intended content positions" as a consequence of the total order alone. It requires an additional **well-formedness invariant**: all V-positions within a document's POOM are allocated at a fixed precision level within their subspace. From [INV-SUBSPACE-CONVENTION]: this is a caller-enforced convention, not a storage-layer structural guarantee.

The `intervalcmp` / `whereoncrum` machinery is sound precisely because the POOM never contains entries at fractional or hierarchically deeper V-addresses within a subspace — but that soundness depends on [SS-SUBSPACE-CONVENTION] holding, not on the total order itself.

---

## Code Exploration

Now I have the complete picture. Here is the full analysis.

---

## Tumbler Total Order and Span Contiguity

### 1. The Total Order: What `tumblercmp` Actually Does

`tumblercmp` [tumble.c:72-85] delegates to `abscmp` [tumble.c:87-111] for positive tumblers. `abscmp` is a **flat lexicographic comparison** on the `(exp, mantissa[0..15])` tuple:

```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp) return(LESS);
    else return(GREATER);
}
// exps equal: compare mantissa[0], mantissa[1], ... left to right
for (i = NPLACES; i--;) {
    if(!(cmp = *a++ - *b++)) {}
    else if (cmp < 0) return(LESS);
    else return(GREATER);
}
return(EQUAL);
```
[tumble.c:92-110]

This is a genuine strict total order. Smaller `exp` (more negative) is LESS; among equal exps, mantissa is compared element by element. Zeros are **not treated specially** — `abscmp` compares all 16 mantissa digits without any zero-termination logic. This distinguishes `abscmp` sharply from `tumbleraccounteq` [tumble.c:38-70], which *does* treat consecutive zeros as a level terminator. These two functions have inconsistent models of what a tumbler means.

---

### 2. Sub-Addresses Are Dense But Legitimate

The hierarchical digit structure means there are infinitely many tumblers that sort strictly between any two adjacent top-level positions. For example, between `[exp=0, mantissa=[2,0,...]]` (= 2) and `[exp=0, mantissa=[3,0,...]]` (= 3):

```
2 < 2.1 < 2.5 < 2.5.3 < 2.9 < 3      (under abscmp, same exp=0)
```

Any `p = [exp=0, mantissa=[2, X, Y, ...]]` with any non-zero `X` or later digits satisfies `2 ≤ p < 3`. These positions compare as "inside" the span `[2, 3)`.

Are they **logically phantom**? No. In Xanadu's model, sub-addresses like 2.5 are legitimate positions within position 2's subtree. The enfilade correctly places them inside any span covering position 2. This is *by design*, not an anomaly.

---

### 3. `absadd` Is Not Standard Addition

The critical mechanism for computing `end = start + width` is `absadd` [tumble.c:444-485]. It is **not numeric addition with carries**. When `aptr->exp == bptr->exp`:

```c
ansmant[0] = amant[0] + bmant[0];   // add only first aligned digit
i = j = 1;
// ... then fill from bmant[1..NPLACES-1], DISCARDING amant[1..]
while ( j <= NPLACES -1 ) {
    ansmant[j++] = bmant[i++];   // b's suffix, not a's
}
```
[tumble.c:460-483]

**A's sub-digits after the alignment point are silently discarded.** Only the first aligned digit of `b` is added to the first aligned digit of `a`. The result's suffix comes from `b`, not `a`.

When `aptr->exp > bptr->exp` (a is "shallower"):
```c
temp = aptr->exp - bptr->exp;
while (i < temp) { ansmant[j++] = amant[i++]; }   // copy a's prefix
ansmant[j++] = amant[i++] + bmant[0];               // add at alignment point
i = 1;
// then fill from bmant[1..], discarding amant[temp+1..]
```
[tumble.c:464-471, 480-483]

Again, `a`'s tail digits beyond the addition point are lost.

---

### 4. The Level-Invariant That Keeps Spans Consistent

In `insertpm` [orglinks.c:74-134], the V-width stored in each POOM crum is computed at exactly the same hierarchical level as the V-address:

```c
shift = tumblerlength (vsaptr) - 1;              // depth of vsaptr
inc = tumblerintdiff (&lwidth, &zero);           // integer value of ispan width
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```
[orglinks.c:115-117]

`tumblerincrement(&zero, shift, inc)` places `inc` at position `shift` in a zero tumbler, yielding `[exp=-shift, mantissa=[inc, 0,...]]`. So if `vsaptr` has level-1 address (e.g., `1.3`, exp=0, mantissa=[1,3,...]), `shift=1`, and the V-width gets `exp=-1`. Then:

```
absadd([exp=0, mantissa=[1,3,...]], [exp=-1, mantissa=[inc,0,...]])
   → aptr->exp(0) > bptr->exp(-1), temp=1
   → copy amant[0]=1, then add amant[1]+bmant[0] = 3+inc
   → result: [exp=0, mantissa=[1, 3+inc, 0,...]]
```

So the span covers `[1.3, 1.(3+inc))` — exactly `inc` sub-positions at level 1. **When the level-invariant holds, span endpoints are computed correctly and the round-trip via `strongsub` works:**

`strongsub([1, 3+inc,...], [1, 3,...])` [tumble.c:548-564]:
- Both exps equal (=0); iterate prefix: mantissa[0] = 1 == 1 → --answer.exp = -1; mantissa[1] = 3+inc ≠ 3
- answer.mantissa[0] = (3+inc) - 3 = inc; suffix: zeros
- Result: `[exp=-1, mantissa=[inc,...]]` = original width ✓

---

### 5. The Pathological Case: Level-Mismatched Span Endpoints

Now, the concrete failure mode. If `start` has sub-digits but `width` is expressed at the top level — mixed levels:

**Example:** `start = 2.5` (`[exp=0, mantissa=[2,5,...]]`), `width = 3` (`[exp=0, mantissa=[3,...]]`):

```
absadd(2.5, 3):
  exps equal (both 0)
  ansmant[0] = 2 + 3 = 5       ← sub-digit .5 discarded
  rest: bmant[1...] = [0, 0,...]
  result: [exp=0, mantissa=[5, 0,...]] = 5
```

Span `[2.5, 5)` under `tumblercmp` now contains:
- `2.5` and all sub-addresses of `2.5` ✓
- `2.6, 2.7, ...` (other sub-positions of 2, after 2.5) ✓
- `3, 3.1, 3.2, ...` — **all of position 3 and its subtree**
- `4, 4.1, 4.2, ...` — **all of position 4 and its subtree**

But if the system intended "3 items starting at sub-position 2.5," the correct width should have been `[exp=-1, mantissa=[3,...]]`, giving end `2.8` and span `[2.5, 2.8)` — covering only 3 sub-positions within 2.x.

With the mismatched width, positions 3 and 4 compare as "inside" [2.5, 5) but were not intended to be part of this span. This is the "inside the range but logically outside" scenario the question asks about.

A further asymmetry: `strongsub(5, 2.5)` [tumble.c:534-565]:
- `bptr->exp(0)` is not less than `aptr->exp(0)`, so normal path
- mantissa[0]: 5 ≠ 2 → immediately: `answer.mantissa[0] = 5 - 2 = 3`
- Result: `[exp=0, mantissa=[3,...]]` = 3 ≠ original width (which might have been `[exp=-1, 3]`)

The round-trip breaks: `absadd(2.5, 3_level0) = 5`, then `strongsub(5, 2.5) = 3_level0`, which appears to reconstruct the width — but now the width is at level 0, making the span 3 top-level units, not 3 sub-units. The information about the original level is permanently lost.

The comment in `insertpm` at orglinks.c:114 — `"I'm suspicious of this shift"` — reflects genuine uncertainty from the author about whether this level-matching mechanism is always invoked correctly.

---

### 6. `strongsub`'s Silent Truncation

`strongsub` [tumble.c:544-546] has a silent failure mode when `bptr->exp < aptr->exp`:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);   // ← just return a unchanged; b is ignored
    return(0);
}
```

If you try to subtract a deep-level tumbler from a shallower one — `strongsub(5, [exp=-1, 3])` — the result is `5`, not `4` or `4+2/3`. Subtraction ignores `b` entirely if it's at a deeper level than `a`. This means level-mismatched arithmetic is silently incorrect in both directions (add and subtract).

---

### 7. Granfilade Guards Against Phantom Hits

The granfilade lookup in `fetchorglgr` [granf2.c:22-81] explicitly rejects addresses that fall inside a crum's range but don't match exactly:

```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```
[granf2.c:37-40]

This means if a query address like `1.3.5` happens to fall within a granfilade crum's range, but the crum was stored at exactly `1.3`, the lookup returns NULL. The "inside the range" property of `tumblercmp` does **not** cause false positive hits in granfilade lookups because an exact-match guard explicitly screens them out.

For text retrieval via `ispan2vstuffset` [granf2.c:286-318], range queries are intentional:
```c
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```
[granf2.c:296-297]

But I-addresses for text are always level-0 (assigned by `tumblerincrement(..., 0, length, ...)` in `inserttextgr` [granf2.c:100]), so the level-invariant holds there, and the `absadd` is safe.

---

### Summary

**The total order is genuine.** `tumblercmp` induces a strict total order on all tumblers, and for any span `[start, end)`, the set `{p : start ≤ p < end}` is a well-defined contiguous interval under this order.

**The hierarchical structure does NOT by itself create phantom inside-positions.** Sub-addresses like `2.5` or `2.5.3` that compare as inside a span containing position `2` ARE logically part of that position's sub-tree. Their presence in the interval is correct and intended.

**But `absadd` is not standard addition**, and this creates a genuine span-boundary problem when its operands are at different hierarchical levels. When `start` has sub-digits and `width` is expressed at a higher (coarser) level, `absadd` discards `start`'s sub-digits [tumble.c:460-483] and computes an `end` that is **too far forward** — extending the span to include entire top-level positions that should not be part of the span. Under `tumblercmp`, these extra positions compare as "inside" `[start, end)`, but they are not logically part of the intended span content.

The system guards against this with the `shift` calculation in `insertpm` [orglinks.c:115-117], which enforces the level-invariant for all POOM crums. When this invariant holds, every position comparing as "inside" a stored span is genuinely logically inside it. When it breaks — either via corrupted spans or user-provided spans with mismatched levels passed into `retrieverestricted` [retrie.c:56-85] — the span [start, end) will contain positions that are logically extraneous, and `tumblercmp` will classify them as inside with no error.
