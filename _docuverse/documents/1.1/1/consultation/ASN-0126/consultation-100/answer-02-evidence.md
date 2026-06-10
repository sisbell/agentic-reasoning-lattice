## Question 2 [evidence]

> Does udanax-green's tumbler addition (tumbleradd) guarantee a result strictly greater than its first operand whenever the addend is nonzero, or are there carry/normalization/exponent-shift cases where `s ⊕ ℓ ≤ s` despite `ℓ > 0`?

## KB Synthesis

## Tumbler Addition: Monotonicity Guarantee

The KB does not directly document `tumbleradd`'s edge-case behavior, but enough can be assembled from structural facts and analogous observations.

---

### What the KB does confirm

**For practical usage ranges, `s ⊕ l > s` holds.** [INV-MONOTONIC] establishes that I-address allocation via `tumblerincrement` (which delegates to `tumbleradd`-family logic) is strictly increasing. [SS-ENFILADE-TREE] and [ST-INSERT] rely on this monotonicity without qualification for the actual V- and I-addresses encountered in operation.

**`tumbleradd` computes genuine arithmetic — it has no exponent guard.** The strongest evidence comes from [PRE-REARRANGE]/[ST-REARRANGE] (Finding 0051): a pivot with cuts at `[1.1, 1.4, 2.5]` produces `diff[1] = 2.5 - 1.4 = 1.1`, and `tumbleradd` of a V-position at `1.1..1.3` with offset `1.1` yields `2.2..2.4` — a cross-subspace result. This proves `tumbleradd` does not refuse to add when exponents differ; it computes across subspace boundaries.

This is the sharpest contrast with `strongsub`. [SS-TUMBLER] (Finding 0055) documents that `strongsub` has an explicit exponent guard: when `b.exp < a.exp`, it returns `a` unchanged without performing any subtraction. **The KB has no analogous statement for `tumbleradd`**, and the rearrangement evidence actively contradicts such a guard for addition.

---

### Where the guarantee may fail

The KB identifies two failure modes, neither well-documented for `tumbleradd` specifically:

**1. Sub-precision precision loss (`s ⊕ l = s`, equality).**

[SS-TUMBLER] (Finding 0031) establishes a fixed mantissa of `NPLACES = 16` digits. When `l` is representable only at a scale that requires more than 16 mantissa positions relative to `s`'s exponent, the addition loses `l` entirely and returns `s` unchanged. For example, if `s` has `exp = 0` and `l` has `exp = -17`, aligning `l` into `s`'s mantissa requires a position beyond mantissa[15], so the contribution disappears. The result: `s ⊕ l = s`, violating strict inequality.

This is **precision loss, not a guard** — unlike `strongsub`'s intentional exponent check. The KB implies `tumbleradd` performs alignment and adds; when `l` falls entirely below the precision floor, the numerical contribution is zero.

**2. Mantissa overflow (`s ⊕ l < s`, strictly less).**

The 16-digit mantissa with sign-magnitude representation [SS-TUMBLER] (Findings 0031, 0053) implies a maximum positive representable value near 10^16. Adding two positive tumblers whose sum requires a 17th digit causes overflow. The KB does not document `tumbleradd`'s overflow policy (truncation, saturation, or wrap). If it wraps (as unsigned C arithmetic does), the result could be strictly less than `s`. This case is not documented and does not arise in practice — actual V-addresses (`1.x` to `3.x`) and I-addresses (a handful of hierarchy levels) are far below the overflow threshold.

---

### Summary table

| Condition | `s ⊕ l` vs `s` | KB basis |
|---|---|---|
| Typical range usage | `> s` (strictly greater) | [INV-MONOTONIC], [ST-INSERT], [ST-REARRANGE] |
| `l` below 16-digit precision floor | `= s` (equality) | [SS-TUMBLER] NPLACES=16 fixed mantissa |
| `s` near 16-digit maximum (overflow) | potentially `< s` | [SS-TUMBLER] sign-magnitude; overflow policy undocumented |
| Cross-exponent, but both within precision | `> s` (no exponent guard) | [ST-REARRANGE] Finding 0051; contrast with [SS-TUMBLER] Finding 0055 for `strongsub` |

The KB's silence on `tumbleradd` overflow is notable — it is consistent with overflow being unreachable in practice but does not rule it out in the abstract. The sub-precision equality case (`s ⊕ l = s`) is a real structural consequence of fixed-width representation that the KB indirectly confirms via the NPLACES constraint, even though no finding explicitly demonstrates it for `tumbleradd`.

---

## Code Exploration

I have traced every path. Here is the complete analysis.

---

## `tumbleradd` Monotonicity Analysis

### Representation

`common.h:53–65`:
```
NPLACES = 16
tdigit  = uint32_t
tumbler: { exp: short, mantissa: uint32_t[16] }
```

`exp` is always ≤ 0 (`tumblercheckptr` at `tumble.c:174`). A less-negative `exp` means a *greater* address — `abscmp` (`tumble.c:92`) orders by `exp` first. A valid digit satisfies `(INT)digit >= 0`, i.e., digit ≤ `0x7FFFFFFF` = `INT_MAX`. The digit bound is enforced by `tumblercheckptr` at `tumble.c:202-209`, but that check is **commented out** in all active call sites (`tumble.c:397`).

`tumbleradd` is a macro (`common.h:197`):
```c
#define tumbleradd(x,y,z) functiontumbleradd(x,y,z)
```

---

### `functiontumbleradd` — call routing

`tumble.c:365-404`:

| Condition | Action |
|-----------|--------|
| `ℓ == 0` | `c = s` (trivially `c = s`, not `c > s`) |
| `s == 0` | `c = ℓ` → `c > 0 = s` ✓ |
| `s.sign == ℓ.sign` | `absadd(s, ℓ, c)` — same sign, add magnitudes |
| `\|s\| > \|ℓ\|`, opposite signs | `strongsub(s, ℓ, c)` |
| `\|ℓ\| ≥ \|s\|`, opposite signs | `weaksub(ℓ, s, c)` |

For the typical address case—both positive (`sign=0`)—all arithmetic flows through `absadd`.

---

### `absadd` — structure and behavior

`tumble.c:444-485`. The function has **three branches** on `aptr->exp` vs `bptr->exp`, i.e., on `s->exp` vs `ℓ->exp`. Throughout, `aptr = s`, `bptr = ℓ`.

**There is no carry propagation anywhere.** Each digit position is computed with a single `+`, independently of all others.

#### Branch 1: `s->exp == ℓ->exp` (`tumble.c:460-463`)
```c
answer.exp = aptr->exp;
ansmant[0] = amant[0] + bmant[0];    // single digit add, no carry
i = j = 1;
```
Then the tail loop copies `bmant[1..]` into `ansmant[1..]`.

Result: `c = [ s[0]+ℓ[0],  ℓ[1], ℓ[2], ..., ℓ[15] ]`, `c.exp = s.exp`.

Monotonicity check vs `s` in `abscmp` (`tumble.c:87-111`):
```c
a = (INT *) aptr->mantissa;   // cast uint32_t → int32_t
b = (INT *) bptr->mantissa;
cmp = *a++ - *b++;             // signed subtraction at each digit
```
At position 0: `cmp = (INT)(s[0]+ℓ[0]) − (INT)s[0]`.

- If `s[0]+ℓ[0] ≤ INT_MAX`: `cmp = ℓ[0] > 0` → **GREATER** ✓
- If `s[0]+ℓ[0] > INT_MAX` (sum overflows int32_t but **not** uint32_t — see below): `(int32_t)(s[0]+ℓ[0])` is negative; the subtraction `cmp = (int32_t)(s[0]+ℓ[0]) - (int32_t)s[0]` overflows signed int — formally UB, but on any two's-complement platform the result is `(s[0]+ℓ[0] − s[0]) mod 2^32 = ℓ[0] > 0` → **GREATER** ✓

**Can uint32_t ever overflow here?** Valid digits satisfy `digit ≤ INT_MAX = 0x7FFFFFFF`. So `s[0] + ℓ[0] ≤ 2 × 0x7FFFFFFF = 0xFFFFFFFE < 2^32`. **No uint32_t wrap.** The sum always fits in `uint32_t`.

#### Branch 2: `s->exp > ℓ->exp` (`tumble.c:464-471`)
```c
answer.exp = aptr->exp;          // = s.exp
temp = aptr->exp - bptr->exp;    // > 0
while (i < temp)
    ansmant[j++] = amant[i++];   // copy s[0..temp-1] verbatim
ansmant[j++] = amant[i++] + bmant[0];   // c[temp] = s[temp] + ℓ[0]
i = 1;
// tail: c[temp+1..] = ℓ[1..]
```

Result: `c = [ s[0], …, s[temp-1],  s[temp]+ℓ[0],  ℓ[1], … ]`, `c.exp = s.exp`.

Monotonicity check: `abscmp` walks digits left to right.
- Positions 0 … temp−1: exactly equal to `s` → `cmp = 0`, continue.
- Position temp: `cmp = (INT)(s[temp]+ℓ[0]) − (INT)s[temp]` = `ℓ[0]` (same two's-complement argument) > 0 → **GREATER** ✓

Note: positions after `temp` differ (`c` has ℓ's tail; `s` has its own tail), but `abscmp` short-circuits at `temp` and never inspects them.

#### Branch 3: `ℓ->exp > s->exp` (`tumble.c:472-478`)
```c
answer.exp = bptr->exp;          // = ℓ.exp (larger, less negative)
temp = bptr->exp - aptr->exp;    // > 0
while (i <= temp)
    ansmant[j++] = bmant[i++];   // copy ℓ[0..temp]
// tail loop: copy ℓ[temp+1..NPLACES-1]
```

**`aptr`'s (s's) mantissa is never read.** The result is a verbatim copy of `ℓ`. This is a latent computation bug—the mathematical sum should be `s + ℓ`, but the code discards `s`.

However, for monotonicity: since `ℓ.exp > s.exp`, `abscmp` short-circuits on the exponent comparison at `tumble.c:92-97` and returns **GREATER** immediately. So `c = ℓ > s` ✓.

---

### Edge-case summary

| Case | Result | `c > s`? | Notes |
|------|--------|----------|-------|
| `ℓ = 0` | `c = s` | `c = s` — not applicable, ℓ assumed > 0 | — |
| `s = 0` | `c = ℓ` | ✓ | — |
| Same `exp`, valid digits | `c[0] = s[0]+ℓ[0]` | ✓ | No uint32_t overflow; two's-comp comparison gives GREATER |
| `s.exp > ℓ.exp`, valid digits | `c[temp] = s[temp]+ℓ[0]` | ✓ | Same arithmetic argument |
| `ℓ.exp > s.exp` | `c = ℓ` (s discarded) | ✓ | c > s by exponent ordering |
| Invalid digit (`digit > INT_MAX`) | wraps or gives "negative digit" per `tumblercheckptr:202` | **FAILS** | `tumblercheck` commented out at `tumble.c:397`; invalid inputs can propagate |

---

### Carry / normalization / exponent-shift verdict

**There is no carry in `absadd`.** Each digit is summed once at a single position (`tumble.c:462`, `tumble.c:470`). No carry can propagate "backward" to reduce a higher-order digit.

**Normalization (`tumblerjustify`) is not called after `absadd`.** The comment at `tumble.c:377` says `absadd` returns a pre-justified result. This is correct: in all three branches, `answer.mantissa[0]` is nonzero whenever at least one input is nonzero (`amant[0]` in branches 1 and 2, `bmant[0]` in branch 3), so no leading-zero normalization shift occurs.

**Exponent shift**: the result's `exp` is always `max(s.exp, ℓ.exp)`, set directly in each branch. No shift happens.

---

### Conclusion

**For valid positive tumblers (all mantissa digits ≤ `INT_MAX = 0x7FFFFFFF`), `tumbleradd(s, ℓ, c)` guarantees `c > s` whenever `ℓ > 0`.**

There are no carry, normalization, or exponent-shift cases that can produce `c ≤ s`. The argument rests on three facts:

1. **No uint32_t digit overflow**: valid digits sum to at most `2 × INT_MAX = 0xFFFFFFFE < 2^32`, so no digit wraps to 0 or a smaller value.
2. **`abscmp` comparison is self-consistent**: the signed-int subtraction used in `abscmp:101-108` to compare digits behaves correctly under two's-complement wrapping, producing `cmp = ℓ[k] > 0` even when the sum digit exceeds `INT_MAX`.
3. **The buggy else branch** (`tumble.c:472-478`) ignores `s` and returns `ℓ`, but since that branch is entered only when `ℓ.exp > s.exp`, `ℓ > s` by exponent order and the monotonicity inequality still holds.

**Two caveats:**

- The guarantee is **formal UB** in C when a sum digit exceeds `INT_MAX` because `abscmp` casts `uint32_t *` to `int32_t *` and uses signed arithmetic. In practice on all two's-complement platforms this works correctly, but a sufficiently aggressive compiler with `-O2` and no `-fwrapv` could in principle misoptimize it.

- **`tumblercheckptr` is commented out** everywhere in active paths (`tumble.c:397`, `tumble.c:311`, `tumble.c:338`). If an invalid tumbler with a digit `> INT_MAX` were to enter `absadd`, a uint32_t overflow at that digit is possible (e.g., `0xFFFFFFFF + 1 = 0`), and if that digit is position 0, `iszerotumbler` would return true and the result would compare as zero—less than any positive address. The "no overflow" guarantee depends entirely on input validity that is no longer actively enforced.
