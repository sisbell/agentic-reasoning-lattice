## Question 12 [gregory]

> Is the tumbler number line dense — can you always construct a tumbler strictly between any two distinct tumblers — or does the fixed 16-digit mantissa impose a minimum gap where no intermediate value can be represented?

## KB Synthesis

The tumbler number line is **not dense** at its finest representable scale, though the exponent mechanism provides a practical approximation of density for hierarchical address construction.

## What the KB tells us

**The representation is finite-precision by construction.** [SS-TUMBLER] Finding 0031 establishes that a tumbler is stored as a sign bit, a short exponent (`exp`), and a fixed-length mantissa of exactly `NPLACES = 16` digit positions. The exponent shifts the mantissa: `exp = 0` places the first digit at the most significant position; negative exponents represent sub-unit fractional positions.

**Adjacent values can exist at the digit level.** [SS-TUMBLER] Finding 0031 documents the increment primitive: `tumblerincrement(&lsa, rightshift, count, &result)` advances a tumbler by `count` units at the digit position indexed by `rightshift`. At `rightshift = 0` (the least significant occupied digit), incrementing by 1 produces the immediate successor — the next representable tumbler at that exponent level. [SS-ADDRESS-SPACE] Finding 0033 confirms this: sequential inserts receive tumblers exactly 1 apart (`tumblerincrement(&lowerbound, 0, 1, isaptr)`), and these are treated as adjacent with no intermediate address in the allocation scheme.

**The exponent is bounded.** The exponent is described as "a short exponent" in [SS-TUMBLER] Finding 0031, corresponding to a `SINT` (short integer in C, typically 16-bit, range −32768 to 32767). This places a floor on representable precision.

## The density conclusion

Between two tumblers A and B that differ only in the last mantissa digit by exactly 1 (same exponent, finest granularity), the exponent mechanism *could* in principle provide an intermediate by using `exp - 1` to represent a finer subdivision. But:

1. If the exponent is already at its minimum value, no more negative exponent is available, and the pair `{A, A+1}` at that scale has **no representable intermediate**.

2. [INV-MONOTONIC] treats the sequence as discrete: allocation always takes `max_existing + 1` with no interpolation step, confirming the implementation treats the I-address space as a sequence of discrete points, not a dense continuum.

3. [SS-ADDRESS-ALLOC] Finding 0021 shows the address allocation algorithm explicitly: find the highest existing address, truncate, and increment by 1 — the same integer-step model.

**Therefore: the tumbler number line is not mathematically dense.** It has the structure of a high-precision but finitely-quantized number system. At any given exponent level, adjacent integers (differing by 1 in the last digit) are truly adjacent — no tumbler with the same exponent fits between them. Finer precision requires a more negative exponent, but the 16-bit exponent bound means there is a finest granularity below which no further subdivision is representable.

The `.0.` hierarchical convention in address construction (depth parameters in [SS-ADDRESS-SPACE] Finding 0021, [SS-ADDRESS-ALLOC]) does allow inserting child addresses between any parent and its successor — but this is structural containment (appending `.0.N`), not numerical interpolation between two arbitrary adjacent values.

---

## Code Exploration

The finding has been prepared. Here is the full answer based on the source code:

---

## The Tumbler Number Line Is Not Dense

**The fixed 16-digit mantissa imposes a minimum gap. There exist pairs of adjacent tumblers with no representable value between them.**

---

### The Representation

From `common.h:53`:
```c
#define NPLACES 16  /* increased from 11 to support deeper version chains */
```

From `common.h:57–65` and `defs.h:12`:
```c
typedef UINT tdigit;   /* uint32_t */

typedef struct structtumbler {
    humber xvartumbler;
    char   varandnotfixed;
    char   sign  BIT;   /* 1 if negative */
    short  exp;         /* must be <= 0 */
    tdigit mantissa[NPLACES];
} tumbler;
```

A tumbler encodes a dotted address like `3.1.4` as `exp=0, mantissa=[3, 1, 4, 0, …]`. Leading zeros are not stored — the parser (`get2.c:81–83`) decrements `exp` and discards them, so `0.3.1` becomes `exp=-1, mantissa=[3, 1, 0, …]`.

**Validity constraint:** `tumblercheck` at `tumble.c:174–178` enforces `exp <= 0`. `exp > 0` is a hard error.

---

### The Ordering

`abscmp` (`tumble.c:87–111`):

1. Compare `exp` first: **larger `exp` → greater value** (so exp=0 > exp=−1)
2. If equal `exp`: **lexicographic mantissa** comparison slot-by-slot

---

### Two Families of Hard Gaps

#### Gap 1 — Between exp levels

Let:
- **A** = exp=−1, mantissa=`[UINT_MAX, UINT_MAX, …, UINT_MAX]` — the address `0.MAX.MAX…` at depth 16
- **B** = exp=0, mantissa=`[1, 0, …, 0]` — the address `1`

Any candidate M strictly between A and B must have:

| M's `exp` | Consequence |
|-----------|-------------|
| `exp < −1` | M < A — wrong direction |
| `exp = −1` | M ≤ A at best — can't exceed `[MAX,MAX,…]` |
| `exp = 0`, `mantissa[0] = 0` | **Invalid** — `tumble.c:186–190` rejects non-normalized: `exp ≠ 0` with `mantissa[0] = 0` is a hard error |
| `exp = 0`, `mantissa[0] ≥ 1` | M ≥ B |

**No representable tumbler exists between A and B.** This gap exists at every exp-level boundary.

#### Gap 2 — At full depth within the same exp

Given:
- **A** = exp=0, mantissa=`[k, UINT_MAX, UINT_MAX, …, UINT_MAX]` (all 16 slots filled)
- **B** = exp=0, mantissa=`[k+1, 0, 0, …, 0]`

Any M with A < M < B at exp=0 needs `mantissa[0] = k` and `mantissa[1..15] > [UINT_MAX, …, UINT_MAX]` — impossible — or `mantissa[0] = k+1`, giving M ≥ B.

**Minimum representable gap:** 1 unit at `mantissa[15]`, with the same `exp` and same `mantissa[0..14]`. Nothing finer exists.

---

### Code Evidence the Gaps Are Known and Intentional

**`strongsub` discards sub-scale differences.** `tumble.c:544–547`:
```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr, cptr);
    return(0);
}
```
When B's exp is smaller than A's (B is at finer scale), `A − B` returns `A`. The difference is below representable precision — the tumbler analogue of floating-point underflow. **Explicit and deliberate.**

**`tumblerincrement` has a hard overflow guard.** `tumble.c:611–619`:
```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
if (idx + rightshift >= NPLACES) {
    gerror("tumblerincrement overflow\n");
}
```
No way to push a depth-16 tumbler further right.

**The protocol parser rejects depth > 16.** `get2.c:88–90`:
```c
if (eatchar(taskptr, '.')) {
    fprintf(taskptr->errp, "tumbler overflow\n");
    return(FALSE);
}
```

**`absadd` has no carry propagation.** `tumble.c:462`:
```c
ansmant[0] = amant[0] + bmant[0];  /* no carry */
```
Each digit slot is independent. An overflow at `mantissa[15]` wraps silently (C unsigned arithmetic) rather than carrying into `mantissa[14]`. There is no arithmetic path to bridge a depth-16 gap.

**The NPLACES comment records the history.** `common.h:53`:
```c
#define NPLACES 16  /* increased from 11 to support deeper version chains */
```
The depth limit was a real bottleneck at 11 and was raised to 16 pragmatically. The ceiling is architectural, not accidental.

---

### Conclusion

The tumbler space is a **finite lattice**, not a continuum.

- **At shallow depths** (fewer than 16 components): effectively dense — you can always insert a sub-address by appending a new dot-component. No gap.
- **At full depth (16 components)**: discrete. The minimum step is 1 unit at `mantissa[15]`. Nothing smaller is representable.
- **At every exp boundary**: the maximally-deep tumbler at exp=n−1 and the minimal tumbler at exp=n are strictly adjacent — no value fits between them.

The density property holds in the practical range for Xanadu document addresses (which are typically a few levels deep). It fails precisely when you exhaust the 16-slot mantissa or hit an exp-level boundary. The `strongsub` underflow behavior and `tumblerincrement` overflow guard are the two places in the code where this fundamental limitation surfaces explicitly.
