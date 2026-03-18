## Question 13 [gregory]

> Is there a canonical representation for a given region of tumbler space, or can the same set of positions be described by spans with different (start, width) pairs using different exponent encodings?

## KB Synthesis

There is no single canonical representation. The same region of tumbler space can be described by spans with different exponent encodings, and these representations are **not equal** as tumblers.

## Start Positions: Canonical After Justification

For start positions alone, `tumblerjustify` normalizes the tumbler, and after that step, `tumblereq` (equality) is unambiguous — two tumblers are equal iff their sign, exponent, and all 16 mantissa digits match [SS-TUMBLER, Finding 0031]. So a given start point has a canonical form once justified.

## Widths: Not Canonical

Width is where non-uniqueness enters. The same integer "width" can be encoded at different tumbler precisions, producing unequal tumbler values.

This is directly evidenced by [SS-INSERT-VWIDTH-ENCODING, Finding 0076] and [INV-WIDTH-VALUE-EQUIVALENCE]:

> `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` but `crum.width.dsas[V] != crum.width.dsas[I]` as tumbler representations

Concretely: a 11-character span yields
- I-width: `0.0.0.0.0.0.0.0.11` (9-digit precision, exp = −8)
- V-width: `0.11` (2-digit precision, exp = −1)

Both decode to integer 11, but `tumblercmp` treats them as distinct values — different exponents mean different positions in the total order [INV-TUMBLER-TOTAL-ORDER].

## Arithmetic Consequences

This non-canonicality is not merely representational — it affects computation. The `strongsub` exponent guard [SS-TUMBLER, Finding 0055] returns the minuend **unchanged** when the subtrahend's exponent is strictly less than the minuend's. Two widths encoding the same integer but at different precisions will behave differently in subtraction:

```
strongsub(a={exp=0}, b={exp=-1}):
  b.exp (-1) < a.exp (0) → no-op, returns a unchanged
```

This is why [FC-SUBSPACE, Finding 0055] notes that DELETE's subspace isolation is an **accidental** property of exponent mismatch — link displacements at `exp=0` are immune to deletion widths at `exp=-1`, even when they represent overlapping numeric ranges.

## Summary

| Aspect | Canonical? |
|--------|-----------|
| Start position (after `tumblerjustify`) | Yes |
| Width value (as tumbler) | No — same integer encodable at multiple precisions |
| Region equality via `tumblereq` | Requires matching exponent + mantissa, not just numeric value |

The POOM exploits this intentionally [SS-POOM-BOTTOM-CRUM]: V-widths are re-encoded at V-address precision, I-widths copied directly. The same region's extent is stored twice in different tumbler encodings, and they compare unequal. Any spec reasoning about "equivalent spans" must use value extraction (`tumblerintdiff`) rather than tumbler equality.

---

## Code Exploration

Now I have a complete picture. Here is the full answer.

---

## Canonical Representation in Tumbler Space

### The Tumbler Data Structure

A tumbler is defined in `backend/common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;     // 1 if negative, 0 otherwise
    short exp;         // always <= 0 in normalized form
    tdigit mantissa[NPLACES]; // 16 × uint32_t
} tumbler;
```

`tdigit` is `uint32_t` (`common.h:57`). `NPLACES` is `16` (`common.h:53`). The `exp` field is a signed short.

---

### The Canonical Form Is Unique — and Enforced by Code

#### The normalization invariant

`tumblercheckptr` [tumble.c:169-227] rejects three kinds of malformed tumblers:

1. **`exp > 0`** — [tumble.c:174-179]: only negative or zero exponents are valid.

2. **`exp != 0` AND `mantissa[0] == 0`** — [tumble.c:186-191]: flagged as `"fucked up non-normalized"`. The mantissa must be left-justified; the first slot cannot be zero unless the exponent is also zero.

3. **`mantissa[0] == 0` with any non-zero digit elsewhere** — [tumble.c:192-200]: flagged as `"nonzerozerotumbler"`.

The consequence: **`exp` encodes exactly how many leading-zero "stories" precede the first non-zero mantissa digit, and that mapping is injective.** A tumbler with `exp = -2, mantissa = [3, 5, 0, ...]` represents `0.0.3.5`; there is no other valid encoding of that address.

#### The human-readable serialization confirms this

`puttumbler` in `put.c:26-46` renders the exponent as literal leading `0.` groups:

```c
for(i = tumblerptr->exp; i < 0; ++i)
    fprintf(outfile, "0.");
// then prints mantissa[0..last_nonzero]
```

So `exp = -2, mantissa = [3, 5, ...]` serializes as `0.0.3.5`.

The FEBE wire format (`putfe.c:104-117`) sends `-exp` as an explicit integer prefix:

```c
putnum (outfile, - tumblerptr->exp);   // e.g. sends "2"
// then sends TUMDELIM-separated mantissa digits
```

The FEBE parser (`get2fe.c:69-88`) reads them back:

```c
getnum (taskptr, &num);
tumblerptr->exp = -num;
for (i = 0; gettdigit(taskptr, &value); i++) {
    tumblerptr->mantissa[i] = value;
}
```

There is no normalization step on FEBE input. The backend takes the `exp` and mantissa exactly as supplied. An input like `2.0.0.3.5~` would produce `exp = -2, mantissa = [0, 0, 3, 5, ...]` — but that would fail `tumblercheckptr` (rule 2: exp≠0 and mantissa[0]=0). **The protocol accepts whatever the client sends, but only internally-normalized tumblers are valid.**

#### `tumblerjustify` enforces normalization after arithmetic

Any arithmetic operation that might leave leading zeros calls `tumblerjustify` [tumble.c:289-313]:

```c
for (shift = 0; mantissaptr[shift] == 0; ++shift) { … }
for (i = 0, j = shift; j < NPLACES;)
    mantissaptr[i++] = mantissaptr[j++];
tumblerptr->exp -= shift;
```

It strips leading zeros and compensates by decrementing `exp`. After justification, `mantissa[0]` is again the first non-zero digit. `tumblersub` always calls `tumblerjustify` at [tumble.c:430]. The addition path (`absadd`) leaves the result left-justified by construction [tumble.c:444-485].

---

### Comparison Is Structural, Not Semantic

`abscmp` [tumble.c:87-111] compares by `exp` first:

```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp)
        return(LESS);
    else
        return(GREATER);
}
```

Two tumblers with **different `exp` values can never compare as `EQUAL`**, regardless of their mantissa contents. This means the ordering and equality relations treat the canonical structural encoding as the identity of the value.

`tumblereq` [tumble.c:24-36] does field-by-field comparison including `exp` and every mantissa slot. Again: different `exp` ⟹ not equal.

---

### Spans: (start, width) Is Also Uniquely Determined

`typespan` (= `typevspan`, `typeispan`) is defined in `xanadu.h:65-71`:

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid itemid;
    tumbler stream;   // start
    tumbler width;
} typespan;
```

There is **no additional span-level normalization** beyond the individual tumbler normalizations. Both `stream` and `width` are canonical tumblers. Because each canonical tumbler has a unique encoding, a given pair (start, width) has exactly one binary representation, and that representation uniquely identifies the half-open interval `[start, start+width)`.

The span merger in `putvspaninlist` [orglinks.c:329-387] checks for adjacency via `tumblercmp` returning `EQUAL` on endpoints — which only occurs when the tumblers are structurally identical. This would break if two differently-encoded tumblers could represent the same address; the fact that it is not guarded against reflects the assumption that canonical form is unique.

---

### The One Real Hazard: `strongsub` Truncates Across Scales

`strongsub` [tumble.c:534-565] has a surprising early-exit:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

If `b` is at a finer scale (more negative `exp`) than `a`, the function returns `a` unchanged rather than computing `a − b`. The rationale: at the scale of `a`, `b` contributes nothing to the upper stories, so the result is considered equal to `a`. This is **lossy** — span endpoints computed via such subtraction can silently drop fine-grained contributions.

This does not create two encodings for one value. It means that certain span widths, when computed through subtraction, will be rounded up to the coarser granularity. The result is still canonical; it just does not represent the mathematically exact difference.

---

### Summary

| Property | Verdict | Key evidence |
|---|---|---|
| Each tumbler value has exactly one normalized encoding | **Yes** | `tumblercheckptr` [tumble.c:186-191], `tumblerjustify` [tumble.c:289-313] |
| Two tumblers with different `exp` can be equal | **No** | `abscmp` [tumble.c:92-96] returns LESS/GREATER before checking mantissa |
| A span (start, width) uniquely identifies a region | **Yes**, given canonical components | No span-level normalization beyond tumbler normalization |
| Non-canonical tumblers can be injected via FEBE | **Yes** (silently) | `get2fe.c:69-88` does not call `tumblercheckptr` on input |
| Scale-crossing subtraction is exact | **No** | `strongsub` [tumble.c:544-547] rounds coarser when `b->exp < a->exp` |

**The canonical form is unique.** Given the normalization invariant (`exp` = count of leading-zero stories, `mantissa[0]` = first non-zero digit), the same set of tumbler-space positions cannot be described by two different valid (start, width) pairs with different exponent encodings. The `exp` field is not a floating-point scale factor that can be freely shifted; it is an address-component index that is structurally bound to the mantissa content.
