## Question 19 [gregory]

> `tumblerjustify` normalizes a tumbler before equality comparison — what invariant does it restore (leading-zero removal, trailing-zero trimming, exponent normalization), and can two tumblers that are `tumblercmp`-ordered but not `tumblerjustify`-normalized produce an inconsistent ordering?

## KB Synthesis

## `tumblerjustify` and Normalization

**What the KB tells us about the representation**

From [SS-TUMBLER] Finding 0031: a tumbler is stored as `(sign, exp, mantissa[NPLACES=16])`. The exponent shifts the mantissa — `exp=0` places the first mantissa digit as most-significant; negative exp represents fractional positions. `tumblerlength()` returns `nstories(t) - t.exp` (significant digit count).

**What `tumblerjustify` normalizes**

The KB doesn't describe `tumblerjustify`'s implementation directly, but Finding 0031 gives the critical constraint:

> "Two tumblers are equal iff their sign, exponent, and all 16 mantissa digits match (**no normalization ambiguity after `tumblerjustify`**)"

The phrase "no normalization ambiguity after `tumblerjustify`" implies that without it, the same logical value can be represented multiple ways. Given the exponent/mantissa structure, the ambiguity is **leading-zero equivalence**: the value `0.11` can be represented as either:
- `exp=-1, mantissa=[1,1,0,...,0]` (normalized: first digit non-zero)
- `exp=0, mantissa=[0,1,1,0,...,0]` (unnormalized: leading zero shifts value by one position)

`tumblerjustify` restores the **canonical form** where the leading mantissa digit is non-zero (or the tumbler is zero), adjusting `exp` accordingly — analogous to floating-point normalization.

**Can unnormalized tumblers produce inconsistent ordering?**

Yes. From [INV-TUMBLER-TOTAL-ORDER] Finding 0031, `abscmp` compares exponents first: "a larger exponent means a larger absolute value." If two tumblers represent the same value but one has a leading zero (requiring a higher `exp` to "reach" the significant digits), `abscmp` would classify the larger-exponent variant as strictly greater — returning an incorrect non-zero comparison for logically equal values.

Concretely:
```
A = exp=0,  mantissa=[0,1,1,0,...,0]  → logically "0.11"
B = exp=-1, mantissa=[1,1,0,...,0]    → logically "0.11"

abscmp: compares exp first: 0 > -1 → returns GREATER
        But A and B are equal values → INCONSISTENT
```

This would break any ordering predicate that relies on the total-order invariant, including interval classification ([SS-INTERVAL-CMP]), POOM traversal ([SS-WHEREONCRUM]), and enfilade search ([SS-ENFILADE-TREE]).

**Conclusion**

`tumblerjustify` restores canonical form by eliminating leading zeros from the mantissa (adjusting exp accordingly), ensuring the representation is unique per value. Without this normalization, `tumblercmp`'s exponent-first comparison produces incorrect ordering for logically equal but differently-encoded tumblers. The KB directly confirms this: equality comparison is only unambiguous after `tumblerjustify`, and since ordering subsumes equality, unnormalized tumblers can corrupt the total order that all downstream operations depend on.

---

## Code Exploration

---

## `tumblerjustify`: Invariant and Ordering Safety Analysis

### The Tumbler Representation

The `tumbler` struct [`common.h:59-65`]:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;          /* 1 if negative, otherwise 0 */
    short exp;          /* always <= 0 for valid tumblers */
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

`NPLACES = 16` [`common.h:53`]. `mantissa[0]` is the most-significant digit (MSD). `exp` is always `<= 0` (positive `exp` is a validity error at [`tumble.c:174-178`]). The value is conceptually:

```
mantissa[0] at story-level exp
mantissa[1] at story-level exp-1
mantissa[2] at story-level exp-2
...
```

The zero tumbler is identified by the macro [`common.h:72`]:
```c
#define iszerotumbler(tumblerptr) (!((tumblerptr)->mantissa[0]))
```
It checks **only `mantissa[0]`**.

---

### What `tumblerjustify` Does

```c
int tumblerjustify(tumbler *tumblerptr)          /* tumble.c:289 */
{
    mantissaptr = tumblerptr->mantissa;
    if (mantissaptr[0] != 0) {                   /* line 296 */
        return(0);    /* already normalized */
    }
    for (shift = 0; mantissaptr[shift] == 0; ++shift) {
        if (shift == NPLACES - 1) {              /* line 302 */
            tumblerptr->exp = 0;
            tumblerptr->sign = 0;
            return(0);    /* all-zeros: canonical zero */
        }
    }
    /* left-shift mantissa by `shift` positions */
    for (i = 0, j = shift; j < NPLACES;)
        mantissaptr[i++] = mantissaptr[j++];    /* line 307 */
    while (i < NPLACES)
        mantissaptr[i++] = 0;
    tumblerptr->exp -= shift;                   /* line 310 */
}
```

Three paths:

1. **`mantissa[0] != 0` → return immediately** [`tumble.c:296-298`]. The tumbler is already in canonical form. No work to do.

2. **All `NPLACES` digits are zero → canonicalize to zero** [`tumble.c:299-305`]. Sets `exp = 0` and `sign = 0`. This ensures there is exactly one bit pattern for zero, eliminating "negative zero" (`sign=1, mantissa=all-zeros`, which `tumblercheck` explicitly rejects at [`tumble.c:180-183`]).

3. **Leading zeros with a non-zero tail → left-shift and adjust `exp`** [`tumble.c:306-313`]. Counts leading zero digits (`shift`), slides the mantissa array left by `shift` positions, zeros the vacated tail, and subtracts `shift` from `exp` to preserve value: `mantissa[0]_before` was at story-level `exp`; the first non-zero digit at position `shift` was at story-level `exp - shift`; after the shift, that digit is at `mantissa[0]` and the new `exp` equals `exp - shift`.

---

### The Invariant Restored

`tumblerjustify` restores **leading-digit normalization**:

> **For any non-zero tumbler, `mantissa[0]` must be non-zero.**

This is neither trailing-zero trimming (trailing zeros in the mantissa are left intact — `nstories` at [`tumble.c:255`] and `lastdigitintumbler` at [`tumble.c:282`] both work over trailing zeros without removing them) nor IEEE-style exponent bias normalization. It is strictly a requirement that the **first story slot be occupied by the most significant digit**.

`tumblercheck` gives the invariant explicitly in two diagnostics:

- **`"fucked up non-normalized"`** [`tumble.c:186-190`]: fires when `ptr->exp != 0 && ptr->mantissa[0] == 0` — the exponent says there are significant digits above story-0 but the top slot is empty.
- **`"nonzerozerotumbler"`** [`tumble.c:192-200`]: fires when `mantissa[0] == 0` but any later mantissa entry is non-zero — the digit is buried under leading zeros.

The secondary invariant also restored: **no negative zero** — the zero value always has `sign == 0` [`tumble.c:180-183`].

---

### Can Un-Normalized Tumblers Produce Inconsistent `tumblercmp` Ordering?

**Yes. The inconsistency is structural, not hypothetical.**

The root cause: `tumblercmp` [`tumble.c:72-85`] begins with zero-checks using `iszerotumbler`, which is defined as `!((tumblerptr)->mantissa[0])` [`common.h:72`]. Any un-normalized tumbler with `mantissa[0] == 0` and a non-zero digit somewhere in positions `1..15` is **misclassified as zero** by this macro. The actual non-zero value buried in the tail is invisible to `tumblercmp`.

**Concrete example of inconsistency:**

Let T be un-normalized: `mantissa = [0, 0, 5, 0, ...]`, `exp = 0`, `sign = 0`.  
T_norm (after `tumblerjustify`): `mantissa = [5, 0, ...]`, `exp = -2`, `sign = 0`.  
Let B be normalized: `mantissa = [3, 0, ...]`, `exp = -1`, `sign = 0`.

Actual ordering: T_norm at story-level `-2` vs B at story-level `-1`. In `abscmp`, `exp(-2) < exp(-1)`, so T_norm < B. Correct.

Now call `tumblercmp(T, B)` with un-normalized T:
- `iszerotumbler(T)` → `!mantissa[0]` → `!0` → **TRUE** (wrong — T is not zero)
- Fall into `return (bptr->sign ? GREATER : LESS)` [`tumble.c:78`]
- B has `sign = 0`, so returns **LESS**: T < B ← accidentally correct here

But call `tumblercmp(T, ZERO)` where ZERO is the genuine zero tumbler (all mantissa zero, exp=0):
- `iszerotumbler(T)` → TRUE (T misidentified as zero)
- `iszerotumbler(ZERO)` → TRUE (genuinely zero)
- Returns **EQUAL** [`tumble.c:76`]

So `tumblercmp` says T == 0 AND T < B AND 0 < B — which is self-consistent in this case. But now consider T2, an un-normalized tumbler with `mantissa = [0, 7, 0, ...]`, `exp = -3`, `sign = 0` (actual value 7 at story-level `-4`):

- `tumblercmp(T, T2)`: both have `mantissa[0] == 0`, so both are misclassified as zero → returns **EQUAL**
- `tumblercmp(T_norm, T2_norm)`: T_norm has `exp = -2` (story `-2`, value 5); T2_norm has `exp = -4` (story `-4`, value 7). In `abscmp`: `exp(-2) > exp(-4)`, so returns **GREATER**: T_norm > T2_norm

Result: `tumblercmp(T, T2) = EQUAL` but `tumblercmp(T_norm, T2_norm) = GREATER`. The un-normalized comparison and the normalized comparison give **opposite verdicts** for the same pair of values. Transitivity is broken: T == T2 and T == 0 and T2 == 0, but T_norm > T2_norm > 0.

**The mechanism is clear**: `abscmp` is only called when both operands pass the `!iszerotumbler()` gate. Un-normalized tumblers with leading zeros never reach `abscmp` at all — they are short-circuited at the zero-detection branches. Those branches do not look at `exp` or any mantissa position beyond `[0]`, so all structural information in positions `1..15` is discarded.

---

### Summary

| Question | Answer |
|---|---|
| What invariant does `tumblerjustify` restore? | `mantissa[0] != 0` for any non-zero tumbler (leading-zero removal). Also: the zero value is canonical — `sign = 0`, all mantissa zeros. |
| Which of leading-zero removal / trailing-zero trimming / exponent normalization? | **Leading-zero removal only.** Trailing zeros are preserved. `exp` is adjusted arithmetically as a consequence, not normalized by a separate rule. |
| Can un-normalized tumblers produce inconsistent `tumblercmp` ordering? | **Yes.** `iszerotumbler` checks only `mantissa[0]`. Any un-normalized tumbler (leading zeros, non-zero tail) is misclassified as zero and never reaches `abscmp`. Two such tumblers representing different positive values compare EQUAL to each other and to the actual zero tumbler, producing ordering contradictions. |

The defense in the codebase: `tumblersub` always calls `tumblerjustify` on its output [`tumble.c:430`]; `functiontumbleradd` and `tumblerincrement` call `partialtumblerjustify` (a slightly more efficient variant that skips the early-exit check [`tumble.c:315-340`]) whenever a leading zero can occur. `partialtumblerjustify` is identical in logic; callers guard it with `if(cptr->mantissa[0] == 0)` [`tumble.c:387, 392`]. These call sites collectively enforce that public outputs of arithmetic operations are always normalized before being handed to comparison functions.
