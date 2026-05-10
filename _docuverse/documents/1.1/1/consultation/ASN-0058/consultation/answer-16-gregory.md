## Question 16 [gregory]

> What is the precise boundary condition for the ONMYRIGHTBORDER case in `whereoncrum` — does it require exact equality between the query point and the crum's reach (displacement + width), and does it use `tumblereq` with full 16-digit comparison?

## KB Synthesis

The KB provides precise information on this, primarily from [SS-WHEREONCRUM] and [SS-INTERVAL-CMP].

## Boundary Condition for ONMYRIGHTBORDER

**Exact equality is required.** `whereoncrum()` at `retrie.c:345-372` computes:

```
left  = offset + cdsp        (grasp)
right = left + cwid           (reach)
```

Then classifies `address` against these values. ONMYRIGHTBORDER fires when `address == reach` — strict equality, not "within some epsilon."

The KB's formal statement from [SS-WHEREONCRUM]:

> `whereoncrum(crum, crum.reach) == OnRight`

And the concrete example:

```
whereoncrum(crum, v+1) → ONMYRIGHTBORDER (1)   ← NOT THRUME
```

## Does It Use `tumblereq` (Full 16-Digit Comparison)?

The KB doesn't quote the literal implementation of `whereoncrum`'s equality check. What it does specify:

- **`tumblereq`** (`tumble.c:24-36`): two tumblers are equal iff sign, exponent, and all 16 mantissa digits match — "no normalization ambiguity after `tumblerjustify`" [SS-TUMBLER Finding 0031]
- **`tumblercmp`** returning `EQUAL` (`tumble.c:72-85`): same criteria — sign then absolute value via `abscmp` which does lexicographic mantissa comparison [INV-TUMBLER-TOTAL-ORDER]

The five-way classification in [SS-INTERVAL-CMP] is built on `tumblercmp`, and `intervalcmp`/`whereoncrum` share the same structure. Both `tumblereq` and `tumblercmp == EQUAL` are functionally identical for non-degenerate tumblers — they both require sign, exponent, and all 16 mantissa digits to match.

**Practical consequence:** since `cwid > 0` is enforced by [INV-NO-ZERO-WIDTH-CRUM], the reach is always positive, avoiding the zero-tumbler special case in `tumblercmp`. The ONMYRIGHTBORDER check is therefore a full 16-digit field comparison regardless of which function is called internally.

## Why This Matters

From [ST-INSERT] / [SS-WHEREONCRUM]: when `INSERT at v+1` encounters a crum whose reach equals `v+1`, `makegappm()` exits early (no knife cut), and `isanextensionnd()` then checks `reach == new_origin` using this same equality. This is what enables coalescing (the `+0 crums` cost for sequential typing). Any representation difference between `reach` and `new_origin` — even in "trailing" mantissa digits — would break coalescing and force a split, increasing crum count unnecessarily.

**Summary:** ONMYRIGHTBORDER requires exact tumbler equality between the query point and `offset + cdsp + cwid`. The KB identifies the comparison as using the tumbler total order (effectively all 16 digits), but does not confirm whether the implementation calls `tumblereq` directly vs derives it from `tumblercmp == EQUAL`.

---

## Code Exploration

I now have everything needed to answer precisely. Here is the complete analysis:

---

## `ONMYRIGHTBORDER` in `whereoncrum`: Precise Boundary Condition

### The function — `retrie.c:345`

```c
INT whereoncrum(typecorecrum *ptr, typewid *offset, tumbler *address, INT index)
```

It classifies where `address` falls relative to the crum's interval. The interval is `[left, right)` — but the boundary cases make it half-open only at the logical level. The actual conditions are:

### SPAN/POOM path (lines 354–372)

**Right endpoint `right` is computed as:**
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // left = offset + displacement
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // right = left + width
```
`right` = offset displacement + crum displacement + crum width — the exclusive end of the crum's span.

**`ONMYRIGHTBORDER` is returned when** [`retrie.c:365–369`]:
```c
cmp = tumblercmp(address, &right);
if (cmp == LESS) {
    return(THRUME);
} else if (cmp == EQUAL) {
    return(ONMYRIGHTBORDER);   // ← exact equality
} else {
    return(TOMYRIGHT);
}
```

**Yes — it requires exact equality** between `address` and `right` (= displacement + width). Not `<=`, not "within epsilon" — precisely `tumblercmp(address, right) == EQUAL`.

### GRAN path (line 351–353)

```c
tumbleradd(&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
return(intervalcmp(&offset->dsas[WIDTH], &right, address));
```

`intervalcmp` at `tumble.c:144–160` applies the same two-step `tumblercmp` logic — `ONMYRIGHTBORDER` iff `tumblercmp(address, right) == EQUAL`.

---

### Does it use `tumblereq`?

**No.** `whereoncrum` calls `tumblercmp` [`retrie.c:357, 365`], not `tumblereq`. These are different functions:

| Function | Definition | What it compares |
|----------|-----------|-----------------|
| `tumblereq` | `tumble.c:24` | All fields: `xvartumbler`, `varandnotfixed`, `sign`, `exp`, all 16 mantissa digits |
| `tumblercmp` | `tumble.c:72` | Numeric value only: handles zero specially, compares `sign`, `exp`, then all `NPLACES` mantissa digits via `abscmp` |

`tumblercmp` returns `EQUAL` (defined as `0` at `common.h:80`) when `abscmp` finds: same `exp`, then all `NPLACES=16` mantissa digits equal [`tumble.c:92–110`].

So while `tumblercmp` does not compare the `xvartumbler` or `varandnotfixed` fields (those are checked only by `tumblereq`), it **does** do a full 16-digit mantissa comparison when exponents match, iterating `for (i = NPLACES; i--;)` at `tumble.c:101`.

---

### Summary

1. **Boundary condition:** `ONMYRIGHTBORDER` is returned iff `address == right` exactly, where `right = offset.dsas[index] + crum.cdsp.dsas[index] + crum.cwid.dsas[index]` — i.e., `address` equals the crum's reach (displacement + width) precisely. One digit of difference returns `TOMYRIGHT`.

2. **Comparison function used:** `tumblercmp`, not `tumblereq`. The `EQUAL` result from `tumblercmp` requires: same sign, same exponent, and all 16 mantissa places equal (`NPLACES=16`, `common.h:53`).

3. **`tumblereq` is not used here.** It additionally compares `xvartumbler` and `varandnotfixed` — structural fields for variable tumbler support — which `tumblercmp` ignores. `tumblereq` appears in `tumblersub` and `strongsub`, not in the interval comparison path.

4. **The macro equivalents** (`intervalcmppart2` at `retrie.c:343`) are commented out in the live SPAN/POOM path but show the same intent — they were the precursors to the inlined code at lines 364–372, and produce identical results.
