## Question 13 [gregory]

> Are `tumbleradd` and `tumblersub` inverses of each other for all representable tumblers, i.e., does `tumbleradd(tumblersub(a, b), b)` always recover `a` exactly, or are there precision-loss cases from the fixed mantissa?

## KB Synthesis

## `tumbleradd`/`tumblersub` as Inverses

**Short answer: No, they are not inverses in general.** The KB documents at least one case where the round-trip `tumbleradd(tumblersub(a, b), b) ≠ a`, and the fixed 16-digit mantissa creates a second potential failure mode.

---

### Case 1: The `strongsub` Exponent Guard (documented)

[SS-TUMBLER] Finding 0055 documents a definitive counterexample. `strongsub` — the implementation backing `tumblersub` — has an exponent guard:

> when the subtrahend's exponent is strictly less than the minuend's exponent, `strongsub` returns the minuend unchanged

So when `b.exp < a.exp`:

```
tumblersub(a, b) = strongsub(a, b) = a   (no-op, not a - b)
tumbleradd(a, b) = a + b  ≠  a
```

The round-trip `tumbleradd(tumblersub(a, b), b)` yields `a + b`, not `a`. Finding 0055 gives a concrete example:

```
strongsub(a={exp=0, mant=[2,1]}, b={exp=-1, mant=[3]}):
  b.exp (-1) < a.exp (0) → TRUE
  Returns a unchanged: {exp=0, mant=[2,1]} = tumbler 2.1
```

This is not a bug in the finding's framing — it's a **deliberate architectural property** that prevents cross-subspace POOM shifts during DELETE ([FC-SUBSPACE], Finding 0055, Finding 0067). But it means subtraction is a partial function, not an invertible one.

---

### Case 2: Fixed-Precision Mantissa Overflow (structural)

[SS-TUMBLER] Finding 0031 establishes:

> A tumbler is stored as a sign bit, a short exponent, and a fixed-length mantissa of `NPLACES` (16) digits.

With only 16 mantissa digits, `tumbleradd` on two tumblers whose sum would require 17+ significant digits must truncate or overflow. The KB doesn't document the exact carry-overflow behavior, but the fixed-width representation makes precision loss structurally possible for sufficiently large or fine-grained tumblers. Since `tumblersub` reduces the magnitude and `tumbleradd` restores it, any truncation introduced during subtraction would propagate — if `c = a - b` loses low-order digits, `c + b` recovers something in the right range but not necessarily `a` exactly.

---

### When the Round-Trip Does Hold

For same-exponent subtraction without mantissa overflow — i.e., when both operands are positive, share the same exponent, and the result fits in 16 digits — the sign-magnitude arithmetic should recover exactly. [SS-TUMBLER] Finding 0053 confirms subtraction is implemented as sign negation plus addition, so same-exponent cases with `a ≥ b ≥ 0` should satisfy `(a - b) + b = a` within precision bounds.

---

### Spec Implications

This matters for [PRE-DELETE] and [FC-SUBSPACE]: the `strongsub` no-op is the mechanism that prevents DELETE from shifting link crums into negative territory across subspace boundaries ([INT-DELETE-SUBSPACE-ASYMMETRY]). It is an **intentional non-inverse** that the spec must capture as a conditional postcondition: `tumblersub(a, b) = a - b` only when `b.exp ≥ a.exp`; otherwise `tumblersub(a, b) = a`.

---

## Code Exploration

I now have everything needed. Here is the full analysis:

---

## Are `tumbleradd` and `tumblersub` inverses?

**No. `tumbleradd(tumblersub(a, b), b)` does not in general recover `a`.** There are multiple distinct failure modes, each traceable to specific code paths in `tumble.c`. None of them involve carry/borrow — because the arithmetic has no carry at all.

---

### The Representation

`tdigit = UINT` (32-bit unsigned), `NPLACES = 16` [`common.h:53,57`].

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;   /* 1 if negative */
    short exp;       /* always ≤ 0 for valid tumblers */
    tdigit mantissa[NPLACES];
} tumbler;
```
[`common.h:59–65`]

`tumblercheckptr` enforces `exp > 0` as invalid [`tumble.c:174–179`]. After `tumblerjustify`, the first non-zero digit is always at `mantissa[0]`, and `exp` counts how many leading zeros were shifted away (hence always ≤ 0). An address like `0.0.5.3` becomes `{exp=-2, mantissa=[5,3,0,...]}`.

There is **no carry between levels**. Each `mantissa[k]` is an independent integer representing one level of the Xanadu address hierarchy. Zeros in the mantissa are semantically significant separators.

---

### `tumblersub` dispatch

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr) {
    if (iszerotumbler(bptr))        movetumbler(aptr, cptr);
    else if (tumblereq(aptr, bptr)) tumblerclear(cptr);
    else if (iszerotumbler(aptr))   { movetumbler(bptr, cptr); cptr->sign = !cptr->sign; }
    else {
        movetumbler(bptr, &temp);
        temp.sign = !temp.sign;
        tumbleradd(aptr, &temp, cptr);   /* a + (-b) */
    }
    tumblerjustify(cptr);
}
```
[`tumble.c:406–440`]

In the general case it negates b and calls `tumbleradd(a, -b, c)`. Since the signs differ, `functiontumbleradd` dispatches based on `abscmp`:

- `|a| > |b|` → `strongsub(a, b, c)`, sign = a's sign  
- `|b| ≥ |a|` → `weaksub(b, a, c)`, sign = b's sign

[`tumble.c:384–396`]

---

### Failure Mode 1 — `strongsub` early return, then `absadd` corrupts the result

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr) {
    tumblerclear(&answer);
    if (tumblereq(aptr, bptr)) { movetumbler(&answer, cptr); return 0; }
    if (bptr->exp < aptr->exp) {            /* ← EARLY RETURN */
        movetumbler(aptr, cptr);
        return 0;
    }
    /* ... skip equal prefix, subtract at first differing digit ... */
}
```
[`tumble.c:534–565`]

When `b.exp < a.exp` (b is deeper in the hierarchy than a), `strongsub` immediately returns `a` unchanged. So `d = tumblersub(a, b) = a`.

Now `tumbleradd(d, b) = tumbleradd(a, b)` where both are positive and `a.exp > b.exp`. This hits the `aptr->exp > bptr->exp` branch of `absadd`:

```c
} else if (aptr->exp > bptr->exp) {
    answer.exp = aptr->exp;
    temp = aptr->exp - bptr->exp;          /* positive */
    while (i < temp) {
        ansmant[j++] = amant[i++];         /* copy a's prefix */
    }
    ansmant[j++] = amant[i++] + bmant[0]; /* add b's first digit into a */
    i = 1;
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];            /* fill from b's suffix */
}
```
[`tumble.c:464–484`]

**Concrete counterexample:**

- `a = {exp=0, mantissa=[1,2,3,0,...]}` — address `1.2.3`
- `b = {exp=-2, mantissa=[5,0,...]}` — address `0.0.5` (two levels deep)

`tumblersub(a, b)`: `abscmp` sees `a.exp(0) > b.exp(-2)` → GREATER → `strongsub` → `b.exp(-2) < a.exp(0)` → returns `a` unchanged. `d = {exp=0, [1,2,3,0,...]}`.

`tumbleradd(d, b)`: same sign, `absadd(d, b)` with `d.exp(0) > b.exp(-2)`, `temp=2`:  
- copies `d[0]=1, d[1]=2` into `answer[0,1]`  
- `answer[2] = d[2] + b[0] = 3 + 5 = 8`  
- fills from `b[1], b[2], ...` (all zero)

**Result: `{exp=0, [1,2,8,0,...]}` — address `1.2.8`, not `1.2.3`.**

---

### Failure Mode 2 — `absadd` else branch silently discards the first operand

The `else` branch of `absadd` (when `bptr->exp > aptr->exp`):

```c
} else {
    answer.exp = bptr->exp;
    temp = bptr->exp - aptr->exp;
    while (i <= temp) {
        ansmant[j++] = bmant[i++];         /* copy b's prefix */
    }
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];             /* copy b's suffix */
}
```
[`tumble.c:473–484`]

`aptr` is **never read**. The result is just `b`'s digits.

This fires whenever the first argument to `tumbleradd` has a more negative `exp` than the second — exactly what happens when `d = tumblersub(a, b)` strips a common prefix.

**Concrete counterexample** (standard same-level addresses):

- `a = {exp=0, [3,5,7,9,0,...]}`, `b = {exp=0, [3,2,1,0,...]}`

`strongsub(a, b)`:
- Skip equal position 0 (both 3): `answer.exp = -1`
- At position 1: `a[1]=5 > b[1]=2`, so `answer.mantissa[0] = 5-2 = 3`
- Copy `a[2]=7 → answer.mantissa[1]=7`, `a[3]=9 → answer.mantissa[2]=9`
- `d = {exp=-1, mantissa=[3,7,9,0,...]}`

`tumbleradd(d, b)`: same sign, `absadd(d, b)` with `b.exp(0) > d.exp(-1)` → **else branch**:
- `temp = 0 - (-1) = 1`  
- copies `b[0]=3, b[1]=2` (inner while: `i <= 1`)  
- outer while: copies `b[2]=1, b[3]=0, ...`

**Result: `{exp=0, [3,2,1,0,...]} = b`, not `a`.**

---

### Failure Mode 3 — `absadd` same-exp branch drops all but the first digit of the smaller operand

When both operands have the same `exp`:

```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;
    ansmant[0] = amant[0] + bmant[0];   /* only first digit pair used */
    i = j = 1;
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];           /* rest filled from b only */
}
```
[`tumble.c:460–484`]

`a[1], a[2], ...` are completely ignored. Only `a[0]` contributes.

---

### Failure Mode 4 — NPLACES truncation

In `absadd` with `aptr->exp > bptr->exp`:

```c
temp = aptr->exp - bptr->exp;
while (i < temp) {
    ansmant[j++] = amant[i++];
}
ansmant[j++] = amant[i++] + bmant[0];
i = 1;
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];
}
```
[`tumble.c:466–484`]

If `temp` is large, `b`'s low-order digits are truncated when `j` reaches `NPLACES-1`. Any digit in `b` (or in the result of `tumblersub`) beyond position 15 is silently dropped. Similarly, in `tumblerincrement`:

```c
if (idx + rightshift >= NPLACES) {
    gerror("tumblerincrement overflow\n");
}
```
[`tumble.c:612–619`]

The system treats overflow as a fatal error rather than silently wrapping, but the `absadd` path has no such guard.

---

### Why the code works at all — operand order matters

In actual use, `tumbleradd` is always called as **`tumbleradd(high_level, low_level)`** — the higher-`exp` (shallower) address first:

```c
/* granf2.c:296 */
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
/* stream first, width second — stream.exp ≥ width.exp */
```

```c
/* orglinks.c:131 */
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
/* accumulated offset (higher level) + increment (lower level) */
```

In this order, `absadd` uses the `aptr->exp > bptr->exp` branch, which correctly places the high-level prefix and adds the low-level increment at the right position. The **reverse** call `tumbleradd(low, high)` hits the else branch and returns `high` unchanged — it is not an error from the code's perspective, but it does not produce `low + high`.

The identity that holds in practice is:

```
tumbleradd(start, tumblersub(end, start)) == end
```

— **start first**, difference second — because `start.exp ≥ width.exp` after prefix cancellation.

The question's formulation `tumbleradd(tumblersub(a, b), b)` puts the **difference first**, which reverses the expected operand order and triggers the else branch.

---

### Summary table

| Condition | `d = tumblersub(a, b)` | `tumbleradd(d, b)` | Recovers `a`? |
|-----------|------------------------|---------------------|---------------|
| `b == 0` | `d = a` | `a + 0 = a` | ✓ |
| `a == b` | `d = 0` | `0 + b = b = a` | ✓ |
| `a == 0` | `d = -b` | `-b + b = 0 = a` | ✓ |
| `b.exp < a.exp` | `d = a` (strongsub early return [`tumble.c:544`]) | `absadd(a,b)` blends b into a | ✗ |
| Same-level, common prefix | `d.exp` more negative than `b.exp` | `absadd` else branch returns `b` [`tumble.c:473`] | ✗ |
| Same `exp` | `d.exp` more negative after prefix strip | `absadd` same-exp branch drops `a[1..]` [`tumble.c:462`] | ✗ |
| `temp ≥ NPLACES` | Bits overflow | Low-order truncation [`tumble.c:480`] | ✗ |

---

### Conclusion

`tumbleradd` and `tumblersub` are **not inverses** in the general case. The `absadd` implementation is explicitly **asymmetric**: the first argument supplies the high-level prefix; the second supplies the low-level suffix/increment. When `d = tumblersub(a, b)` is computed, the result has a more negative `exp` than `b` (because common prefix digits were cancelled), so `tumbleradd(d, b)` treats `b` as the dominant prefix and discards `d`'s information — returning `b`, not `a`.

Precision loss from the fixed 16-place mantissa is a secondary concern: the **operand-order asymmetry** causes total information loss even before any digit overflow can occur. The arithmetic is correct only in the direction the code actually uses it: `tumbleradd(higher_level_address, lower_level_offset)`.
