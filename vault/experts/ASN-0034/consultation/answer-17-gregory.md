## Question 17 [gregory]

> When two tumblers have different exponents, `tumblercmp` compares them — is the ordering purely lexicographic on the (exponent, mantissa) pair, or does the exponent shift the mantissa digits before comparison so that `2.1` (exp=0) and `0.21` (exp=-1) compare as equal?

## KB Synthesis

The comparison is **not** value-normalizing. `2.1` (exp=0) and `0.21` (exp=-1) compare as strictly ordered, not equal.

From [SS-TUMBLER] Finding 0031 and [INV-TUMBLER-TOTAL-ORDER]:

`abscmp` uses a two-phase comparison:
1. **Exponent first** — a larger exponent means a larger absolute value, full stop.
2. **Mantissa second** — lexicographic left-to-right, only when exponents are equal.

For your example:
- `2.1`: `exp=0`, `mantissa=[2,1,0,...,0]`
- `0.21`: `exp=-1`, `mantissa=[2,1,0,...,0]`

`abscmp` sees `exp=0 > exp=-1` and returns GREATER immediately — the mantissa is never consulted. So `2.1 > 0.21`.

**Equality is exact match**: two tumblers are equal iff sign, exponent, and all 16 mantissa digits match. [SS-TUMBLER] Finding 0031 states explicitly: "no normalization ambiguity after `tumblerjustify`." `tumblerjustify` canonicalizes the representation, and then `tumblereq` is a bitwise comparison of the three fields.

This design is what makes [SS-TUMBLER] Finding 0055's `strongsub` exponent guard meaningful: when `b.exp < a.exp`, `strongsub` returns `a` unchanged rather than attempting cross-exponent arithmetic — because the exponent comparison alone encodes a magnitude relationship that prevents the subtraction from being meaningful at the same scale.

---

## Code Exploration

The answer is clear from two functions in `backend/tumble.c`. Let me walk through them precisely.

---

## `tumblercmp` [tumble.c:72–85]

```c
INT tumblercmp(tumbler *aptr, tumbler *bptr)
{
    if (iszerotumbler(aptr)){
        if (iszerotumbler(bptr))
            return (EQUAL);
        else
            return (bptr->sign ? GREATER : LESS);
    }
    if (iszerotumbler(bptr))
        return (aptr->sign ? LESS : GREATER);
    if (aptr->sign == bptr->sign)
        return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
    return (aptr->sign ? LESS : GREATER);
}
```

Zero-tumbler edge cases aside, for two positive tumblers it delegates directly to `abscmp(aptr, bptr)`.

---

## `abscmp` [tumble.c:87–111] (active branch — `#ifndef ExPeriMental`)

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {
        if (aptr->exp < bptr->exp) {
            return(LESS);
        } else {
            return(GREATER);
        }
    } else {
        a = (INT *) aptr->mantissa;
        b = (INT *) bptr->mantissa;
        for (i = NPLACES; i--;) {
            if(!(cmp = *a++ - *b++)){
            } else if (cmp < 0) {
                return (LESS);
            } else {
                return (GREATER);
            }
        }
    }
    return (EQUAL);
}
```

The logic is a strict two-level lexicographic comparison:

1. **Primary key: exponent** [tumble.c:92–97]. If `aptr->exp != bptr->exp`, the result is decided **entirely by the exponent** — the mantissa is never examined.
2. **Secondary key: mantissa, slot by slot** [tumble.c:99–108]. Only reached when exponents are equal; compares `mantissa[0]`, `mantissa[1]`, … left-to-right.

There is **no digit shifting**. The mantissa slots of `a` and `b` are compared directly at the same array indices. The exponent is treated as an independent key, not as an alignment offset.

---

## Answering the specific example

For `2.1` (exp=0, mantissa=[2,1,…]) vs `0.21` (exp=-1, mantissa=[2,1,…]):

- The exponents differ: 0 ≠ -1.
- `abscmp` enters the `if (aptr->exp != bptr->exp)` branch [tumble.c:92].
- `exp=0 > exp=-1`, so `2.1` returns **GREATER**.
- The mantissa arrays `[2,1,…]` are **never consulted**.

They do **not** compare as equal. The encoding `0.21` with exp=-1 is a completely different address from `2.1` with exp=0 — the exponent is treated as a distinct numeric field, not as a decimal-shifting mechanism.

---

## Normalization constraint confirms this

`tumblercheckptr` [tumble.c:186–191] enforces:
```c
if (ptr->exp && ptr->mantissa[0] == 0){
    wrong = TRUE;
}
```

A valid non-zero tumbler with `exp != 0` must have `mantissa[0] != 0` (no leading zeros). `tumblerjustify` [tumble.c:289–313] normalizes by shifting leading zeros out and **decrementing** `exp` by the shift count. This means the representation is canonical: there is only one valid encoding for any given abstract address. Two tumblers that "look the same after alignment" would have already been collapsed into the same canonical form before comparison — so there is no need for `abscmp` to perform alignment. It simply never does.

---

## Conclusion

**The ordering is purely lexicographic on the `(exp, mantissa)` pair.** The exponent is not used to align or shift digits before comparison. `2.1` (exp=0) and `0.21` (exp=-1) compare as **GREATER/LESS** — not equal — because their exponents differ, and `abscmp` returns immediately on that difference without ever looking at the mantissa.
