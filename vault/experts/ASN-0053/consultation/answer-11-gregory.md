## Question 11 [gregory]

> Given that tumblers use `.0.` as a hierarchical separator by convention but not enforcement, does a span starting at `1.1` with width `0.5` cover position `1.3.0.1` — i.e., do spans enumerate all tumblers within the range regardless of hierarchical depth?

## KB Synthesis

## Spans Are Flat Numeric Intervals

**Yes, `1.3.0.1` falls within a span starting at `1.1` with width `0.5`** (reaching `1.6`). Span containment uses the tumbler total order, which is purely lexicographic — the `.0.` hierarchical separator convention has no effect on containment arithmetic.

### The Total Order

From [INV-TUMBLER-TOTAL-ORDER] and [SS-TUMBLER, Finding 0031]: `tumblercmp` compares tumblers by expanding to their fixed-precision mantissa representations. `1.1.0.2 < 1.1.0.2.0.1` because the shorter tumbler compares as having trailing zeros — which are less than the non-zero continuation. The comparison is purely positional on the digit sequence.

For the specific case:
- `1.1` → mantissa `[1, 1, 0, 0, ..., 0]`
- `1.3.0.1` → mantissa `[1, 3, 0, 1, 0, ..., 0]`
- `1.6` → mantissa `[1, 6, 0, 0, ..., 0]`

Digit-by-digit: position 1 differs. `1 < 3 < 6`, so `1.1 < 1.3.0.1 < 1.6`. The address falls strictly interior to the span (`THRUME` in [SS-INTERVAL-CMP] and [SS-WHEREONCRUM] terminology).

### The Mechanism

From [SS-INTERVAL-CMP]: `intervalcmp(left, right, address)` classifies membership using `tumblercmp` directly. No special handling exists for `.0.` boundaries — the function is unaware of address hierarchy. The half-open interval `[1.1, 1.6)` includes every tumbler `t` where `tumblercmp(1.1, t) != GREATER && tumblercmp(t, 1.6) == LESS`, regardless of how many `.0.` separators `t` contains.

From [SS-TUMBLER, Finding 0001]: "The document/element decomposition is a predicate over tumblers, not a structural subtype." The `.0.` hierarchy is a convention enforced by callers, not by the comparison machinery [PRE-SUBSPACE-CONVENTION].

### Practical Implications

In POOM queries ([SS-POOM-MULTIMAP]), `findcbcinarea2d` traverses the B-tree using this same total order. Any entry with a V-address in `[1.1, 1.6)` is returned — if `1.3.0.1` were stored as a V-address, it would be found.

In practice, text V-addresses within a document are allocated as `1.1, 1.2, 1.3, ...` (flat byte offsets via `tumblerincrement` with `rightshift=0`) [SS-ADDRESS-SPACE, Finding 0033], so hierarchically deep V-addresses don't typically arise in the text subspace. But for I-address spans (permascroll queries), this matters: a span `[2.1.0.5.0.100, width=10)` would capture `2.1.0.5.0.100.3.1` if such an address existed, because it falls numerically within the range.

The subspace boundary between text (`1.x`) and links (`2.x`) is also enforced through this total order: the two-blade knife in INSERT sets `blade[1] = 2.1` to exclude the link subspace from shift operations [SS-TWO-BLADE-KNIFE, FC-SUBSPACE] — which only works correctly because the total order places all `1.x` addresses below `2.1` and all `1.3.0.1`-style addresses in between.

---

## Code Exploration

Now I have everything I need. Let me trace through the full arithmetic.

---

## Answer

**Yes, the span `[start=1.1, width=0.5)` covers position `1.3.0.1`.** The backend uses flat mantissa comparison with no hierarchical semantics baked into the comparison logic. Here is the complete proof from the source.

---

### 1. The C Tumbler Structure

From `backend/common.h:53-65`:

```c
#define NPLACES 16
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

A tumbler is an exponent plus a 16-place array of non-negative digits. The `.` in `1.3.0.1` is **not stored** — only the integer digits are, laid out in `mantissa[0..3]`.

---

### 2. Protocol Parsing: How `1.3.0.1` Enters the C Backend

The Python client encodes `Tumbler(1,3,0,1)` on the wire as `0.1.3.0.1~` — the leading `0` is the count of leading zeros (the exponent), followed by each digit separated by `.` [`client.py:166-174`].

The FE parser `gettumbler` in `backend/get2fe.c:69-88`:

```c
bool gettumbler(typetask *taskptr, tumbler *tumblerptr)
{
    INT i, num, value;
    tumblerclear(tumblerptr);
    getnum(taskptr, &num);       // reads leading number: "0"
    tumblerptr->exp = -num;      // exp = 0
    for (i = 0; gettdigit(taskptr, &value); i++) {
        tumblerptr->mantissa[i] = value;
    }
    ...
}
```

`gettdigit` [`get2fe.c:90-99`] simply consumes a `.` then reads the next integer. For `0.1.3.0.1~`:

| mantissa slot | value |
|---|---|
| mantissa[0] | 1 |
| mantissa[1] | 3 |
| mantissa[2] | 0 |
| mantissa[3] | 1 |
| mantissa[4..15] | 0 |

Result: **`exp=0, mantissa=[1,3,0,1,0,…]`**

The `0` in position 2 is just a zero digit. It has no structural role in the comparison engine.

---

### 3. Computing the Span End: `1.1 + 0.5`

The start `1.1` (wire `0.1.1~`): `exp=0, mantissa=[1,1,0,…]`  
The width `0.5` (wire `1.5~`): `exp=-1, mantissa=[5,0,…]`

`functiontumbleradd` dispatches to `absadd` in `backend/tumble.c:444-484`:

```c
} else if (aptr->exp > bptr->exp) {   // 0 > -1: true
    answer.exp = aptr->exp;            // exp = 0
    temp = aptr->exp - bptr->exp;      // temp = 1
    while (i < temp) {
        ansmant[j++] = amant[i++];     // ansmant[0] = 1  (copies a's leading digit)
    }
    ansmant[j++] = amant[i++] + bmant[0];  // ansmant[1] = 1 + 5 = 6
    i = 1;
}
while (j <= NPLACES-1) {
    ansmant[j++] = bmant[i++];         // rest are zeros
}
```

Span end = **`exp=0, mantissa=[1,6,0,…]`** = `1.6`.

---

### 4. The Comparison: Does `1.3.0.1` fall in `[1.1, 1.6)`?

Span membership is determined by `intervalcmp` in `backend/tumble.c:144-160`:

```c
INT intervalcmp(tumbler *left, tumbler *right, tumbler *address)
{
    cmp = tumblercmp(address, left);
    if (cmp == LESS) return TOMYLEFT;
    else if (cmp == EQUAL) return ONMYLEFTBORDER;
    cmp = tumblercmp(address, right);
    if (cmp == LESS) return THRUME;        // inside
    else if (cmp == EQUAL) return ONMYRIGHTBORDER;
    else return TOMYRIGHT;
}
```

`tumblercmp` dispatches to `abscmp` for two positive tumblers [`tumble.c:87-111`]:

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) { ... }
    else {
        a = (INT *) aptr->mantissa;
        b = (INT *) bptr->mantissa;
        for (i = NPLACES; i--;) {
            if (!(cmp = *a++ - *b++)) {}
            else if (cmp < 0) return LESS;
            else return GREATER;
        }
    }
    return EQUAL;
}
```

**Check 1: `address (1.3.0.1)` vs `left (1.1)`**

Both have `exp=0`. Compare mantissa left-to-right:
- `mantissa[0]`: `1 − 1 = 0` → equal, continue
- `mantissa[1]`: `3 − 1 = +2` → **GREATER**

`tumblercmp(address, left) = GREATER` → address is not to the left.

**Check 2: `address (1.3.0.1)` vs `right (1.6)`**

Both have `exp=0`. Compare mantissa:
- `mantissa[0]`: `1 − 1 = 0` → continue
- `mantissa[1]`: `3 − 6 = −3` → **LESS**

`tumblercmp(address, right) = LESS` → `intervalcmp` returns **`THRUME`** (inside the interval).

---

### 5. The Zero at `mantissa[2]` Is Irrelevant to Span Membership

The comparison terminates at position 1 — the `0` at `mantissa[2]` and `1` at `mantissa[3]` are never reached. They were already dominated by the `3 < 6` difference at position 1. Even if the comparison had reached `mantissa[2] = 0`, it would merely continue to the next slot. **There is no code path in `abscmp`, `intervalcmp`, or `whereoncrum` that treats a zero digit as a hierarchical fence.**

The comment in `common.h:53` confirms this is just convention:

```c
/* places in mantissa of tumbler - increased from 11 to support deeper version chains */
```

The only place `.0.` has semantic weight is in `tumbleraccounteq` [`tumble.c:38-70`], which is used for **account ownership testing**, not span membership.

---

### Verdict

**A span starting at `1.1` with width `0.5` covers `1.3.0.1`.** Spans enumerate all tumblers in the numeric half-open interval `[start, start+width)` using flat, left-to-right mantissa comparison. Hierarchical depth — the number of `.`-separated components — plays no role. Position `1.3.0.1` falls squarely in `[1.1, 1.6)` because `1.3 < 1.6` at the second mantissa slot, regardless of how many sub-components follow.
