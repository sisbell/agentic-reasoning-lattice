## Question 15 [gregory]

> Does `tumblerincrement` always produce the immediate successor in the total order, or does it increment only the least-significant nonzero digit — and if the latter, what is the formal successor relation between tumblers?

## KB Synthesis

`tumblerincrement` does **not** in general produce the immediate successor in the tumbler total order. It computes `t + n × 10^(-rightshift)` — that is, it adds `n` at a specific digit position determined by `rightshift`.

## What the function does

The signature is `tumblerincrement(source, rightshift, amount, dest)`:

- `rightshift=0, amount=1`: adds 1 at the units position → `t + 1`
- `rightshift=1, amount=n`: adds at the tenths position → `t + n × 0.1`

The zero-tumbler special case [SS-INSERT-VWIDTH-ENCODING] confirms this: `tumblerincrement(&zero, 1, 11, &result)` produces `exp = -1, mantissa[0] = 11`, representing `0.11`.

For I-address allocation [ST-INSERT], Finding 0031: `tumblerincrement(&lsa, 0, textset->length, &lsa)` with `rightshift=0` advances the address by the text length in integer units. For single-character allocation [SS-ADDRESS-SPACE], Finding 0033: `tumblerincrement(&lowerbound, 0, 1, isaptr)` steps by exactly 1.

## Why this is NOT the immediate total-order successor in general

The tumbler total order [INV-TUMBLER-TOTAL-ORDER] is lexicographic: compare signs, then exponents, then mantissa digits left-to-right. This means:

```
1.1.0.2.0.1  <  1.1.0.2.0.1.1  <  1.1.0.2.0.2
```

`tumblerincrement(1.1.0.2.0.1, 0, 1)` yields `1.1.0.2.0.2` — the **next sibling** — skipping over all descendants (`1.1.0.2.0.1.1`, `1.1.0.2.0.1.2`, ...). The KB makes this explicit [SS-ADDRESS-ALLOC], Finding 0021: `upperbound = tumblerincrement(hintisa, depth-1, 1)` is described as "the next sibling of the parent."

The function is deliberately used this way to compute **upper bounds** that fence off subtrees during allocation searches (via `findpreviousisagr`), not to enumerate all tumblers in order.

## When it does produce the total-order successor

For **permascroll atom I-addresses** (e.g., `2.1.0.5.0.100`), `tumblerincrement(t, 0, 1)` yields `2.1.0.5.0.101`, which is the immediate successor. This holds because permascroll I-addresses have no descendants by construction — the allocation scheme never creates sub-tumblers below a content atom address [SS-ADDRESS-SPACE], Finding 0033. So for flat I-address ranges, integer-step increment equals total-order increment.

## The formal successor relation

`tumblerincrement(t, k, n)` computes `t + n × 10^(-k)` in the tumbler numeric representation. The total-order immediate successor of `t` would require knowing the global state: if any tumbler `t'` exists with `t < t' < t + 10^(-k)` (i.e., any descendant of `t`), then `t + 10^(-k)` is not the immediate successor. The function makes no such promise — it is a pure arithmetic operation, not a search over existing addresses.

---

## Code Exploration

Now I have everything needed for a complete answer. Let me synthesize from the source code.

---

## Answer: `tumblerincrement` and the Tumbler Successor Relation

### 1. What `tumblerincrement` actually computes

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
// tumble.c:599
```

The function has two paths:

**Zero-tumbler path** [tumble.c:603–608]: Constructs a new tumbler from scratch — `exp = -rightshift`, `mantissa[0] = bint`. Used when `aptr` is the origin.

**Non-zero path** [tumble.c:609–622]:
```c
for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
// ...
cptr->mantissa[idx + rightshift] += bint;
tumblerjustify (cptr);
```

The loop scans backward from `mantissa[NPLACES-1]` and stops at the **last (highest-index, least-significant) non-zero digit** — call this position `idx`. It then adds `bint` to `mantissa[idx + rightshift]` and normalizes.

So with the canonical call `tumblerincrement(T, 0, 1, T)`:
- `idx` = position of the last nonzero mantissa digit
- `mantissa[idx]` += 1
- All digits after `idx` remain zero (trailing zeros were already there)

### 2. The tumbler data model and total order

From `common.h:59–65` and `defs.h`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;          // 1 = negative
    short exp;          // always <= 0  [tumblercheckptr, tumble.c:174]
    tdigit mantissa[NPLACES];  // NPLACES=16, each digit is unsigned int
} tumbler;
```

`iszerotumbler` [common.h:72] = `!mantissa[0]`. A normalized non-zero tumbler always has `mantissa[0] != 0`.

The **total order** is defined by `abscmp` [tumble.c:87–111]:
1. Compare `exp` fields: smaller exp (more negative) → LESS.
2. If equal exp, compare `mantissa[0..NPLACES-1]` **lexicographically** from index 0 to 15.

So the order is the strict lexicographic order on the tuple `(exp, mantissa[0], mantissa[1], ..., mantissa[15])`.

### 3. Does `tumblerincrement` produce the immediate successor?

**No.** There are infinitely many tumblers between `T` and `tumblerincrement(T, 0, 1, T')` in the total order.

Consider `T = [A, B]` (exp=0, `mantissa[0]=A, mantissa[1]=B, rest zero`). Then:

```
tumblerincrement(T, 0, 1) → [A, B+1]
```
(`idx=1`, adds 1 to `mantissa[1]`)

But the tumbler `[A, B, 1, 0, ...]` (exp=0) has:
- Same `mantissa[0]=A`, same `mantissa[1]=B`, then `mantissa[2]=1`
- Lexicographically: `[A, B, 1, ...] > [A, B, 0, ...]` = T  ✓
- Lexicographically: `[A, B, 1, ...] < [A, B+1, 0, ...]` = T' ✓

So `T < [A, B, 1] < T'`. The gap between T and its "next sibling" is an entire sub-tree of deeper addresses.

### 4. The formal successor relation

In the tumbler address space, tumblers form a tree:
- `[A]` is an ancestor of `[A, B]` for any B ≥ 1
- `[A, B]` is an ancestor of `[A, B, C]` for any C ≥ 1
- The tree order respects the total order: all descendants of T sort between T and T's next peer

The true **immediate successor** of T (with last nonzero at position `idx`) in the total order is `tumblerincrement(T, 1, 1)`, which adds a new digit 1 one level deeper:

```
immediate_successor([A, B]) = [A, B, 1]   (tumblerincrement with rightshift=1)
```

Because the mantissa digits are non-negative integers (`tdigit = UINT`), there is no value between `B` and `B+1` at the same position — the only things between `[A, B]` and `[A, B+1]` in the total order are sub-addresses of `[A, B]`.

### 5. What `rightshift` actually controls

`rightshift` shifts the write target relative to `idx`:

| rightshift | Write position | Semantic |
|---|---|---|
| `0` | `mantissa[idx]` | Increment last digit — **next peer** at current depth |
| `+1` | `mantissa[idx+1]` | Write to next-deeper level — **first child** = immediate successor |
| `+N` | `mantissa[idx+N]` | Write N levels deeper — Nth-generation child |
| `-1` | `mantissa[idx-1]` | Increment parent digit — **next peer at shallower depth** |

The call in `findaddressofsecondcutforinsert` [insertnd.c:179] uses `rightshift=-1` precisely to step up one level before finding an insertion boundary:
```c
tumblerincrement (position, -1, 1, secondcut);  // [A, B] → [A+1, B] (idx=1, writes to idx-1=0)
```

And in `setlinkvsas` [do2.c:172–176], a two-call sequence builds a two-digit tumbler:
```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // zero → [1], exp=0
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // [1] → [1, 1] (idx=0, writes to idx+1=1)
```

The `credel.c:511` usage `tumblerincrement(..., 2, 1, ...)` writes 2 positions deeper than the last nonzero digit.

### 6. Summary

**`tumblerincrement` increments the least-significant nonzero digit (at `idx`), offset by `rightshift`.** With the canonical `(rightshift=0, bint=1)` call:

- It does **not** produce the immediate successor in the total order.
- It produces the **next peer** at the same hierarchical depth — the smallest tumbler at that depth strictly greater than T.
- The formal gap `(T, tumblerincrement(T, 0, 1))` in the total order contains exactly the sub-tree of T: all tumblers of the form `[T.mantissa[0..idx], k, ...]` for k ≥ 1 and any deeper extensions.

The **true immediate successor** in the total order is `tumblerincrement(T, 1, 1)` — which appends a digit 1 one level deeper and is the first member of T's subtree `[tumble.c:599–622]`.
