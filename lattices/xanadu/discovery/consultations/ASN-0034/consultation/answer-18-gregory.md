## Question 18 [gregory]

> What happens when `tumbleradd` or `tumblerincrement` would produce a result requiring more than 16 mantissa digits — is there silent truncation, wraparound, or an error condition, and has this limit ever been hit in practice?

## KB Synthesis

This question is not answerable from the KB.

The KB establishes the relevant structural facts: tumblers have a fixed-precision representation with exactly `NPLACES` (16) mantissa digits and a short exponent [SS-TUMBLER Finding 0031], and operations like `tumblerincrement` and `tumbleradd` are used throughout the codebase for I-address allocation and V-position arithmetic [SS-ADDRESS-SPACE, ST-INSERT, ST-REARRANGE].

However, no finding documents what happens when arithmetic would overflow the 16-digit mantissa — whether the implementation silently truncates, wraps, errors via `qerror`/abort, or whether `tumblerjustify` handles this. The KB also contains no evidence that this limit has been hit in practice (e.g., no golden test failure or finding referencing a mantissa-overflow bug).

This would require direct code inspection of `tumble.c`'s `tumbleradd` and `tumblerincrement` implementations, particularly their carry-propagation and overflow paths.

---

## Code Exploration

I have everything I need. Here is the full analysis:

---

## Tumbler Overflow Behavior: `tumbleradd`, `tumblerincrement`, and the 16-digit limit

---

### The Data Structure

From `common.h:53-65`:

```c
#define NPLACES 16  /* places in mantissa of tumbler - increased from 11 to support deeper version chains */

typedef UINT tdigit;   // uint32_t — common.h:57, defs.h:12

typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];   // 16 slots of uint32_t
} tumbler;
```

The mantissa is a 16-element array of **unsigned 32-bit integers**. Each element is one "place" or "story" in the Xanadu hierarchical address (e.g., `1.1.0.2.0.5` uses 6 places). Zeros within the mantissa are semantic level separators, not padding. Tumblers are always normalized so that `mantissa[0] != 0` for non-zero tumblers [tumble.c:186-190].

---

### `tumblerincrement` — Two Distinct Failure Modes

`tumblerincrement(aptr, rightshift, bint, cptr)` at `tumble.c:599` adds `bint` at the position `rightshift` places to the right of the last non-zero digit.

```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);  // find last nonzero [tumble.c:611]

if (idx + rightshift >= NPLACES) {   // [tumble.c:612]
#ifndef DISTRIBUTION
    dumptumbler(aptr);
    fprintf(stderr, " idx = %d  rightshift = %d\n", idx, rightshift);
    gerror("tumblerincrement overflow\n");   // [tumble.c:616]
#else
    gerror("");                              // [tumble.c:618]
#endif
}
cptr->mantissa[idx + rightshift] += bint;  // [tumble.c:621]
```

`gerror` is defined as `#define gerror(s) qerror(s)` [common.h:119], and `qerror` at `genf.c:546-551`:

```c
INT qerror(char *message)
{
    fprintf(stderr, "Error: %s\n", message);
    abort();          // process terminates
    return(1);
}
```

**Failure Mode 1: Structural overflow** (`idx + rightshift >= NPLACES`)

The result would require a mantissa position at index ≥ 16. This is **detected explicitly**. In both DISTRIBUTION and non-DISTRIBUTION builds the code calls `gerror` → `qerror` → `abort()`. The process dies; there is no silent truncation, no wraparound. In non-DISTRIBUTION builds a diagnostic is printed first.

**Failure Mode 2: Digit-value overflow** (`mantissa[pos] + bint > UINT32_MAX`)

Line 621: `cptr->mantissa[idx + rightshift] += bint` performs unsigned 32-bit arithmetic with no overflow check. If the sum exceeds `2^32 − 1`, C's unsigned wraparound applies **silently** — no error, no diagnostic, wrong answer stored. This is undocumented and unguarded.

In practice this would require a single digit value to exceed ~4 billion. Given how the allocator works (allocating documents as 1, 2, 3, … under each account [granf2.c:162-175]), individual digits stay small. But a text span of more than 4 billion characters in a single leaf crum would trigger it.

---

### `absadd` (called by `tumbleradd`) — No Overflow Check at All

`absadd` at `tumble.c:444` is the active addition implementation (the `OlDVeRsIon` variant at line 488 is dead code). It performs a **single-point addition**, not a full multi-precision carry chain.

**Equal-exponent case** [tumble.c:460-464]:

```c
answer.exp = aptr->exp;
ansmant[0] = amant[0] + bmant[0];  // one uint32_t add, no carry check [tumble.c:462]
i = j = 1;
```

Then the loop [tumble.c:480-482] copies `bmant[1..15]` verbatim; `amant[1..15]` is entirely discarded. If `amant[0] + bmant[0]` overflows `uint32_t`, the result **wraps silently** with no error or diagnostic of any kind.

**Unequal-exponent case** [tumble.c:464-482]:

When `aptr->exp > bptr->exp`: the prefix of `amant` is copied, then one digit of `amant[i] + bmant[0]` is added at the crossover point (line 470), then the remainder of `bmant` is copied. Again, only one addition site, no carry, no overflow check.

When `bptr->exp > aptr->exp`: `bmant` is copied entirely and `amant` is discarded. The subtraction-via-negation path in `tumblersub` [tumble.c:426-429] routes through `tumbleradd`, subject to the same constraints.

**There is no structural overflow guard in `absadd`.** If the combination of exponent difference and mantissa depth would require writing past `NPLACES`, the loop `while (j <= NPLACES-1)` simply copies `bmant[i++]` until `j` reaches `NPLACES-1`. However, the tumblercheck invariant `exp <= 0` [tumble.c:174] limits how many leading positions are possible, and in practice the two operands are always within the same address subspace.

---

### Has This Limit Ever Been Hit?

**Yes — definitively, in practice, with `NPLACES=11`.**

From `bugs/0012-deep-version-chain-crash.md`:

> The backend crashes when creating or accessing version chains deeper than 3–4 levels. The root cause was tumbler overflow — document addresses for deep versions exceed the tumbler mantissa capacity. The tumbler struct had `NPLACES=11` mantissa digits. Deep version chains exceed this, causing overflow in `tumblerincrement`.

Version addresses grow one digit per generation: `1.1.0.1.0.1` → `1.1.0.1.0.1.1` → `1.1.0.1.0.1.1.1` etc. With NPLACES=11, a version chain of depth ~4 hit the structural check at `tumble.c:612`, `gerror` fired, and the process `abort()`ed.

The fix was increasing NPLACES from 11 to 16, recorded in `common.h:53` with the comment *"increased from 11 to support deeper version chains."* Verified working to depth 5 after the fix. Bug 0012 notes that some of those crashes may also have been triggered by the separate `recombine` stack buffer overflow (Bug 0020), since both produce `SIGABRT` with no `gerror` message in the DISTRIBUTION build.

---

### Summary Table

| Operation | Condition | Behavior |
|---|---|---|
| `tumblerincrement` | `idx + rightshift >= NPLACES` (position overflow) | `gerror` → `abort()` — detected, fatal, never silent |
| `tumblerincrement` | `mantissa[pos] += bint` overflows `uint32_t` (digit overflow) | Silent unsigned wraparound — **undetected** |
| `absadd` / `tumbleradd` | `amant[0] + bmant[0]` overflows `uint32_t` | Silent unsigned wraparound — **undetected** |
| `absadd` | Result would need > NPLACES positions | No guard — copies beyond intended range (UB if it occurs) |
| **NPLACES=11 hit** | Deep version chains (depth ≥ 4–5) | Confirmed in Bug 0012; fixed by raising to NPLACES=16 |

The short answer: structural position overflow in `tumblerincrement` causes `abort()`, not silent truncation. Digit-value (`uint32_t`) overflow in both `tumblerincrement` and `absadd` wraps silently with no error. The NPLACES limit was concretely hit in practice with the original value of 11, forcing it to be raised to 16 — the code still carries that comment today at `common.h:53`.
